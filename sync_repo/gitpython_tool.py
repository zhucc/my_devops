#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06 13:33:10
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    :

from git import Repo, Git
from poc_config import file_to_be_filter, components
from os import path as osp


class GitRepo(Repo):
    """docstring for RepoTools."""

    def get_changed_component(self, commit_value):
        commit = self.commit(commit_value)
        previous = commit.parents
        diff = commit.diff(previous)
        change_files = [
            d.a_path.split("/")[1]
            for d in diff
            if components in d.a_path]
        return ",".join(list(set(change_files) & file_to_be_filter))

    def get_all_commits_of_branch(self, branch):
        all_commits = [str(i.hexsha) for i in self.iter_commits(branch)]
        all_commits.reverse()
        return all_commits

    def get_file_commit(self, file_name, short=False):
        c = list(self.iter_commits(paths=file_name, max_count=1))[0]
        commit = c.hexsha[:7] if short is True else c.hexsha
        return commit

    def get_commits_by_files(self, file_list, short=False):
        commit_list = map(lambda f: self.get_file_commit(osp.join(components, f), short), file_list)
        return dict(zip(file_list, commit_list))


class GitCmd(Git):
    """git fun base on git command."""

    def get_file_commit(self, file_name, short=False):
        print file_name
        short_flag = "h" if short is True else "H"
        return self.execute("git log -n1 --format=%{1} {0}".format(file_name, short_flag))

    def get_commits_by_files(self, file_list, short=False):
        # return {file:***}
        commit_list = map(lambda f: self.get_file_commit(f, short), file_list)
        return dict(zip(file_list, commit_list))

    def get_modified_dir(self):
        r = self.execute("git status -s ")
        # print (r == u"" )
        if r:
            return set([
                change.split()[1].split("/")[0]
                for change in r.split("\n")])
        else:
            return set(list())


if __name__ == '__main__':
    gg = GitCmd("meta-5g/recipes-components")
    print gg.get_file_commit("oamagent")
    # print git.get_commits_by_files(file_to_be_filter)
    # print repo.get_all_commits_of_branch("master")
    # for i, c in enumerate(repo.get_all_commits_of_branch("master")):
    #     print i, repo.get_changed_component(c)
