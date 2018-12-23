from django.conf.urls import url
from . import views, cron

urlpatterns = [
    url(r'^announcement?$', views.announcement),
    url(r'^login', views.onlogin),
    url(r'^availableTime',views.availableTime),
    url(r'^reservation', views.reservation),
    url(r'^book', views.book),
    url(r'^room', views.room),
    url(r'^salt', views.salt),
    url(r'^pwlogin', views.pwLogin),
    url(r'^register', views.register),
    url(r'^isBind', views.isBind),
    url(r'^notBind', views.notBind),
    url(r'^bind?$', views.bindRedirect),
    url(r'^bindCampus?$', views.bindCampus),
]
