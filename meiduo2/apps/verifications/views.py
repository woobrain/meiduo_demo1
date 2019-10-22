import random

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render
from libs.captcha.captcha import captcha
# Create your views here.
from django.views import View
from django_redis import get_redis_connection
import logging
from libs.yuntongxun.sms import CCP

logger = logging.getLogger()
# 图片验证码
class ImageVerify(View):
    def get(self, request, uuid):
        text, image = captcha.generate_captcha()

        redis_con = get_redis_connection('code')

        # redis_con.setex(key, time, value)
        redis_con.setex('img_%s' % uuid, 120, text)

        return HttpResponse(image, content_type='image/jpeg')


class SmsVerify(View):

    def get(self,request,mobile):
        from utils.response_code import RETCODE
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        if not all([image_code, uuid]):
            return JsonResponse({"code":RETCODE.IMAGECODEERR,"errmsg":"参数不能为空"})
        redis_con = get_redis_connection('code')
        i_mobile = redis_con.get("flag_%s"%mobile)
        if i_mobile:
            return JsonResponse({"code":RETCODE.OKO,"errmsg":"请勿频繁注册"})
        i_code = redis_con.get("img_%s" % uuid)
        i_code = i_code.decode()

        if i_code is None:
            return JsonResponse({"code":RETCODE.IMAGECODEERR,"errmsg":"验证码已经失效"})
        try:
            redis_con.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)
        if i_code.lower() != image_code.lower():
            return JsonResponse({"code":RETCODE.IMAGECODEERR,"errmsg":"图形验证码不正确"})
        random_code = '%06d'% random.randint(0,999999)
        redis_con.setex("sms_%s" % mobile,200,random_code)
        redis_con.setex("flag_%s" % mobile,200,1)
        from celery_tasks.sms.tasks import sms_send
        sms_send.delay(mobile,random_code)
        # CCP().send_template_sms(mobile, [random_code, 2], 1)
        return JsonResponse({"code":RETCODE.OK,"errmsg":"消息发送成功"})
