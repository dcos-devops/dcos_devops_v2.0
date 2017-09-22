# -*- coding: utf-8 -*-

from django.shortcuts import render
from db import db_init
from django.http import HttpResponse
import json


def index():
    sql_info = "SELECT DISTINCT LEVEL from icinga_info"
    levels = db_init.execute_sql(sql_info)
    return render('index.html', levels)


def get_ip(request):
    level = request.GET.get('level')
    sql_info = "SELECT DISTINCT ip from icinga_info WHERE LEVEL = '{}'".format(level)
    ip_raw = db_init.execute_sql(sql_info)
    ip_pool = []
    for ip in ip_raw:
        ip_pool.append(ip[0])
    ip_cooked = {"ip": ip_pool}
    return HttpResponse(json.dumps(ip_cooked), content_type='application/json')


def get_table_information(request):
    level = request.args.get('level')
    ip = request.args.get('ip')
    table_information = [('Time', 'IP', 'Service', 'Message')]
    sql_info = "SELECT time,ip,service,message FROM icinga_info WHERE ip = '{}' AND level = '{}'".format(ip, level)
    rest_information_raw = db_init.execute_sql(sql_info)
    for item in rest_information_raw:
        table_information.append(item)
    rest_information_cooked = {"information": table_information}
    return HttpResponse(json.dumps(rest_information_cooked),  content_type='application/json')
