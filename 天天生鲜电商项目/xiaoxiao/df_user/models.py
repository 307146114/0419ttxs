from django.db import models

# Create your models here.
class UserInfo(models.Model):
    # 登录名
    username = models.CharField(max_length=20)
    # 登录密码
    password = models.CharField(max_length=40)
    # 注册填写邮箱
    email = models.CharField(max_length=40)
    # 收件人  注册时默认填写‘’
    name = models.CharField(max_length=20,default="")
    # 详细地址  注册时默认填写‘’
    adress = models.CharField(max_length=100,default="")
    # 邮编  注册时默认填写‘’
    youbian = models.CharField(max_length=6,default="")
    # 电话  注册时默认填写‘’
    tel = models.CharField(max_length=11,default="")
