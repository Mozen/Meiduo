import celery

# 创建 celery 对象
celery_app = celery.Celery('meiduo')

# # 添加配置文件
celery_app.config_from_object('celery_task.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_task.sms'])


