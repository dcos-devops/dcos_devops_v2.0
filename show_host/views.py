# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from dcos_devops.models import Host, Field, Cluster
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.db.models import Q
import log_operation
import docker_operation

def checkip(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        ip = request.GET.get("ip")

        host_query_res = Host.objects.filter(ip=ip)
        if len(host_query_res)==0:
            error='new'
            status=0
            checkres={'status':status,'error':error}
        else:
            cluster_id=host_query_res[0].cluster_id
            name=host_query_res[0].name
            cluster0 = Cluster.objects.filter(id=cluster_id)[0]
            cluster=cluster0.name
            field_id=cluster0.field_id
            field=Field.objects.filter(id=field_id)[0].name
            error='old'
            status=1
            checkres={'status':status,'error':error,'field':field,'cluster':cluster,'name':name,'ip':ip}
        check_info_res = {"checkres": checkres}
        return HttpResponse(json.dumps(check_info_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def addhost(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        field = request.GET.get("field")
        cluster = request.GET.get("cluster")
        name = request.GET.get("name")
        ip = request.GET.get("ip")
        comp_name = request.GET.get("comp_name")
        comp_port = request.GET.get("comp_port")

        host_query_res = Host.objects.filter(ip=ip)
        if len(host_query_res)==0:
            status=1
            field_id = Field.objects.filter(name=field)[0].id
            cluster_id = Cluster.objects.filter(name=cluster,field_id=field_id)[0].id
            newhost=Host(name=name,ip=ip,cluster_id=cluster_id,comp_port=comp_port,comp_name=comp_name)
            saveres=newhost.save()
            addres={'status':status,'saveres':saveres}
            add_info_res = {"addres": addres}
            return HttpResponse(json.dumps(add_info_res), content_type='application/json')
        else:
            field_id = Field.objects.filter(name=field)[0].id
            cluster_id = Cluster.objects.filter(name=cluster,field_id=field_id)[0].id
            host_query_res = Host.objects.filter(ip=ip,cluster_id=cluster_id,name=name)
            if len(host_query_res)==0:
                status=0
                error='该主机IP已经存在于其他集群，或该主机名和主机IP不对应'
            else:
                host_query_res = Host.objects.filter(ip=ip,comp_port=comp_port)
                if len(host_query_res)!=0:
                    status=0
                    error='该主机端口已经被其他组件占用！'
                else:
                    status=1
                    newhost=Host(name=name,ip=ip,cluster_id=cluster_id,comp_port=comp_port,comp_name=comp_name)
                    saveres=newhost.save()
                    addres={'status':status,'saveres':saveres}
                    add_info_res = {"addres": addres}
                    return HttpResponse(json.dumps(add_info_res), content_type='application/json')
        addres={'status':status,'error':error}
        add_info_res = {"addres": addres}
        return HttpResponse(json.dumps(add_info_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def delexitdockers(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        # hostip = request.GET.get("hostip")
        #TODO
        # get the password from the db.and not use the root.
        hostip = '20.26.33.32'
        password = '20172Epc'
        port = 22
        username = 'root'
        delres=docker_operation.del_dockers(hostip, port, username, password)
        docker_info_res = {"delres": delres}
        return HttpResponse(json.dumps(docker_info_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def delexitdocker(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        # hostip = request.GET.get("hostip")
        dockerid = request.GET.get("dockerid")
        hostip = '20.26.33.32'
        password = '20172Epc'
        port = 22
        username = 'root'
        delres=docker_operation.del_docker(hostip, port, username, password, dockerid)
        docker_info_res = {"delres": delres}
        return HttpResponse(json.dumps(docker_info_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def showexitdocker(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        # hostip = request.GET.get("hostip")
        hostip = '20.26.33.32'
        password = '20172Epc'
        port = 22
        username = 'root'
        dockers=docker_operation.show_exit_docker(hostip, port, username, password)
        docker_infos=[]
        for item in dockers:
            docker_infos.append({"ID": item['ID'],"IMAGE": item['IMAGE'],"CREATED": item['CREATED'],"STATUS": item['STATUS']})
        docker_info_res = {"docker_infos": docker_infos}
        return HttpResponse(json.dumps(docker_info_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def emplog(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        filename = request.GET.get("filename")
        # hostip = request.GET.get("hostip")
        hostip = '20.26.33.32'
        password = '20172Epc'
        port = 22
        username = 'root'
        text=log_operation.empty_log(hostip, port, username, password, filename)
        empres = {"empres": text}
        return HttpResponse(json.dumps(empres), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def dellog(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        filename = request.GET.get("filename")
        # hostip = request.GET.get("hostip")
        hostip = '20.26.33.32'
        password = '20172Epc'
        port = 22
        username = 'root'
        text=log_operation.del_log(hostip, port, username, password, filename)
        delres = {"delres": text}
        return HttpResponse(json.dumps(delres), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def showlog(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        # hostip = request.GET.get("hostip")
        hostip = '20.26.33.32'
        password = '20172Epc'
        port = 22
        username = 'root'
        execmd = "du -m /data/logs/*/*  | sort -nr | head -n 10"
        logfiles=log_operation.show_log(hostip, port, username, password, execmd)
        file_infos=[]
        for item in logfiles:
            file_infos.append({"size": item['size'],"filename": item['filename']})
        file_info_res = {"file_infos": file_infos}
        return HttpResponse(json.dumps(file_info_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')


def search_field(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        fields = []
        fields_query_res = Field.objects.all()
        for item in fields_query_res:
            fields.append(item.name)
        return render_to_response("show_host.html", {"fields": fields})
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def get_field(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        fields = []
        fields_query_res = Field.objects.all()
        for item in fields_query_res:
            fields.append(item.name)
        fields_res = {"fields": fields}
        return HttpResponse(json.dumps(fields_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def search_component(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        components = []
        components_query_res = Host.objects.values('comp_name').distinct()
        for item in components_query_res:
            components.append(item['comp_name'])
        components_res = {"components": components}
        return HttpResponse(json.dumps(components_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

def search_cluster(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        clusters = []
        field = request.GET.get("field")
        field_id = Field.objects.filter(name=field)[0].id
        clusters_query_res = Cluster.objects.filter(field_id=field_id)
        for item in clusters_query_res:
            clusters.append(item.name)
        clusters_res = {"clusters": clusters}
        return HttpResponse(json.dumps(clusters_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')


def search_host(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        host_info = []
        cluster = request.GET.get("cluster")
        field = request.GET.get("field")
        if cluster != "--- 请选择集群约束 ---" and field != "--- 请选择生产域 ---":
            cluster_id = Cluster.objects.filter(name=cluster)[0].id
            host_query_res = Host.objects.filter(cluster_id=cluster_id)
            for item in host_query_res:
                host_info.append({"field": field, "cluster": cluster, "name": item.name, "ip": item.ip, "comp_name": item.comp_name, "comp_port": item.comp_port})
        elif cluster == "--- 请选择集群约束 ---" and field != "--- 请选择生产域 ---":
            field_id = Field.objects.filter(name=field)[0].id
            cluster_objs = Cluster.objects.filter(field_id=field_id)
            for item in cluster_objs:
                host_info_res = [host_obj for host_obj in Host.objects.filter(cluster_id=item.id)]
                for info in host_info_res:
                    host_info.append({"field": field, "cluster": item.name, "name": info.name, "ip": info.ip, "comp_name": info.comp_name, "comp_port": info.comp_port})
        host_info_res = {"host_info": host_info}
        return HttpResponse(json.dumps(host_info_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')


def search_host_info(request):
    is_login = request.session.get('IS_LOGIN', False)
    if is_login:
        host_info = []
        cluster = request.GET.get("cluster")
        field = request.GET.get("field")
        if cluster != "--- 请选择集群约束 ---" and field != "--- 请选择生产域 ---":
            cluster_id = Cluster.objects.filter(name=cluster)[0].id
            search_info = request.GET.get("search_info")
            search_info_res = Host.objects.filter(
                Q(name__contains=search_info) | Q(ip__contains=search_info) | Q(comp_name__contains=search_info) | Q(comp_port__contains=search_info),
                cluster_id=cluster_id)
            for item in search_info_res:
                host_info.append({"field": field, "cluster": cluster, "name": item.name, "ip": item.ip, "comp_name": item.comp_name, "comp_port": item.comp_port})
        elif cluster == "--- 请选择集群约束 ---" and field != "--- 请选择生产域 ---":
            field_id3 = Field.objects.filter(name=field)[0].id
            search_info = request.GET.get("search_info")
            cluster_objs = Cluster.objects.filter(field_id=field_id3)
            for item in cluster_objs:
                search_info_res = [host_obj for host_obj in Host.objects.filter(
                    Q(name__contains=search_info) | Q(ip__contains=search_info) | Q(comp_name__contains=search_info) | Q(
                        comp_port__contains=search_info), cluster_id=item.id)]
                for info in search_info_res:
                    host_info.append({"field": field, "cluster": item.name, "name": info.name, "ip": info.ip, "comp_name": info.comp_name, "comp_port": info.comp_port})
        else:
            search_info = request.GET.get("search_info")
            search_info_res = Host.objects.filter(
                Q(name__contains=search_info) | Q(ip__contains=search_info) | Q(comp_name__contains=search_info) | Q(comp_port__contains=search_info))
            for item in search_info_res:
                cluster_id2 = item.cluster_id
                cluster_obj = Cluster.objects.filter(id=cluster_id2)[0]
                field_id2 = cluster_obj.field_id
                cluster2 = cluster_obj.name
                field2 = Field.objects.filter(id=field_id2)[0].name
                host_info.append({"field": field2, "cluster": cluster2, "name": item.name, "ip": item.ip, "comp_name": item.comp_name, "comp_port": item.comp_port})
        host_info_res = {"host_info": host_info}
        return HttpResponse(json.dumps(host_info_res), content_type='application/json')
    else:
        response = HttpResponseRedirect('/')
        return render(request, 'login.html')

