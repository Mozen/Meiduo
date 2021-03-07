# coding=utf-8
from django.shortcuts import render
from django.views import View
from django import http
from django.core.cache import cache

from address.models import AdressModel
from meiduo_mall.utils.response_code import RETCODE
# Create your views here.

class AddressView(View):
    """查询省市区地址
    查询地址分两种情况:
        1. 查询省份时，不需要参数 areas
        2. 查询市区时需要参数 areas
    """
    def get(self, request):
        # 获取参数
        area_id = request.GET.get('area_id')
        # 查询省份
        if not area_id:
            
            province_list = cache.get('province_list')
            
            if not province_list:
                # 是否在 cache里
                try:
                    # 根据父类的id是null, 查询出的结果是一个模型类，不是一个字典类型 需要转换
                    province_model_list = AdressModel.objects.filter(parent_id__isnull=True)
                    
                    province_list = []
                    for province_model in province_model_list:
                        province_id = province_model.id
                        province_name = province_model.name
                        province_list.append({'id':province_id, 'name':province_name})
                        
                    # 存储省份信息
                    cache.set('province_list', province_list, 3600)
                except Exception as e:
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份查询失败'})
                
            return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'OK', "province_list":province_list})
        else:
    
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                # 根据 areas(id) 查询 父类信息
                # 为什么要这样做呢？可以直接通过areas_id 查询所有的需要的数据啊?
                # 问题在于 需要返回父类信息，所以这里只能先查父类，然后通过父类在查询子类
                try:
                    parent_model = AdressModel.objects.get(id=area_id)
                    # 一对多查询方法
                    subs_model_list = parent_model.subs.all()
                    subs = []
                    for subs_model in subs_model_list:
                        subs_id = subs_model.id
                        subs_name = subs_model.name
                        subs.append({'id':subs_id, 'name':subs_name})
                        
                    sub_data = {'id': parent_model.id,
                                'name': parent_model.name,
                                'subs': subs}
                    # 存储省份信息
                    cache.set('sub_area_' + area_id, sub_data, 3600)
                except Exception as e:
                    return http.JsonResponse({'code':RETCODE.DBERR,'errmsg':'OK'})
                
            return http.JsonResponse({'code':RETCODE.OK,'errmsg':'OK','sub_data':sub_data})
            
    