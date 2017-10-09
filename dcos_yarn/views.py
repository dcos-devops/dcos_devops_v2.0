# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
import json
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def dcos_yarn(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        allocate_sql = "select * from dcos_yarn where type_info ='allocate' and time < now() and time > now() - 4m order by time desc limit 7;"
        col1, col2, col3, col4, col5 = "time", "dcos_cpu", "dcos_memory","yarn_cpu","yarn_memory"
        allocate_info = get_influxdb_info(allocate_sql, col1, col2, col3, col4, col5)
        print allocate_info
        used_sql = "select * from dcos_yarn where type_info ='used' and time < now() and time > now() - 4m order by time desc limit 7;"
        col1, col2, col3, col4, col5 = "time", "dcos_cpu", "dcos_memory","yarn_cpu","yarn_memory"
        used_info = get_influxdb_info(used_sql, col1, col2, col3, col4, col5)
        print used_info
        return render_to_response("dcos_yarn.html", {"allocate_info": allocate_info, "used_info": used_info})
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')


def query_influxdb(sql):
    client = InfluxDBClient("20.26.25.156", 8086, 'root', 'root', 'grafa')
    res = client.query(sql)
    return res


def get_influxdb_info(sql, col1, col2, col3, col4, col5):
    influxdb_info = {}
    print col1,col2,col3,col4,col5
    query_res = query_influxdb(sql)
    influxdb_info[col1], influxdb_info[col2], influxdb_info[col3], influxdb_info[col4], influxdb_info[col5] = [], [], [], [], []
    for i in query_res:
        for j in range(len(i)):
            print i[j][col1],i[j][col2],i[j][col3],i[j][col4],i[j][col5]
            influxdb_info[col1].insert(0, (datetime.strptime((i[j]["time"][:19]), "%Y-%m-%dT%H:%M:%S") + timedelta(hours=8)).strftime("%H:%M:%S")[0:5])
            influxdb_info[col2].insert(0, round(i[j][col2],3))
            if "used" in sql:
                influxdb_info[col3].insert(0, i[j][col3])
                influxdb_info[col5].insert(0, i[j][col5])
            else:
                influxdb_info[col3].insert(0, i[j][col3])
                influxdb_info[col5].insert(0, i[j][col5])
            influxdb_info[col4].insert(0, i[j][col4])
    json_influxdb_info = json.dumps(influxdb_info)
    return json_influxdb_info
