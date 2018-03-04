#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-24 15:05:46
# @Author  : robin (robin.zhu@nokia-sbell.com)
# @site    : HangZhou
# @Desc    :
import pci_model as pcim
from playhouse.shortcuts import model_to_dict


class PCISQL(object):
    """auto connect mysql,advanced fun of peewee."""

    def __init__(self, database):
        self.db = database
        self.db.connect()
    # basic

    def get_cloumn_records_by_model_filed(self, model, field):
        return [getattr(record, field) for record in model.select()]

    def get_row_records_by_key_value(self, model, field_name, field_value):
        row_records = model.select().where(
            getattr(model, field_name) == field_value)
        return model_to_dict(row_records.get())

    def update_row_records_by_key_value(self, model, field_name, field_value, data):
        update_cmd = model.update(
            **data).where(getattr(model, field_name) == field_value)
        return update_cmd.execute()

    # advanced
    def gen_module_version(self,
                           model=pcim.PocModuleVersion,
                           field_name="version",
                           field_value="self_def"):
        row_record = model.select().where(
            getattr(model, field_name) == field_value).get()
        module_version = "{0}.{1}.{2}".format(
            row_record.part1, row_record.part2, row_record.part3)
        new_part3 = str(int(row_record.part3) + 1).zfill(6)
        row_record.update(part3=new_part3).execute()
        return module_version

    def get_poc_last_commits_from_sql(self,
                                      model=pcim.Poclastcommit,
                                      field_name="version",
                                      field_value="new"):
        # return {my_fi_le:***}
        return self.get_row_records_by_key_value(model,
                                                 field_name,
                                                 field_value)

    def write_last_commit_to_sql(self, file_2_commit, model=pcim.Poclastcommit):
        # raw file name is illegality for sql
        new_data = {}
        for f, c in file_2_commit.items():
            new_data["my_{0}".format(f.replace("-", "_"))] = c
        old_data = self.get_poc_last_commits_from_sql()
        old_data.pop("version")
        self.update_row_records_by_key_value(model, "version", "old", old_data)
        return self.update_row_records_by_key_value(model, "version", "new", new_data)

    def write_commits(self, table_name, key_name, value_name, kv_dict):
        for k, v in kv_dict.items():
            print "{2}.update({0}=v).where({2}.{1} == k)".format(
                value_name, key_name, table_name)
            query = eval("{2}.update({0}=v).where({2}.{1} == k)".format(
                value_name, key_name, table_name))
            if query.execute():
                print "write relationship success {0}>>{1}:  \
                  {2}>>>>{3}".format(key_name, value_name, k, v)

    def write_relationship_commit(self, key_name, value_name, kv_dict):
        print "write relationship .... {0}>>{1}:  with{2}".format(key_name,
                                                                  value_name,
                                                                  kv_dict)
        self.write_commits("RepoRelationship", key_name, value_name, kv_dict)
        print "write relationship .... {0}>>{1} finished".format(key_name,
                                                                 value_name)

    def close_sql(self):
        if self.db.is_closed():
            return "close sql success"
        else:
            self.db.close()
            return "close sql success"


if __name__ == '__main__':
    aa = PCISQL(pcim.database)
    print aa.gen_module_version()
    print aa.get_poc_last_commits_from_sql()
    aa.close_sql()
