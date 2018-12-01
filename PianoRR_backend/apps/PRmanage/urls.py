from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^announcement?$', views.announcement),
    url(r'^login', views.onlogin),
    url(r'^availableTime',views.availableTime),
    url(r'^reservation', views.reservation)
]
