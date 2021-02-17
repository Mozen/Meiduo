from jinja2 import Environment
from django.urls import reverse
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage


def jinja2environment(**options):
    """jinja2 模板引擎环境变量补充"""
    # 创建环境变量
    env = Environment(**options)
    # 自定义语法 {{static('静态文件相对路径')}}{{url('路由的命名空间')}}
    env.globals.update({
        'static':staticfiles_storage, # 获取静态文件前缀
        'urls':reverse   # 重定向
    })
    
    return env
    
    