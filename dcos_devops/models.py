from __future__ import unicode_literals

from django.db import models


class App(models.Model):
    appid = models.CharField(max_length=255)
    sys_name = models.CharField(max_length=255)
    module_name = models.CharField(max_length=255)
    cpu_allocate = models.IntegerField()
    mem_allocate = models.IntegerField()
    disk_allocate = models.IntegerField()
    container_num = models.IntegerField()
    auto_scale = models.IntegerField()
    cluster_name = models.CharField(max_length=255)
    create_time = models.DateTimeField()
    charger_name = models.CharField(max_length=255, blank=True, null=True)
    charger_tel = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.IntegerField()
    cluster_id = models.IntegerField()
    marathon_id = models.IntegerField()
    haproxy_id = models.IntegerField()
    zookeeper_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'app'


class Cluster(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cpu_total = models.CharField(max_length=255)
    mem_total = models.CharField(max_length=255)
    disk_total = models.CharField(max_length=255)
    field_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cluster'


class Component(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    host_ip = models.CharField(max_length=255)
    field_id = models.IntegerField()
    tag_name = models.CharField(max_length=255, blank=True, null=True)
    port = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'component'


class Container(models.Model):
    container_id = models.CharField(max_length=255)
    appid = models.CharField(max_length=255)
    host_ip = models.CharField(max_length=255)
    host_port = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'container'


class Field(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'field'


class Host(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    comp_name = models.CharField(max_length=255)
    cluster_id = models.IntegerField()
    comp_port = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'host'


class Programs(models.Model):
    name = models.CharField(max_length=255)
    host_ip = models.CharField(max_length=255)
    last_exec_time = models.DateTimeField()
    last_exec_user = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'programs'


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'role'


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    role_id = models.IntegerField()
    tel = models.CharField(max_length=255)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'


class Loginuser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __unicode__(self):
        return self.username
