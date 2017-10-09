# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from db import db_init
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def index(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        sql_info = "SELECT DISTINCT LEVEL from icinga_info"
        levels = db_init.execute_sql(sql_info)
        return render_to_response('index.html', {"levels": levels})
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')


def get_ip(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        level = request.GET.get('level')
        sql_info = "SELECT DISTINCT ip from icinga_info WHERE LEVEL = '{}'".format(level)
        ip_raw = db_init.execute_sql(sql_info)
        ip_pool = []
        for ip in ip_raw:
            ip_pool.append(ip[0])
        ip_cooked = {"ip": ip_pool}
        return HttpResponse(json.dumps(ip_cooked), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')
        


def get_table_information(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        level = request.GET.get('level')
        ip = request.GET.get('ip')
        table_information = [('Time', 'IP', 'Service', 'Message')]
        sql_info = "SELECT time,ip,service,message FROM icinga_info WHERE ip = '{}' AND level = '{}'".format(ip, level)
        rest_information_raw = db_init.execute_sql(sql_info)
        for item in rest_information_raw:
            table_info = (item[0].strftime('%Y-%m-%d %H:%M:%S'), item[1], item[2], item[3])
            table_information.append(table_info)
        rest_information_cooked = {"information": table_information}
        return HttpResponse(json.dumps(rest_information_cooked), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')


def get_service_time(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        level = request.GET.get('level')
        ip = request.GET.get('ip')
        sql_info = "select service, count(*) from icinga_info where ip='{}' and level='{}' GROUP BY service;".format(ip, level)
        service_time, service_name = [], []
        d = []
        service_information_raw = db_init.execute_sql(sql_info)
        for item in service_information_raw:
            a = {}
            a['value']=item[1]
            a['name'] = item[0]
            d.append(a)
            service_name.append(item[0])
            service_time.append((item[1]))
        #print(service_name,service_time)
        service_information = {"service_name": service_name, "service_time": service_time, "d": d}
        return HttpResponse(json.dumps(service_information), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')