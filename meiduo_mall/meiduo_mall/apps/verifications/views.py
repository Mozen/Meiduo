from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden,JsonResponse
from django.views import View
from django_redis import get_redis_connection
import random, logging


from verifications.libs.captcha.captcha import captcha
from verifications.libs.yuntongxun.ccp_sms import CCP
from meiduo_mall.utils.response_code import RETCODE
from celery_task.sms.tasks import send_sms_code

# Create your views here.

logger = logging.getLogger('django')

class ImageCodeView(View):
    """二维码验证"""
    def get(self, request, uuid):
        # 获取响应参数，验证参数
        # 自动获取二维码数据
        
        text, image = captcha.generate_captcha()
        # 保存二维码内容到redis
        # 参数 'verify_code' 表示的是选择redis的几号库
        # 前面的配置中对应于验证码的数据，配置到2号库中，对应的字段名是 verify_code
        redis_connt = get_redis_connection('verify_code')
        redis_connt.setex(f"img_{uuid}", 3000, text)
        
        # 响应
        return HttpResponse(image, content_type='image/jpg')
    
    
class MessageCodeView(View):
    """短信验证码"""
    def get(self, request, mobile):
        # 获取响应数据
        # 手机号，图像验证码，uuid
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        
        if not all([image_code_client, uuid]):
            return HttpResponseForbidden('缺少必传参数')
        
        # 图像验证码验证
        redis_connt = get_redis_connection('verify_code')
        
        send_flag_mobile = redis_connt.get('send_flag_%s'%mobile)
        if send_flag_mobile:
            return JsonResponse({'code':RETCODE.THROTTLINGERR,'errmsg':'发送短信过于频繁'})
        
        # 获取redis中的图形验证码
        image_code_server = redis_connt.get('img_%s' % uuid)
        if image_code_server is None:
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图像验证码已失效'})
        # 删除redis中的验证码
        redis_connt.delete('img_%s' % uuid)
        # 对比验证码
        if image_code_client.lower() != image_code_server.decode().lower():
            return JsonResponse({'code':RETCODE.IMAGECODEERR,'errmsg':'图像验证码有误'})
        
        # 获取随机验证码
        random_num = '%06d'% random.randint(0,999999)
        logger.info(random_num)
        
        # # 保存验证码
        # redis_connt.setex('sms_%s' % mobile, 3000, random_num)
        # # 保存发送短信的时间
        # redis_connt.setex('send_flag_%s' % mobile, 60, 1)
        
        # 创建管道
        pl = redis_connt.pipeline()
        # 将 redis 请求添加到队列中
        pl.setex('sms_%s' % mobile, 300, random_num)
        # 保存发送短信的时间
        pl.setex('send_flag_%s' % mobile, 60, 1)
        # 执行管道队列
        pl.execute()

        # CCP().send_sms(mobile, [random_num, 5], 1)
        send_sms_code.delay(mobile, random_num)
        return JsonResponse({'code':RETCODE.OK, 'msg':'验证成功'})
    
    
    

