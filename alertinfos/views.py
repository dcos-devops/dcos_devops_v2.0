# -*- coding: utf-8 -*-

from django.shortcuts import render
 
def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'alertinfos/a.html', context)
