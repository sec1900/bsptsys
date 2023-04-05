from django.db import models


# 导航栏表
class Navigation(models.Model):
    nav_id = models.AutoField('导航序号', primary_key=True)
    nav_name = models.CharField('导航名称', max_length=20)
    nav_link = models.CharField('导航链接', max_length=50, default='/')

    def __str__(self):
        return self.nav_name

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '导航栏'
        verbose_name_plural = '导航栏'


# 脚本分类表
class Label(models.Model):
    label_id = models.AutoField('脚本类别序号', primary_key=True)
    label_name = models.CharField('脚本类别名称', max_length=20)
    label_path = models.CharField('脚本类别文件夹位置', max_length=50, default='null')

    def __str__(self):
        return self.label_name

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '脚本分类'
        verbose_name_plural = '脚本分类'


# 脚本文件
class Script(models.Model):
    script_id = models.AutoField('脚本序号', primary_key=True)
    script_name = models.CharField('脚本名称', max_length=50)
    script_file = models.CharField('脚本文件地址', max_length=50)
    script_label = models.ForeignKey(Label, on_delete=models.CASCADE, verbose_name='脚本分类')

    def __str__(self):
        return self.script_name

    class Meta:
        # 设置Admin界面的显示内容
        verbose_name = '脚本'
        verbose_name_plural = '脚本'
