# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
import json
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def dcos_yarn(request):
    dcos_cpu_mem_allocate_sql = "select * from dcos_yarn where type_info ='dcos' and time < now() and time > now() - 14m order by time desc;"
    dcos_cpu_mem_allocate_col1, dcos_cpu_mem_allocate_col2, dcos_cpu_mem_allocate_col3 = "time_line", "allocate_cpu", "allocate_mem"
    dcos_cpu_mem_allocate_info = get_influxdb_info(dcos_cpu_mem_allocate_sql, dcos_cpu_mem_allocate_col1, dcos_cpu_mem_allocate_col2, dcos_cpu_mem_allocate_col3)

    yarn_cpu_mem_allocate_sql = "select * from dcos_yarn where type_info ='yarn' and time < now() and time > now() - 14m order by time desc;"
    yarn_cpu_mem_allocate_col1, yarn_cpu_mem_allocate_col2, yarn_cpu_mem_allocate_col3 = "time_line", "allocate_cpu", "allocate_mem"
    yarn_cpu_mem_allocate_info = get_influxdb_info(yarn_cpu_mem_allocate_sql, yarn_cpu_mem_allocate_col1, yarn_cpu_mem_allocate_col2, yarn_cpu_mem_allocate_col3)

    dcos_cpu_mem_used_sql = "select * from dcos_yarn_used where type_info ='dcos' and time < now() and time > now() - 14m order by time desc;"
    dcos_cpu_mem_used_col1, dcos_cpu_mem_used_col2, dcos_cpu_mem_used_col3 = "time_line", "used_cpu", "used_memory"
    dcos_cpu_mem_used_info = get_influxdb_info(dcos_cpu_mem_used_sql, dcos_cpu_mem_used_col1, dcos_cpu_mem_used_col2, dcos_cpu_mem_used_col3)

    yarn_cpu_mem_used_sql = "select * from dcos_yarn_used where type_info ='yarn' and time < now() and time > now() - 14m order by time desc;"
    yarn_cpu_mem_used_col1, yarn_cpu_mem_used_col2, yarn_cpu_mem_used_col3 = "time_line", "used_cpu", "used_memory"
    yarn_cpu_mem_used_info = get_influxdb_info(yarn_cpu_mem_used_sql, yarn_cpu_mem_used_col1, yarn_cpu_mem_used_col2, yarn_cpu_mem_used_col3)
    return render_to_response("dcos_yarn.html", {"dcos_cpu_mem_allocate_info": dcos_cpu_mem_allocate_info,
                                                 "yarn_cpu_mem_allocate_info": yarn_cpu_mem_allocate_info,
                                                 "dcos_cpu_mem_used_info": dcos_cpu_mem_used_info,
                                                 "yarn_cpu_mem_used_info": yarn_cpu_mem_used_info})


def query_influxdb(sql):
    client = InfluxDBClient("20.26.25.156", 8086, 'root', 'root', 'grafa')
    res = client.query(sql)
    return res


def get_influxdb_info(sql, col1, col2, col3):
    influxdb_info = {}
    query_res = query_influxdb(sql)
    influxdb_info[col1], influxdb_info[col2], influxdb_info[col3] = [], [], []
    for i in query_res:
        for j in range(len(i)):
            influxdb_info[col1].insert(0, (datetime.strptime((i[j]["time"][:19]), "%Y-%m-%dT%H:%M:%S") + timedelta(hours=8)).strftime("%H:%M:%S")[0:5])
            influxdb_info[col2].insert(0, i[j][col2])
            influxdb_info[col3].insert(0, round(i[j][col3]/1024, 2))
    json_influxdb_info = json.dumps(influxdb_info)
    return json_influxdb_info
