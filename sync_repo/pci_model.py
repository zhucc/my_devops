from peewee import *
# flake8: noqa
# create by peewee cmd
# python -m pwiz -e mysql -H 10.157.163.143 -u root -P 5gzuul_pwd zuul-pci > pci_model.py
database = MySQLDatabase(
    'zuul-pci',
    **{'host': '10.157.163.143', 'password': '5gzuul_pwd', 'user': 'root'})


class UnknownField(object):

    def __init__(self, *_, **__):
        pass


class BaseModel(Model):

    class Meta:
        database = database


class Poclastcommit(BaseModel):
    my_5gl1sw = TextField(null=True)
    my_cp_rt = TextField(null=True)
    my_cplane = TextField(null=True)
    my_deployment = TextField(null=True)
    my_interfaces = TextField(null=True)
    my_jscommbridge = TextField(null=True)
    my_l2_hi = TextField(null=True)
    my_l2_lo = TextField(null=True)
    my_l2_ps = TextField(null=True)
    my_l2_rt_common = TextField(null=True)
    my_logging_agent = TextField(null=True)
    my_mz_proxy = TextField(null=True)
    my_node_js = TextField(null=True)
    my_nodeoam = TextField(null=True)
    my_oamagent = TextField(null=True)
    my_oamagentjs = TextField(null=True)
    my_open_stack_heat_templates = TextField(null=True)
    my_pmagent_proxy = TextField(null=True)
    my_racoam = TextField(null=True)
    my_siteoam = TextField(null=True)
    my_syscom_proxy = TextField(null=True)
    version = TextField(null=True)

    class Meta:
        db_table = 'PocLastCommit'
        primary_key = False


class AlembicVersion(BaseModel):
    version_num = CharField(primary_key=True)

    class Meta:
        db_table = 'alembic_version'


class PocModuleVersion(BaseModel):
    part1 = TextField(null=True)
    part2 = TextField(null=True)
    part3 = TextField(null=True)
    version = TextField(null=True)

    class Meta:
        db_table = 'poc_module_version'
        primary_key = False


class RepoRelationship(BaseModel):
    gnb_change = CharField(null=True)
    gnb_ci = CharField(null=True)
    meta_5g_change = CharField(null=True)
    meta_5g_changed_file = CharField(null=True)
    meta_5g_ci = CharField(null=True)
    meta_5g = IntegerField(db_column='meta_5g_id', null=True)
    meta_5g_poc_change = CharField(null=True)
    meta_5g_poc_ci = CharField(null=True)

    class Meta:
        db_table = 'repo_relationship'
        primary_key = False


class ZuulBuildset(BaseModel):
    change = IntegerField(null=True)
    message = TextField(null=True)
    patchset = IntegerField(null=True)
    pipeline = CharField(null=True)
    project = CharField(null=True)
    ref = CharField(null=True)
    score = IntegerField(null=True)
    zuul_ref = CharField(null=True)

    class Meta:
        db_table = 'zuul_buildset'


class ZuulBuild(BaseModel):
    buildset = ForeignKeyField(
        db_column='buildset_id',
        null=True,
        rel_model=ZuulBuildset,
        to_field='id')
    end_time = DateTimeField(null=True)
    job_name = CharField(null=True)
    log_url = CharField(null=True)
    node_name = CharField(null=True)
    result = CharField(null=True)
    start_time = DateTimeField(null=True)
    uuid = CharField(null=True)
    voting = IntegerField(null=True)

    class Meta:
        db_table = 'zuul_build'


if __name__ == '__main__':
    database.create_table(Poclastcommit)
