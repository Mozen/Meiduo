# coding=utf-8
from celery_task.sms.yuntongxun.ccp_sms import CCP
from celery_task.main import celery_app

@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, random_num):
    """异步发送短信验证码"""
    res = CCP().send_sms(mobile, [random_num, 5], 1)
    return res