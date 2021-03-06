# coding=utf-8
from django.db import models

class BaseModel(models.Model):
    """基类model"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        abstract = True # abstract 抽象类, 用于继承使用, 数据库迁移时, 不会创建BaseModel表