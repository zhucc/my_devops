#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-01 10:13:25
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou

from gitpython_tool import GitRepo
from base_shell_cmd import get_commit_by_file, commit_short2long
from mysql_tool import PCISQL
from pci_model import RepoRelationship, database
from poc_config import file_to_be_filter
from collections import OrderedDict
import os
import sys
import requests
sys.path.append(os.path.realpath(".."))
from CITOOLS.api.gerrit_rest import GerritRestClient
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# filed name of sql model define
order_num = "meta_5g"
commit_value = "meta_5g_ci"
change_files = "meta_5g_changed_file"
poc_commit = "meta_5g_poc_ci"


def record_last_commit(sql_op, repo_path, file_list=file_to_be_filter):
    """Get commits by file list,record commits to sql."""
    os.chdir(repo_path)
    f2c = {
        f: get_commit_by_file(f, short=True)
        for f in file_list}
    sql_op.write_last_commit_to_sql(f2c)


def query_changes_by_commits(gerrit_op, commits):
    long_commits = map(commit_short2long, commits)
    changes = [query_change_by_commit(gerrit_op, c) for c in long_commits]
    return changes


def query_change_by_commit(gerrit_op, commit):
    res = gerrit_op.query_ticket(commit)
    change = str(res[0].get("_number")) if res else "?"
    return change


def record_changes_by_commits(sql_op, gerrit_op, poc_repo_path):
    commits_datas = sql_op.get_cloumn_records_by_model_filed(RepoRelationship, poc_commit)
    commits_datas = set(commits_datas) - set([None])
    os.chdir(poc_repo_path)
    for commits in commits_datas:
        print commits
        changes = query_changes_by_commits(gerrit_op, commits.split(","))
        change_value = ",".join(changes)
        print change_value
        data = dict(meta_5g_poc_change=change_value)
        sql_op.update_row_records_by_key_value(RepoRelationship, poc_commit, commits, data)


def get_commit_info(repo_op, allcommits):
    def get_commit_change(commit):
        commit_index = int(allcommits.index(commit))
        changes = repo_op.get_changed_component(commit)
        return OrderedDict([
            (order_num, commit_index),
            (commit_value, commit[:7]),
            (change_files, changes)])
    return get_commit_change


def record_changes_of_all_commits(repo_op, repo_branch, sql_op, model, step):
    """Get repo's change files and record them to mysql with peewee."""
    allcommits = repo_op.get_all_commits_of_branch(repo_branch)
    get_commit_and_changes = get_commit_info(
        repo_op=repo_op, allcommits=allcommits)
    exist_sql_commits = sql_op.get_cloumn_records_by_model_filed(
        model, commit_value)
    # convert commits from 7 byte to 40 byte
    exist_sql_commits = [c for c in allcommits if c[:7] in exist_sql_commits]
    to_do_commits = [c for c in allcommits if c not in exist_sql_commits]
    for i in range(0, len(to_do_commits), step):
        sql_data = list()
        for c in to_do_commits[i:i + step]:
            one_data = get_commit_and_changes(c)
            print "getting {0} {1}  >>>>  {2}".format(*one_data.values())
            sql_data.append(one_data)
        if sql_data:
            with sql_op.db.atomic():
                model.insert_many(sql_data).execute()


def _main():
    try:
        db_poc = PCISQL(database)
        repo = GitRepo("meta-5g")
        gerrit_op = GerritRestClient("https://gerrit.ext.net.nokia.com/gerrit/", "myselfname", "iNLR+89OU4LfRmMzxOznkP1UGNJVtz8YTi/BZ/DNRg")
        record_changes_of_all_commits(repo, "master", db_poc, RepoRelationship, 10)
        # record_changes_by_commits(db_poc, gerrit_op, "meta-5g-poc")
        # record_last_commit(db_poc, "meta-5g/recipes-components")
    except Exception:
        raise
    finally:
        db_poc.close_sql()


if __name__ == '__main__':
    _main()
