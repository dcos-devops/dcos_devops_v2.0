from __future__ import unicode_literals

from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class DcosCluster(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    type = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    run_status = models.CharField(max_length=10)
    host_num = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    master_id = models.CharField(max_length=255, blank=True, null=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    step = models.CharField(max_length=255, blank=True, null=True)
    zk_str = models.CharField(max_length=255, blank=True, null=True)
    mesos_str = models.CharField(max_length=255, blank=True, null=True)
    marathon_str = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dcos_cluster'


class DcosHost(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    label = models.CharField(max_length=256, blank=True, null=True)
    ip_addr = models.CharField(unique=True, max_length=32)
    cpus = models.CharField(max_length=32, blank=True, null=True)
    mem = models.CharField(max_length=32, blank=True, null=True)
    disk = models.CharField(max_length=32, blank=True, null=True)
    remark = models.CharField(max_length=4000, blank=True, null=True)
    status = models.CharField(max_length=32)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField(blank=True, null=True)
    cls_id = models.CharField(max_length=255, blank=True, null=True)
    alive_containers = models.IntegerField(blank=True, null=True)
    stop_containers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dcos_host'
        unique_together = (('id', 'ip_addr'),)


class DcosHostServ(models.Model):
    host_id = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    port = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    v1 = models.CharField(max_length=255, blank=True, null=True)
    v2 = models.CharField(max_length=255, blank=True, null=True)
    v3 = models.CharField(max_length=255, blank=True, null=True)
    v4 = models.CharField(max_length=1024, blank=True, null=True)
    v5 = models.CharField(max_length=1024, blank=True, null=True)
    v6 = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dcos_host_serv'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class IcingaInfo(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=255, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'icinga_info'
