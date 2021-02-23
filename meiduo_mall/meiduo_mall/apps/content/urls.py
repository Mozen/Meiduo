from django.urls import re_path, path
from content.views import IndexView

app_name = 'content'
urlpatterns = [
    # 首页广告
    path('', IndexView.as_view(), name='index')
]