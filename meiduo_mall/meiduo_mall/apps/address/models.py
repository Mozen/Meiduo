# coding=utf-8
from django.db import models



# Create your models here.

class AdressModel(models.Model): # Areas  区域地址
    """省市区 区域模型 model"""
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name='subs')
    objects = models.Manager()
    
    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
    
    def __str__(self):
        return self.name
    

    
