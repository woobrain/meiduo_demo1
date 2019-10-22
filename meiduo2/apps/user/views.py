import json
import re

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from apps.user.models import User
from apps.user.utils import get_token
from utils.response_code import RETCODE


class Register(View):
    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        pwd2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        if not all([username, pwd, pwd2, mobile]):
            return HttpResponseBadRequest('有空白参数')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseBadRequest('用户名不符合规则')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', pwd):
            return HttpResponseBadRequest('密码不符合规则')
        if not re.match(r'^1[345789]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号不符合规则')
        if pwd != pwd2:
            return HttpResponseBadRequest('密码不一致')
        redis_conn = get_redis_connection('code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return JsonResponse({'sms_code_errmsg': '无效的短信验证码'})
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'sms_code_errmsg': '输入短信验证码有误'})
        # 使用authenticate时,必须要使用create_user()创建密码加密的用户
        User.objects.create_user(username=username, password=pwd, mobile=mobile)
        response = redirect(reverse('login1:index'))
        response.set_cookie('username', username, 3600)
        return response


class UsernameView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({"count": count})


class UsermobileView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({"count": count})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        allow = request.POST.get('remembered')
        if not all([username, password]):
            return HttpResponseBadRequest('缺少参数')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseBadRequest('用户名不符合规则')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('密码不符合规则')
        from django.contrib.auth import authenticate
        # 认证成功返回User对象
        # 认证失败返回None
        from django.contrib.auth.backends import ModelBackend
        # mobile = re.match(r'^1[3-9]\d{9}$',username).group()
        # username = User.objects.get(mobile=mobile).username
        user1 = authenticate(username=username, password=password)
        if user1 is None:
            return HttpResponseBadRequest("用户名或者密码不匹配")
        login(request, user1)

        if allow:
            # 默认两周
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        response = redirect(reverse('login1:index'))
        response.set_cookie('username', username, 3600)
        return response


class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect(reverse('login1:index'))
        response.delete_cookie('username')
        return response


class UserVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "username": request.user.username,
            "mobile": request.user.mobile,
            "email": request.user.email,
            "email_active": request.user.email_active,
        }

        return render(request, 'user_center_info.html', context=context)


class EmailsView(LoginRequiredMixin, View):
    def put(self, request):
        # username = request.user.username
        # mobile = request.user.
        # username = request.user.username
        body_str = request.body.decode()
        data = json.loads(body_str)
        email = data.get('email')
        if email is None:
            return JsonResponse({"code": RETCODE.EMAILERR, "errmsg": "邮箱不能为空"})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({"code": RETCODE.EMAILERR, "errmsg": "邮箱格式不正确"})
        request.user.email = email
        request.user.save()
        # from django.core.mail import send_mail
        # subject='美多测试'
        # message=''
        # from_email='管理员<15893775982@163.com>'
        # recipient_list=['15893775982@163.com']
        # html_message="<a href='http://www.meiduo.site:8000/emails/?token=1'>这是一个标签</a>"
        # send_mail(subject=subject,
        #           message=message,
        #           from_email=from_email,
        #           recipient_list=recipient_list,
        #           html_message=html_message)
        from celery_tasks.emails.tasks import send_active_email
        send_active_email.delay(request.user.id, email)
        return JsonResponse({"code": RETCODE.OK, "errmsg": "发送成功"})


class EmailsActiveView(View):
    def get(self, request):
        token_id = request.GET.get('token')
        # id = request.GET.get('id')
        # email = request.GET.get('email')
        if token_id is None:
            return HttpResponseBadRequest('激活失败')
        data = get_token(token_id)
        try:
            user = User.objects.get(id=data.get('id'),email=data.get('email'))
        except Exception as e:
            return HttpResponseBadRequest('验证失败')

        user.email_active = True
        user.save()

        # user = User.objects.update(email_active=True)

        return redirect(reverse('user:center'))