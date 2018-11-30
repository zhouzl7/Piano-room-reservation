# _*_ coding: utf-8 _*_
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from PRmanage.models import Announcement,PianoRoom,TimeTable
from BOOKmanage.models import BookRecord
from USERmanage.models import User,UserGroup
from django.core import serializers
import requests
from PianoRR_backend.settings import WECHAT_SECRET, WECHAT_APPID

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
        'appid': WECHAT_APPID,
        'secret': WECHAT_SECRET,
        'grant_type': 'authorization_code',
    }
    data['js_code'] = request.GET['code']
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=data)
    result = {
        'openId' : r.json()['openid'] 
    }
    return JsonResponse(result)

def availableTime(request):
    openId = request.GET['openId']
    user = User.objects.filter(open_id = openId).first()
    PianoRoomLists = PianoRoom.objects.all()
    dateToday =[]
    dateTomorrow = []
    dateAfter_Tomorow = []
    for room in PianoRoomLists:
        dateTodayi = TimeTable.objects.filter(piano_room=room,date=0).first()
        if(dateTodayi.Time1 == 1):
            time1 = 'false'
        else:
            time1 = 'true'
        if(dateTodayi.Time2 == 1):
            time2 = 'false'
        else:
            time2 = 'true'
        if(dateTodayi.Time3 == 1):
            time3 = 'false'
        else:
            time3 = 'true'
        if(dateTodayi.Time4 == 1):
            time4 = 'false'
        else:
            time4 = 'true'
        if(dateTodayi.Time5 == 1):
            time5 = 'false'
        else:
            time5 = 'true'
        if(dateTodayi.Time6 == 1):
            time6 = 'false'
        else:
            time6 = 'true'
        if(dateTodayi.Time7 == 1):
            time7 = 'false'
        else:
            time7 = 'true'
        if(dateTodayi.Time8 == 1):
            time8 = 'false'
        else:
            time8 = 'true'
        if(dateTodayi.Time9 == 1):
            time9 = 'false'
        else:
            time9 = 'true'
        if(dateTodayi.Time10 == 1):
            time10 = 'false'
        else:
            time10 = 'true'
        if(dateTodayi.Time11 == 1):
            time11 = 'false'
        else:
            time11 = 'true'
        if(dateTodayi.Time12 == 1):
            time12 = 'false'
        else:
            time12 = 'true'
        if(dateTodayi.Time13 == 1):
            time13 = 'false'
        else:
            time13 = 'true'
        if(dateTodayi.Time14 == 1):
            time14 = 'false'
        else:
            time14 = 'true'

        if(room.piano_type == 0):
            money = user.group.smallPR_price
        elif(room.piano_type == 1):
            money = user.group.bigPR_price
        else:
            money = user.group.xinghaiPR_price
        dateToday.append({
            'name':room.room_id,
            'disabled':[time1,time2,time3,time4,time5,time6,time7,time8,time9,time10,time11,time12,time13,time14],
            'money':money
        })