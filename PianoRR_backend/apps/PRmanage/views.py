# _*_ coding: utf-8 _*_
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.db import transaction
from django.db.models import Q
from PRmanage.models import Announcement,PianoRoom,TimeTable
from BOOKmanage.models import BookRecord
from USERmanage.models import User,UserGroup,BlackList
from django.core import serializers
from PianoRR_backend.settings import WECHAT_APPID, WECHAT_SECRET
import json
import requests
import datetime

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
    dateAfter_Tomorrow = []
    date0 = ''
    date1 = ''
    date2 = ''
    for room in PianoRoomLists:
        if(room.piano_type == 0):
            money = user.group.smallPR_price
        elif(room.piano_type == 1):
            money = user.group.bigPR_price
        else:
            money = user.group.xinghaiPR_price
        dateTodayi = TimeTable.objects.filter(piano_room=room,TT_type=0).first()
        if(dateTodayi):
            date0 = dateTodayi.date
            if(dateTodayi.Time1 == 1):
                time1 = False
            else:
                time1 = True
            if(dateTodayi.Time2 == 1):
                time2 = False
            else:
                time2 = True
            if(dateTodayi.Time3 == 1):
                time3 = False
            else:
                time3 = True
            if(dateTodayi.Time4 == 1):
                time4 = False
            else:
                time4 = True
            if(dateTodayi.Time5 == 1):
                time5 = False
            else:
                time5 = True
            if(dateTodayi.Time6 == 1):
                time6 = False
            else:
                time6 = True
            if(dateTodayi.Time7 == 1):
                time7 = False
            else:
                time7 = True
            if(dateTodayi.Time8 == 1):
                time8 = False
            else:
                time8 = True
            if(dateTodayi.Time9 == 1):
                time9 = False
            else:
                time9 = True
            if(dateTodayi.Time10 == 1):
                time10 = False
            else:
                time10 = True
            if(dateTodayi.Time11 == 1):
                time11 = False
            else:
                time11 = True
            if(dateTodayi.Time12 == 1):
                time12 = False
            else:
                time12 = True
            if(dateTodayi.Time13 == 1):
                time13 = False
            else:
                time13 = True
            if(dateTodayi.Time14 == 1):
                time14 = False
            else:
                time14 = True

            dateToday.append({
                'name':room.room_id,
                'disabled':[time1,time2,time3,time4,time5,time6,time7,time8,time9,time10,time11,time12,time13,time14],
                'money':money,
                'multiMoney': 2*money
            })

        dateTomorrowi = TimeTable.objects.filter(piano_room=room,TT_type=1).first()
        if(dateTomorrowi):
            date1 = dateTomorrowi.date
            if(dateTomorrowi.Time1 == 1):
                time1 = False
            else:
                time1 = True
            if(dateTomorrowi.Time2 == 1):
                time2 = False
            else:
                time2 = True
            if(dateTomorrowi.Time3 == 1):
                time3 = False
            else:
                time3 = True
            if(dateTomorrowi.Time4 == 1):
                time4 = False
            else:
                time4 = True
            if(dateTomorrowi.Time5 == 1):
                time5 = False
            else:
                time5 = True
            if(dateTomorrowi.Time6 == 1):
                time6 = False
            else:
                time6 = True
            if(dateTomorrowi.Time7 == 1):
                time7 = False
            else:
                time7 = True
            if(dateTomorrowi.Time8 == 1):
                time8 = False
            else:
                time8 = True
            if(dateTomorrowi.Time9 == 1):
                time9 = False
            else:
                time9 = True
            if(dateTomorrowi.Time10 == 1):
                time10 = False
            else:
                time10 = True
            if(dateTomorrowi.Time11 == 1):
                time11 = False
            else:
                time11 = True
            if(dateTomorrowi.Time12 == 1):
                time12 = False
            else:
                time12 = True
            if(dateTomorrowi.Time13 == 1):
                time13 = False
            else:
                time13 = True
            if(dateTomorrowi.Time14 == 1):
                time14 = False
            else:
                time14 = True

            dateTomorrow.append({
                'name':room.room_id,
                'disabled':[time1,time2,time3,time4,time5,time6,time7,time8,time9,time10,time11,time12,time13,time14],
                'money':money,
                'multiMoney': 2*money
            })

        dateAfter_Tomorrowi = TimeTable.objects.filter(piano_room=room,TT_type=2).first()
        if(dateAfter_Tomorrowi):
            date2 = dateAfter_Tomorrowi.date
            if(dateAfter_Tomorrowi.Time1 == 1):
                time1 = False
            else:
                time1 = True
            if(dateAfter_Tomorrowi.Time2 == 1):
                time2 = False
            else:
                time2 = True
            if(dateAfter_Tomorrowi.Time3 == 1):
                time3 = False
            else:
                time3 = True
            if(dateAfter_Tomorrowi.Time4 == 1):
                time4 = False
            else:
                time4 = True
            if(dateAfter_Tomorrowi.Time5 == 1):
                time5 = False
            else:
                time5 = True
            if(dateAfter_Tomorrowi.Time6 == 1):
                time6 = False
            else:
                time6 = True
            if(dateAfter_Tomorrowi.Time7 == 1):
                time7 = False
            else:
                time7 = True
            if(dateAfter_Tomorrowi.Time8 == 1):
                time8 = False
            else:
                time8 = True
            if(dateAfter_Tomorrowi.Time9 == 1):
                time9 = False
            else:
                time9 = True
            if(dateAfter_Tomorrowi.Time10 == 1):
                time10 = False
            else:
                time10 = True
            if(dateAfter_Tomorrowi.Time11 == 1):
                time11 = False
            else:
                time11 = True
            if(dateAfter_Tomorrowi.Time12 == 1):
                time12 = False
            else:
                time12 = True
            if(dateAfter_Tomorrowi.Time13 == 1):
                time13 = False
            else:
                time13 = True
            if(dateAfter_Tomorrowi.Time14 == 1):
                time14 = False
            else:
                time14 = True

            dateAfter_Tomorrow.append({
                'name':room.room_id,
                'disabled':[time1,time2,time3,time4,time5,time6,time7,time8,time9,time10,time11,time12,time13,time14],
                'money':money,
                'multiMoney': 2*money
            })

    Days = []
    Days.append({
        'name':date0,
        'room':dateToday
    })
    Days.append({
        'name':date1,
        'room':dateTomorrow
    })
    Days.append({
        'name':date2,
        'room':dateAfter_Tomorrow
    })

    result = {
        'Days':Days
    }
    return JsonResponse(result)

def reservation(request):
    openId = request.GET['openId']
    user = User.objects.filter(open_id = openId).first()
    bookLists = BookRecord.objects.filter(user = user)
    bookall = []
    for book in bookLists:
        bookall.append({
            'room':book.piano_room.room_id,
            'useTime':str(book.BR_date) + ' ' + str(book.use_time+7) +'-' + str(book.use_time+8),
            'people':book.user_quantity,
            'user':user.name
        })
    bookall.reverse()
    result = {
        'reserve': bookall
    }
    return JsonResponse(result)

def book(request):
    #check if the times are available
    body = json.loads(request.body)
    print(body['openId'])
    try:
        user = User.objects.get(open_id=body['openId'])
    except:
        return JsonResponse({'errMsg':'您尚未绑定!'})
    if(BlackList.objects.filter(open_id=body['openId']).exists()):
        return JsonResponse({'errMsg': '您已被加入黑名单,请联系管理员'})
    available = False
    query = Q()
    bookTime = body['bookTime']
    for i in bookTime:
        timeQuery = Q(piano_room=i['room']) & Q(TT_type=i['day'])
        for j in i['time']:
            timeQuery.children.append((j,TimeTable.TIME_ABLED))
        query = query | timeQuery
    print(query)
    result = TimeTable.objects.select_for_update().filter(query)
    with transaction.atomic():
        print(result)
        if len(result) == len(bookTime):
            available = True
            for i in result:
                for j in bookTime:
                    print(j)
                    if (j['day'] == i.TT_type) and (j['room'] == i.piano_room.room_id):
                        for time in j['time']:
                            print(time)
                            setattr(i,time,TimeTable.TIME_BOOKED)
                        break
                i.save()
        else:
            available = False
    
    money = 0
    resData = {
        'times': []
    }
    for timetable in TimeTable.objects.all():
        time = []
        for i in range(1,15):
            if(getattr(timetable,'Time'+str(i)) == 1):
                time.append(False)
            else:
                time.append(True)
        resData['times'].append({
            'day' : timetable.TT_type,
            'room' : timetable.piano_room.room_id,
            'disabled' : time
        })
    if available == True:
        if body['single']:
            prices = user.group
        else:
            prices = UserGroup.objects.get(group_name='普通用户')
        for i in bookTime:
            room = PianoRoom.objects.get(room_id=i['room'])
            if room.piano_type == PianoRoom.TYPE_SMALL:
                price = prices.smallPR_price
            elif room.piano_type == PianoRoom.TYPE_BIG:
                price = prices.bigPR_price
            elif room.piano_type == PianoRoom.TYPE_XINGHAI:
                price = prices.xinghaiPR_price
            money += len(i['time']) * price
            #createBookRecord:
            for j in i['time']:
                record = BookRecord.objects.create(user=user,fee=price,
                        is_pay=True,user_quantity=body['single'],
                        BR_date=datetime.date.today()+datetime.timedelta(days=i['day']),
                        use_time=int(j[4:]),status=BookRecord.STATUS_VALID,piano_room=room)
                #TODO: is_pay should be false by default, but there's no pay model
                record.save()
    else:
        resData['errMsg'] = '所选时间已被占用或无法使用!'
    #refresh the availableTime
    return JsonResponse(resData)
    
