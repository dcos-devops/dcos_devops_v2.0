"""dcos_devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import view as login_views
from alertinfos import views as alert_info_views
from resourceremain import views as resource_remain_views
from dcos_yarn import views as dcos_yarn_views
from show_host import views as show_host_views

urlpatterns = [
    url(r'^$', login_views.hello),
    url(r'^login', login_views.login),
    url(r'^index', alert_info_views.index),
    url(r'^get_ip', alert_info_views.get_ip),
    url(r'^get_rest_information', alert_info_views.get_table_information),
    url(r'^get_service_time', alert_info_views.get_service_time),
    url(r'^cluster_resource', resource_remain_views.cluster_resource),
    url(r'^dcos_yarn', dcos_yarn_views.dcos_yarn),
    url(r'^show_host', show_host_views.search_field),
    url(r'^search_field', show_host_views.get_field),
    url(r'^get_cluster', show_host_views.search_cluster),
    url(r'^get_host_info', show_host_views.search_host),
    url(r'^get_component', show_host_views.search_component),
    url(r'^search_host_info', show_host_views.search_host_info),
    url(r'^del_host_logfile', show_host_views.dellog),
    url(r'^empty_host_logfile', show_host_views.emplog),
    url(r'^search_host_logfile', show_host_views.showlog),
    url(r'^search_host_exitdocker', show_host_views.showexitdocker),
    url(r'^del_host_docker', show_host_views.delexitdocker),
    url(r'^clean_exit_dockers', show_host_views.delexitdockers),
    url(r'^logout', login_views.logout),
    url(r'^add_host', show_host_views.addhost),
    url(r'^check_ip', show_host_views.checkip),
]
