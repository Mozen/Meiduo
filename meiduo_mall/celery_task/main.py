import celery


# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'
    
# 创建 celery 对象
celery_app = celery.Celery('meiduo')

# # 添加配置文件
celery_app.config_from_object('celery_task.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_task.sms', 'celery_task.send_email'])


