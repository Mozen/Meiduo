# coding=utf-8
from django.urls import re_path
from . import views

urlpatterns = [
    # 省市区 地址
    re_path(r'areas/',views.AddressView.as_view()),
]