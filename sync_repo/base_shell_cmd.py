#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-26 13:53:49
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    :
import os
from commands import getstatusoutput as excute_shell


class ExcuteShellError(BaseException):
    """docstring for ExcuteShellError."""

    pass


def run_shell(commands):
    """If don't check result,use excute_shell."""
    # print("running:  {0}".format(commands))
    result = excute_shell(commands)
    if result[0] != 0:
        raise ExcuteShellError(
            "excute {0} failed,{1}".format(commands, result[-1]))
    return result[-1]


def union_dict(*objs):
    _keys = reduce(lambda a, b: list(set(a + b)), [obj.keys() for obj in objs])
    _total = {}
    for _key in _keys:
        _total[_key] = ",".join([obj.get(_key, "") for obj in objs if obj.get(_key, "")])
    return _total


def write_dict_to_file(file_name, dict_to_write):
    new_dict = dict()
    for k, v in dict_to_write.items():
        if not isinstance(v, str):
            new_dict[k] = str(v)
    with open(file_name, "w") as f:
        data = map(lambda kv: ":".join(kv) + "\n", new_dict.items())
        f.writelines(data)


def get_patchset_by_info(infos):
    try:
        for info in infos:
            if "https://gerrit.ext.net.nokia.com/:" in info:
                return info.split()[1].split("/")[-1]
    except Exception:
        print "get patchset version failed ...."
        return ""



# below fun need to run in git repo

def get_modified_components():
    r = run_shell("git status -s")
    return [
        l.split("/")[1]
        for l in r.split("\n")
        if r
    ]

def commit_short2long(short):
    return run_shell("git log {} -n1 --format=%H".format(short))

def get_commit_by_file(file, short=False):
    short_flag = "h" if short is True else "H"
    return run_shell("git log -n1 --format=%{0} {1} ".format(short_flag, file))


def get_commits_from_repo_with_closure(repo):
    def get_commits_from_files(src_files):
        os.chdir(repo)
        commit_ids = [get_commit_by_file(file) for file in src_files]
        return commit_ids
    return get_commits_from_files


def get_commits_from_repo(repo_dir, file_list, short=False):
    # return {file:***}
    os.chdir(repo_dir)
    commit_list = map(lambda f: get_commit_by_file(f), file_list)
    commit_list = [
        c[:7] if short
        else c
        for c in commit_list]
    return dict(zip(file_list, commit_list))


def get_commits_between(commit_new, commit_old, file, short=False):
    if commit_new == commit_old:
        return list()
    short_flag = "h" if short is True else "H"
    commits_string = run_shell(
        "git log --format=%{3} {0}..{1}  -- {2}".format(
            commit_old, commit_new, file, short_flag))
    return commits_string.split("\n")


def local_branch_exist(branch_name):
    return branch_name in run_shell("git branch")


def get_change_file_by_commits(commits):
    return map(get_change_file_by_commit, commits)


def get_change_file_by_commit(commit):
    infos = run_shell("git show {0} | grep ^+++".format(commit))
    files = list()
    for info in infos.split("\n"):
        if "recipes-components" not in info:
            pass
        data = info.split("/")[1:3]
        files.append("/".join(data))
    return files


if __name__ == '__main__':
    os.chdir("meta-5g/recipes-components")
    from poc_config import file_to_be_filter
    print get_commits_from_repo(list(file_to_be_filter), short=True)