# coding=utf-8
from django.urls import re_path
from oauth import views

urlpatterns = [
    #
    re_path(r'qq/login/', views.QQLoaderView.as_view(), name='qqlogin'),
    # 回调路由
    re_path(r'oauth_callback/', views.QQAuthUserView.as_view(), name='qqlogin'),
]