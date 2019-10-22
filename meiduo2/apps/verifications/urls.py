from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^t1', t1)
    # url(r'^image_codes/(?P<image>[\w-]+)/$', views.ImageVerify.as_view(),name='image'),
    # url(r'^/image_codes/(?P<uuid>[\w-]+)/', views.ImageVerify.as_view(),name='uuid'),
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageVerify.as_view(), name='uuid'),
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsVerify.as_view(), name='code'),

]
