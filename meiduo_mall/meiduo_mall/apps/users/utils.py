# coding=utf-8
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
import re

from users.models import User
from . import constants_users
import logging

logger = logging.getLogger('django')


def verify_email_url(token):
    """通过前端数据 token 获取 user_id 最终获取 user"""
    # 初始化序列化
    s = serializer(settings.SECRET_KEY, constants_users.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = s.loads(token)
    except Exception as e:
        return None
    user_id = data.get('user_id')
    email = data.get('email')
    try:
        user = User.objects.get(id=user_id, email=email)
    except Exception as e:
        logger.error('获取用户失败')
        return None
    
    return user
        

def get_email_verify_url(user):
    """生成邮箱激活链接"""
    # 初始化序列化
    s = serializer(settings.SECRET_KEY, constants_users.VERIFY_EMAIL_TOKEN_EXPIRES)
    # 需要序列化的数据(user 当前登陆账户的信息)
    data = {'user_id':user.id, 'email':user.email}
    # 序列化数据
    token = s.dumps(data).decode()
    # 生成token_url
    token_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return token_url
    

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
        
        
        
        