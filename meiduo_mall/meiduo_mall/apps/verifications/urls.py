from django.urls import path, re_path
from verifications.views import ImageCodeView, MessageCodeView


urlpatterns = [
    re_path(r'image_code/(?P<uuid>[\w-]+)/',ImageCodeView.as_view()),
    re_path(r'sms_code/(?P<mobile>1[0-9]{10})/',MessageCodeView.as_view()),
]