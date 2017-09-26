# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
import requests
import socket
import json


def get_mesos_leader(mesos_master_nodes):
    http_headers = { 'Accept': '*/*','Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
    for mmn in mesos_master_nodes:
        baseurl = None
        try:
            url = "http://{0}/redirect".format(mmn)
            rs = requests.get(url,headers=http_headers,timeout=10)
            baseurl = "http://" + socket.gethostbyname(rs.url.split("//")[1].split(":")[0]) + ":5050/"
        except Exception as e:
            print("failed to get url: {} ".format(url))
        if baseurl:
            break

    if baseurl is None:
        raise Exception
    return baseurl


def cluster_resource(request):

    zj01_name, mesos_master_name, new_x86_name = "中心化测试环境", "营业厅测试环境", "新X86测试环境"
    zj01_mesos_ips = ["20.26.25.11:5050", "20.26.25.12:5050", "20.26.25.13:5050"]
    mesos_master_ips = ["20.26.28.22:5050", "20.26.28.23:5050", "20.26.28.24:5050"]
    new_x86_name_ips = ["20.26.28.20:5050", "20.26.28.21:5050", "20.26.33.50:5050"]
    zj01_mesos_leader = get_mesos_leader(zj01_mesos_ips) + "master/state"
    mesos_master_leader = get_mesos_leader(mesos_master_ips) + "master/state"
    new_x86_leader = get_mesos_leader(new_x86_name_ips) + "master/state"

    zj01_resource = get_cluster_resource(zj01_mesos_leader)
    mesos_master_resource = get_cluster_resource(mesos_master_leader)
    new_x86_resource = get_cluster_resource(new_x86_leader)

    return render_to_response('get_cluster_resource.html', {"zj01_name": zj01_name,
                                                            "zj01_resource": zj01_resource,
                                                            "zj01_mesos_ips": ",".join(zj01_mesos_ips),
                                                            "mesos_master_name": mesos_master_name,
                                                            "mesos_master_resource": mesos_master_resource,
                                                            "mesos_master_ips": ",".join(mesos_master_ips),
                                                            "new_x86_name": new_x86_name,
                                                            "new_x86_resource": new_x86_resource,
                                                            "new_x86_name_ips": ",".join(new_x86_name_ips)})


def get_cluster_resource(url):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 6.1;Win64;x64)"
                      "AppleWebKit / 537.36(KHTML, likeGecko)"
                      "Chrome / 58.0.3029.110"
                      "Safari / 537.36",
    }
    html = requests.get(url=url, headers=headers).text
    jsonstr = json.loads(html)
    res, attributes_all, attributes_resources, left_resource_pec = {}, [], {}, {}

    for slave in jsonstr['slaves']:
        attributes = str(slave['attributes'])[1:-1].replace("u'", "").replace("'", "")
        if attributes not in attributes_all:
            attributes_all.append(attributes)
        resources = slave['resources']
        used_resources = slave['used_resources']
        cpus_left = resources['cpus'] - used_resources['cpus']
        mem_left = resources['mem'] - used_resources['mem']
        disk_left = resources['disk'] - used_resources['disk']
        ports_used = len(used_resources['ports'].split(',')) if 'ports' in used_resources.keys() else 0
        ports_tmp = resources['ports'].split('-')
        ports_total = int(ports_tmp[1][:-1]) - int(ports_tmp[0][1:])
        ports_left = ports_total - ports_used

        if attributes not in attributes_resources:
            attributes_resources[attributes] = {}
            attributes_resources[attributes]['cpus_left'] = cpus_left
            attributes_resources[attributes]['cpus_all'] = resources['cpus']
            attributes_resources[attributes]['mem_left'] = mem_left
            attributes_resources[attributes]['mem_all'] = resources['mem']
            attributes_resources[attributes]['disk_left'] = disk_left
            attributes_resources[attributes]['disk_all'] = resources['disk']
            attributes_resources[attributes]['ports_left'] = ports_left
            attributes_resources[attributes]['slave_num'] = 1
        else:
            attributes_resources[attributes]['cpus_left'] += cpus_left
            attributes_resources[attributes]['cpus_all'] += resources['cpus']
            attributes_resources[attributes]['mem_left'] += mem_left
            attributes_resources[attributes]['mem_all'] += resources['mem']
            attributes_resources[attributes]['disk_left'] += disk_left
            attributes_resources[attributes]['disk_all'] += resources['disk']
            attributes_resources[attributes]['ports_left'] += ports_left
            attributes_resources[attributes]['slave_num'] += 1

    for attribute in attributes_all:
        left_resource_pec[attribute] = {}
        left_resource_pec[attribute]['cpus_left_pec'] = round((attributes_resources[attribute]['cpus_left'] / attributes_resources[attribute]['cpus_all'] * 100), 2)
        left_resource_pec[attribute]['mem_left_pec'] = round((attributes_resources[attribute]['mem_left'] / attributes_resources[attribute]['mem_all'] * 100), 2)
        left_resource_pec[attribute]['disk_left_pec'] = round((attributes_resources[attribute]['disk_left'] / attributes_resources[attribute]['disk_all'] * 100), 2)

    for attribute in attributes_all:
        res[attribute] = []
        res[attribute].append(attributes_resources[attribute]['slave_num'])
        res[attribute].append(str(attributes_resources[attribute]['cpus_left'])+" ("+str(left_resource_pec[attribute]['cpus_left_pec'])+"%)")
        res[attribute].append(str(attributes_resources[attribute]['mem_left'])+" ("+str(left_resource_pec[attribute]['mem_left_pec'])+"%)")
        res[attribute].append(str(attributes_resources[attribute]['disk_left'])+" ("+str(left_resource_pec[attribute]['disk_left_pec'])+"%)")
        res[attribute].append(attributes_resources[attribute]['ports_left'])
    return res
