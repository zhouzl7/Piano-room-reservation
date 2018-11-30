# _*_ coding: utf-8 _*_
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from PRmanage.models import Announcement
from django.core import serializers
import requests

def announcement(request):
    announceall = []
    announcements = Announcement.objects.all()
    for announcement in announcements:
        announceall.append({
            'title':announcement.title,
            'time':announcement.published_time,
            'author':announcement.published_person,
            'content':announcement.content
        })
    announceall.reverse()
    result = {
        'announce':announceall
    }
    return JsonResponse(result)

def onlogin(request):
    data = {
        'appid': 'wx77fa9e3e4014ff7a',
        'secret': '79e90ba6f0b6cab8b273cafd79fe1ba2',
        'grant_type': 'authorization_code',
    }
    data['js_code'] = request.GET['code']
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=data)
    result = {
        'openId' : r.json()['openid'] 
    }
    return JsonResponse(result)


