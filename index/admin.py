from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_title = '基于B/S的安全检测工具共享平台'
admin.site.site_header = '基于B/S的安全检测工具共享平台'

admin.site.register(Label)
admin.site.register(Navigation)
admin.site.register(Script)
