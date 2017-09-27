# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dcos_devops.settings")# project_name 项目名称
django.setup()
from views import search_cluster

# Create your tests here.

search_cluster()
