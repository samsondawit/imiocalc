# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Jobs(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Jobs'


class Materialsjobs(models.Model):
    job = models.ForeignKey(Jobs, models.DO_NOTHING, blank=True, null=True)
    material = models.ForeignKey('Materials', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MaterialsJobs'


class Metal(models.Model):
    ore_mass = models.FloatField()
    metal_content = models.FloatField()

    class Meta:
        managed = False
        db_table = 'Metal'


class Metalextractiondata(models.Model):
    c_cu_prod = models.FloatField()
    v_prod = models.FloatField()
    c_cu_raf = models.FloatField()
    c_cu_electrolyte_rich = models.FloatField()
    v_electrolyte_rich = models.FloatField()
    v_organic = models.FloatField()
    c_cu_electrolyte_depleted = models.FloatField()
    v_electrolyte_depleted = models.FloatField()

    class Meta:
        managed = False
        db_table = 'MetalExtractionData'


class Metalleachresult(models.Model):
    day = models.IntegerField()
    extraction_efficiency = models.FloatField()
    c_cu_organic_depleted = models.FloatField()
    c_cu_organic_rich = models.FloatField()
    re_extraction_efficiency_organic = models.FloatField()
    re_extraction_efficiency_electrolyte = models.FloatField()
    cu_gain = models.FloatField()
    total_accumulated_cu = models.FloatField()
    total_cu_recovery = models.FloatField()
    overall_extraction_efficiency = models.FloatField()
    job = models.ForeignKey(Jobs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MetalLeachResult'


class Slag(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sio2 = models.FloatField(db_column='SiO2', blank=True, null=True)  # Field name made lowercase.
    cao = models.FloatField(db_column='CaO', blank=True, null=True)  # Field name made lowercase.
    al2o3 = models.FloatField(db_column='Al2O3', blank=True, null=True)  # Field name made lowercase.
    feo = models.FloatField(db_column='FeO', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    job = models.ForeignKey(Jobs, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Slag'


class Stein(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    gold = models.FloatField(db_column='Gold', blank=True, null=True)  # Field name made lowercase.
    silver = models.FloatField(db_column='Silver', blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    copper = models.FloatField(db_column='Copper', blank=True, null=True)  # Field name made lowercase.
    iron = models.FloatField(db_column='Iron', blank=True, null=True)  # Field name made lowercase.
    sulfur = models.FloatField(db_column='Sulfur', blank=True, null=True)  # Field name made lowercase.
    job = models.ForeignKey(Jobs, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Stein'


class Totalbalanceresult(models.Model):
    in_raf_percent = models.FloatField()
    in_electrolyte_percent = models.FloatField()
    in_katods_percent = models.FloatField()
    in_organics_percent = models.FloatField()
    ore_remain_percent = models.FloatField()
    job = models.ForeignKey(Jobs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TotalBalanceResult'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CoreMetalextractiondata(models.Model):
    id = models.BigAutoField(primary_key=True)
    c_cu_prod = models.FloatField()
    v_prod = models.FloatField()
    c_cu_raf = models.FloatField()
    c_cu_electrolyte_rich = models.FloatField()
    v_electrolyte_rich = models.FloatField()
    v_organic = models.FloatField()
    c_cu_electrolyte_depleted = models.FloatField()
    v_electrolyte_depleted = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_metalextractiondata'


class CoreMetaljobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    job_id = models.BigIntegerField(blank=True, null=True)
    metal_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_metaljobs'


class CoreMetalleachresult(models.Model):
    id = models.BigAutoField(primary_key=True)
    day = models.IntegerField()
    extraction_efficiency = models.FloatField()
    c_cu_organic_depleted = models.FloatField()
    c_cu_organic_rich = models.FloatField()
    re_extraction_efficiency_organic = models.FloatField()
    re_extraction_efficiency_electrolyte = models.FloatField()
    cu_gain = models.FloatField()
    total_accumulated_cu = models.FloatField()
    total_cu_recovery = models.FloatField()
    overall_extraction_efficiency = models.FloatField()
    job_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_metalleachresult'


class CoreTotalbalanceresult(models.Model):
    id = models.BigAutoField(primary_key=True)
    in_raf_percent = models.FloatField()
    in_electrolyte_percent = models.FloatField()
    in_katods_percent = models.FloatField()
    in_organics_percent = models.FloatField()
    ore_remain_percent = models.FloatField()
    job_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_totalbalanceresult'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Materials(models.Model):
    name0 = models.CharField(max_length=255)
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    au = models.FloatField(db_column='Au', blank=True, null=True)  # Field name made lowercase.
    ag = models.FloatField(db_column='Ag', blank=True, null=True)  # Field name made lowercase.
    sio2 = models.FloatField(db_column='SiO2', blank=True, null=True)  # Field name made lowercase.
    cao = models.FloatField(db_column='CaO', blank=True, null=True)  # Field name made lowercase.
    s = models.FloatField(db_column='S', blank=True, null=True)  # Field name made lowercase.
    fe = models.FloatField(db_column='Fe', blank=True, null=True)  # Field name made lowercase.
    cu = models.FloatField(db_column='Cu', blank=True, null=True)  # Field name made lowercase.
    al2o3 = models.FloatField(db_column='Al2O3', blank=True, null=True)  # Field name made lowercase.
    as0 = models.FloatField(db_column='As0', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'materials'
