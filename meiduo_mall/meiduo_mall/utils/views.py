# coding=utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

from meiduo_mall.utils.response_code import RETCODE


class LoginRequiredJsonMixin(LoginRequiredMixin):
    """重写判断用户是否登陆返回结果"""
    # 这里只做了未登录返回的原因?
    # 这里是继承了 LoginRequiredMixin, 用户是否登陆是由父类判断
    # 如果未登录,这使用子类重写的方法
    def handle_no_permission(self):
        return http.JsonResponse({'code':RETCODE.SESSIONERR, 'errmsg':'用户未登录'})