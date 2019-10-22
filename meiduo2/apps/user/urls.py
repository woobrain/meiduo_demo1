from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^register/$',views.Register.as_view(),name='register'),
    url(r'^login/$',views.LoginView.as_view(),name='login'),
    url(r'^logout/$',views.LogoutView.as_view(),name='logout'),
    url(r'^emails/$',views.EmailsView.as_view(),name='emails'),
    url(r'^emailsactive/',views.EmailsActiveView.as_view(),name='emailsactive'),
    url(r'^center/$',views.UserVerifyView.as_view(),name='center'),
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/$',views.UsernameView.as_view(),name='username'),
    url(r'^mobile/(?P<mobile>1[345789]\d{9})/$',views.UsermobileView.as_view(),name='mobile'),
]