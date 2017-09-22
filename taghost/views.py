# -*- coding: utf-8 -*-

from django.shortcuts import render
 
from dcos_devops.models import DcosCluster

def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'taghost/e.html', context)