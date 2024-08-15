from django.db import models

# Create your models here.
class Persons(models.Model):
    person_id = models.IntegerField(db_column='person_id', primary_key=True)
    surname = models.CharField(db_column='surname', max_length=100, blank=False, null=False)
    maiden_name = models.CharField(db_column='maiden_name', max_length=100, blank=True, null=True)
    name = models.CharField(db_column='name', max_length=100, blank=False, null=False)
    patronymic = models.CharField(db_column='patronymic', max_length=100, blank=True, null=False)
    gender = models.CharField(db_column='gender', max_length=1, blank=False, null=False)
    date_of_birth = models.CharField(db_column='date_of_birth', max_length=10, blank=True, null=True)
    date_of_death = models.CharField(db_column='date_of_death', max_length=10, blank=True, null=True)
    father = models.ForeignKey("self", related_name="fathers", on_delete=models.CASCADE, null=True, blank=True)
    mother = models.ForeignKey("self", related_name="mothers", on_delete=models.CASCADE, null=True, blank=True)
    note = models.CharField(db_column='Note', max_length=255, blank=True)
    info = models.TextField(db_column='info', blank=True, null=True)
    status = models.DecimalField(db_column='status', max_digits=1, decimal_places=0, null=False)
    edit_date = models.DateTimeField(db_column='edit_date', blank=True, null=False, auto_now=True)

    def __str__(self):
        if self.maiden_name > '':
            return self.surname + ' (' + self.maiden_name + ') ' + self.name + ' ' + self.patronymic
        return self.surname + ' ' + self.name + ' ' + self.patronymic
    

    class Meta:
        managed = True
        db_table = 'persons'


class Couples(models.Model):
    couple_id = models.AutoField(db_column='person_id', primary_key=True)
    he = models.ForeignKey(Persons, models.DO_NOTHING, related_name="he_set", null=False, blank=False)
    she = models.ForeignKey(Persons, models.DO_NOTHING, related_name="she_set", null=False, blank=False)
    note = models.CharField(db_column='Note', max_length=255, blank=True)
    status = models.DecimalField(db_column='status', max_digits=1, decimal_places=0, null=False)
    edit_date = models.DateTimeField(db_column='edit_date', blank=True, null=False, auto_now=True)

    def __str__(self):
        return self.he + ' - ' + self.she
    

    class Meta:
        managed = True
        db_table = 'couples'


# class Tpobj(models.Model):
#     tpobj_id = models.AutoField(db_column='TPObj_ID', primary_key=True)
#     tptype = models.ForeignKey(SprTptype, models.DO_NOTHING, db_column='TPTYPE_ID', blank=False, null=False)
#     tpname = models.CharField(db_column='TPNAME', max_length=35, blank=False, null=False, verbose_name='РќРѕРјРµСЂ')
#     prefix = models.CharField(db_column='PREFIX', max_length=10, blank=True, null=False, verbose_name='РџСЂРµС„РёРєСЃ')
#     res = models.ForeignKey(SprRes, models.DO_NOTHING, db_column='KPK', blank=False, null=False)
#     uch = models.ForeignKey(SprUch, models.DO_NOTHING, db_column='UCH_ID', blank=False, null=False)
#     consumertp = models.ForeignKey(Consumertp, models.DO_NOTHING, db_column='ConsumerTP_ID', blank=True, null=True)
#     datalinktype = models.ForeignKey(Datalinktype, models.DO_NOTHING, db_column='DataLinkType_ID', null=False)
#     xcoord = models.CharField(db_column='XCoord', max_length=15, blank=True, null=False, verbose_name='X-РєРѕРѕСЂРґРёРЅР°С‚Р°')
#     ycoord = models.CharField(db_column='YCoord', max_length=15, blank=True, null=False, verbose_name='Y-РєРѕРѕСЂРґРёРЅР°С‚Р°')
#     status = models.DecimalField(db_column='Status', max_digits=1, decimal_places=0, null=False)
#     editdate = models.DateTimeField(db_column='EditDate', blank=True, null=False, auto_now=True)

#     def __str__(self):
#         return self.prefix + self.tpname + ' ' + self.tptype.tptypename + ' = ' + self.res.resname

#     class Meta:
#         managed = False
#         db_table = 'tpobj'