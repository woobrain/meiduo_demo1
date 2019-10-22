"""meiduo2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse

#
# def t1(request):
#     import logging
#     logger = logging.getLogger('django')
#     try:
#         pass
#     except Exception as e:
#         logger.info(e)
#         logger.error(e)


    #
    # return HttpResponse('1111')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^t1', t1)
    url(r'', include('apps.user.urls',namespace='user')),
    url(r'', include('apps.login1.urls',namespace='login1')),

    url(r'', include('apps.verifications.urls',namespace='renzheng')),

]
