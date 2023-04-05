from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 获取settings.py的配置信息
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Beta.settings')
# 定义Celery对象，并将项目配置信息加载到对象中。
# Celery的参数一般以为项目名命名
app = Celery('Beta')
app.config_from_object('django.conf:settings', namespace='CELERY')
# 自动发现每个app下的tasks.py
app.autodiscover_tasks()
