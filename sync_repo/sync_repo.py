#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-19 09:59:02
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou

import os
import sys
import fire
import datetime
from collections import OrderedDict
from os import path as osp
from mysql_tool import PCISQL
from poc_config import (
    gerrit_branch, components, file_to_be_filter, workspace,
    gerrit_user, gerrit_token, gerrit_host)
from pci_model import RepoRelationship, database
from data_record import record_last_commit, record_changes_by_commits
from base_shell_cmd import (
    get_commit_by_file, get_commits_between,
    get_commits_from_repo, get_modified_components,
    get_commits_from_repo_with_closure, run_shell,
    local_branch_exist, write_dict_to_file, union_dict)
sys.path.append(os.path.realpath(".."))
from CITOOLS.api.gerrit_rest import GerritRestClient


def get_changed_commits(sql_op, repo_dir, file_list, short=True):
    """Compare repo commit with sql record according to file list to get new commits.

    return {file:[commit1,commit2...]}
    """
    os.chdir(repo_dir)
    changed_commits = OrderedDict()
    old_commits = sql_op.get_poc_last_commits_from_sql()
    new_commits = get_commits_from_repo(repo_dir, file_list, short=short)
    for f in file_list:
        sql_f = "my_{0}".format(f.replace("-", "_"))
        new_commit = new_commits[f]
        old_commit = old_commits[sql_f]
        print "{0} change from {1} to {2}".format(f, old_commit, new_commit)
        changed_commits[f] = get_commits_between(new_commit, old_commit, f, short=short)
    return changed_commits


def do_commit_by_dir(src_repo, dst_repo, subdir):
    what_i_commit = OrderedDict()
    file_version = OrderedDict()
    os.chdir(dst_repo)
    change_files = get_modified_components()
    change_files = list(set(change_files) & file_to_be_filter)
    get_src_commits = get_commits_from_repo_with_closure(
        osp.join(src_repo, subdir))
    commit_ids = get_src_commits(change_files)
    os.chdir(osp.join(dst_repo, subdir))

    for index, file in enumerate(change_files):
        module_version = pci_op.gen_module_version()
        run_shell("git add {0}".format(file))
        run_shell("git commit -m 'commit from {0} {1} {2}'\
            ".format(commit_ids[index], file, module_version))
        head_commit = get_commit_by_file(".")
        what_i_commit[file] = head_commit
        file_version[file] = module_version
    return what_i_commit, file_version


def do_commit_all(repo):
    os.chdir(repo)
    run_shell("git add . ")
    if "nothing to commit" not in run_shell("git status"):
        run_shell("git commit -m 'sync repo at {0}'\
            ".format(datetime.datetime.now()))
        return list((get_commit_by_file("."),))
    return list()


def push_commits(dst_repo, local_branch, remote_branch, commits_to_push, commits_no_push):
    pushed_commits = OrderedDict()
    os.chdir(dst_repo)
    if not local_branch_exist(local_branch):
        run_shell("git checkout -b {0} --track origin/{1} \
            ".format(local_branch, remote_branch))
    run_shell("git checkout topush")
    for commit in commits_no_push:
        run_shell("git reset --hard origin/{0}".format(remote_branch))
        run_shell("git cherry-pick {0}".format(commit))
        run_shell("git push origin HEAD:{0}".format(remote_branch))
    run_shell("git fetch origin {0}".format(remote_branch))
    remote_url = run_shell("git config --get remote.origin.url")
    host, port = remote_url.split("@")[-1].split("/")[0].split(":")
    for file, commit in commits_to_push.items():
        run_shell("git reset --hard origin/{0}".format(remote_branch))
        run_shell("git cherry-pick {0}".format(commit))
        run_shell("git push origin HEAD:refs/for/{0}".format(remote_branch))
        new_commit = get_commit_by_file(".")
        pushed_commits[file] = new_commit
        run_shell("ssh -p {port} {user}@{host} gerrit review \
            --message 'auto_code_review ' \
            --code-review +2 {commit} \
            ".format(port=port, host=host, commit=new_commit, user=gerrit_user))
    return pushed_commits


def data_assemble(meta_5g_cis, mete_5g_poc_cis):
    """
    All input is dict which key is file_name.

    return dict which key is meta_5g commit.
    """
    record_data = dict()
    for f, commits in meta_5g_cis.items():
        for c in commits:
            record_cell = dict()
            record_cell["meta_5g_poc_ci"] = mete_5g_poc_cis.get(f, "")
            record_data[c] = union_dict(record_data.get(c, {}), record_cell)
    return record_data


def sync_repo_a2b(repo_a, repo_a_branch, repo_b, repo_b_branch):
    os.chdir(repo_b)
    if not local_branch_exist(repo_b_branch):
        run_shell("git checkout -b {0} --track origin/{0}".format(gerrit_branch))
    run_shell("git checkout {0}".format(gerrit_branch))
    run_shell("git reset --hard d2de26cb")
    run_shell("rsync -avz --delete --exclude '.git' {0}/ {1}/".format(repo_a, repo_b))


def sync_repo(src_repo, dst_repo):
    """
    Rsync src_repo to dst_repo.

    1.get changed file according to "git status".
    2.commit each changed dir and add commit to list.
    3.cherry-pick according to commit list(base on origin/branch and push).
    tip1:commit on master but cherrypick and push on 'topush' branch.
    4.get pushed commits in dict,filename:pushedcommit
    5.get changed commits in dict,filename:changed commits from srcrepo
    6.write pushed commits according to changed commits.
    """
    sync_repo_a2b(src_repo, gerrit_branch, dst_repo, gerrit_branch)
    commits_to_push, files_version = do_commit_by_dir(
        src_repo, dst_repo, components)
    commits_no_push = do_commit_all(dst_repo)
    print "commits_to_push:{}".format(commits_to_push)
    print "files_version:{}".format(files_version)
    print "commits_no_push:{}".format(commits_no_push)
    print "*************generate commit finished,start to push****************"
    pushed_commits = push_commits(
        dst_repo, "topush", gerrit_branch, commits_to_push, commits_no_push)
    pushed_commits = {f: pushed_commits.get(f)[:7] for f in pushed_commits.keys()}
    print "pushed_commits:{}".format(pushed_commits)
    print "********************push commit finished***************************"
    # write mete_5g_poc_ci meta_5g_poc_change meta_5g_changed_file according to mete_5g_ci
    src_commits = get_changed_commits(pci_op, osp.join(src_repo, components), pushed_commits.keys())
    print "src_commits,below file has these new commits since last sync:"
    for f, commits in src_commits.items():
        print "{0} >>>> {1}".format(f, commits)
    record_data = data_assemble(
        src_commits, pushed_commits)
    write_dict_to_file(osp.join(workspace, "record_data.log"), record_data)
    for commit, record_cell in record_data.items():
        pci_op.update_row_records_by_key_value(RepoRelationship, "meta_5g_ci", commit, record_cell)
    gerrit_op = GerritRestClient(gerrit_host, gerrit_user, gerrit_token)
    record_changes_by_commits(pci_op, gerrit_op, dst_repo)
    record_last_commit(pci_op, osp.join(src_repo, components))

if __name__ == '__main__':
    try:
        pci_op = PCISQL(database)
        fire.Fire(sync_repo)
    except Exception:
        raise
    finally:
        pci_op.close_sql()
