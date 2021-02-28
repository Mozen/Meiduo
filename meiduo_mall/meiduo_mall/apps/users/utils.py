# coding=utf-8
from django.contrib.auth.backends import ModelBackend
from users.models import User
import re

class UserLoginBackend(ModelBackend):
    """自定义用户登陆，实现手机账号同时登陆"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        # 验证用户使用的用户名
        try:
            if re.match(r'1[3-9]\d{9}', username):
                # username 是手机号
                user = User.objects.get(mobile=username)
            else:
                # username 是用户名
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            else:
                return None
        
        
        
        