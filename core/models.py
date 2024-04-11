from django.db import models


class Jobs(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Jobs'


class Materialsjobs(models.Model):
    job = models.ForeignKey(Jobs, models.CASCADE, blank=True, null=True)
    material = models.ForeignKey('Materials', models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MaterialsJobs'


class Slag(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    SiO2 = models.FloatField(db_column='SiO2', blank=True, null=True)  # Field name made lowercase.
    CaO = models.FloatField(db_column='CaO', blank=True, null=True)  # Field name made lowercase.
    Al2O3 = models.FloatField(db_column='Al2O3', blank=True, null=True)  # Field name made lowercase.
    FeO = models.FloatField(db_column='FeO', blank=True, null=True)  # Field name made lowercase.
    Weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    job = models.ForeignKey(Jobs, models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Slag'


class Stein(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    Gold = models.FloatField(db_column='Gold', blank=True, null=True)  # Field name made lowercase.
    Silver = models.FloatField(db_column='Silver', blank=True, null=True)  # Field name made lowercase.
    Weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    Copper = models.FloatField(db_column='Copper', blank=True, null=True)  # Field name made lowercase.
    Iron = models.FloatField(db_column='Iron', blank=True, null=True)  # Field name made lowercase.
    Sulfur = models.FloatField(db_column='Sulfur', blank=True, null=True)  # Field name made lowercase.
    job = models.ForeignKey(Jobs, models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Stein'


class Materials(models.Model):
    name0 = models.CharField(max_length=255)
    Weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    Au = models.FloatField(db_column='Au', blank=True, null=True)  # Field name made lowercase.
    Ag = models.FloatField(db_column='Ag', blank=True, null=True)  # Field name made lowercase.
    SiO2 = models.FloatField(db_column='SiO2', blank=True, null=True)  # Field name made lowercase.
    CaO = models.FloatField(db_column='CaO', blank=True, null=True)  # Field name made lowercase.
    S = models.FloatField(db_column='S', blank=True, null=True)  # Field name made lowercase.
    Fe = models.FloatField(db_column='Fe', blank=True, null=True)  # Field name made lowercase.
    Cu = models.FloatField(db_column='Cu', blank=True, null=True)  # Field name made lowercase.
    Al2O3 = models.FloatField(db_column='Al2O3', blank=True, null=True)  # Field name made lowercase.
    As0 = models.FloatField(db_column='As0', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'materials'

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