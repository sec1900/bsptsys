from django.db import models
from django.contrib.auth.models import User
from django_celery_results import models as celecy_models
from django.utils import timezone
# Create your models here.

# 用户任务队列表, 把用户与任务进行关联
class UserTask(models.Model):
    # 自增序号
    userTask_id = models.AutoField('关联序号', primary_key=True)
    # 以外键的形式绑定用户的ID
    userTask_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户ID')
    # 以外键的形式绑定任务的ID
    userTask_task = models.ForeignKey(celecy_models.TaskResult, on_delete=models.CASCADE, default='', verbose_name='任务ID')
    # 任务开始时间
    date_start = models.DateTimeField('任务开始时间', default=timezone.now)
