# coding=utf-8
"""发送邮箱验证码"""

from django.core.mail import send_mail
from django.conf import settings

from celery_task.main import celery_app

# @celery_app.task(name='send_varify_email')
# 错误重试机制
"""
bind:设置为True时，表示task实例，
retry_backoff: 设置重置时间
"""
@celery_app.task(bind=True, name='send_verify_email', retry_backoff=3)
def send_varify_email(self,to_email, verify_url):
    """发送短信验证"""
    """
    subject：
    message,
    from_email,
    recipient_list,
    html_message=None"""
    
    subject = '美多商城邮箱验证'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(subject,'',settings.EMAIL_FROM, [to_email], html_message=html_message)
    except Exception as e:
        # 有异常自动重试三次
        # exc: 异常问题
        # max_retries 重试次数
        raise self.retry(exc=e,max_retries=3)