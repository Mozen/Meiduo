from django.urls import re_path

from users import views

app_name = 'users'
urlpatterns = [
    # 用户注册路由
    re_path('register/', views.ResgisterView.as_view(), name='register'),
    # 用户名验证是否存在路由,这里可以直接获得用户名,并传递给视图函数get
    # 使用?P<username> 可以直接把参数传递到get中
    re_path(r'username/(?P<username>[a-zA-Z0-9_-]{5,20})/count/', views.UsernameCountView.as_view()),
    # 手机号验证
    re_path(r'mobile/(?P<mobile>1[0-9]{10})/count',views.MobileCountView.as_view()),
    # 用户登陆视图
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    # 用户推出登陆
    re_path(r'^logout/$', views.LoginView.as_view(), name='logout')
]