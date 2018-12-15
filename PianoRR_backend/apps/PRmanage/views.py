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

import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from PRmanage.models import PianoRoom
from PRmanage.models import TimeTable
import datetime

try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")


    # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
    # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次
    @register_job(scheduler, 'cron', minute='58',second='59', id='task_time')
    def test_job():
        t_now = time.localtime()
        all_time_tables = TimeTable.objects.all()

        hour_now = t_now.tm_hour

        if int(hour_now)>=8 and int(hour_now)<=21:
            for all_time_table in all_time_tables:
                if all_time_table.TT_type == 0:
                    print('2-01')
                    if int(hour_now) == 7:
                        if all_time_table.Time1 == 1:
                            all_time_table.Time1 = -1
                    if int(hour_now) == 8:
                        if all_time_table.Time2 == 1:
                            all_time_table.Time2 = -1
                    if int(hour_now) == 9:
                        if all_time_table.Time3 == 1:
                            all_time_table.Time3 = -1
                    if int(hour_now) == 10:
                        if all_time_table.Time4 == 1:
                            all_time_table.Time4 = -1
                    if int(hour_now) == 11:
                        if all_time_table.Time5 == 1:
                            all_time_table.Time5 = -1
                    if int(hour_now) == 12:
                        if all_time_table.Time6 == 1:
                            all_time_table.Time6 = -1
                    if int(hour_now) == 13:
                        if all_time_table.Time7 == 1:
                            all_time_table.Time7 = -1
                    if int(hour_now) == 14:
                        if all_time_table.Time8 == 1:
                            all_time_table.Time8 = -1
                    if int(hour_now) == 15:
                        if all_time_table.Time9 == 1:
                            all_time_table.Time9 = -1
                    if int(hour_now) == 16:
                        if all_time_table.Time10 == 1:
                            all_time_table.Time10 = -1
                    if int(hour_now) == 17:
                        if all_time_table.Time11 == 1:
                            all_time_table.Time11 = -1
                    if int(hour_now) == 18:
                        if all_time_table.Time12 == 1:
                            all_time_table.Time12 = -1
                    if int(hour_now) == 19:
                        if all_time_table.Time13 == 1:
                            all_time_table.Time13 = -1
                    if int(hour_now) == 20:
                        if all_time_table.Time14 == 1:
                            all_time_table.Time14 = -1
                all_time_table.save()

        is_first = 0

        time_tables = TimeTable.objects.filter(TT_type='0')

        for time_table in time_tables:
            if str(time_table.date) == time.strftime('%Y-%m-%d', time.localtime(time.time())) and int(hour_now)==23:
                is_first = 1

        if is_first == 1:

            time_tables = TimeTable.objects.filter(TT_type='0')

            for time_table in time_tables:
                time_table.delete()

            time_tables = TimeTable.objects.filter(TT_type='1')

            for time_table in time_tables:
                time_table.TT_type = '0'
                time_table.save()

            time_tables = TimeTable.objects.filter(TT_type='2')

            for time_table in time_tables:
                time_table.TT_type = '1'
                time_table.save()

            time_tables = TimeTable.objects.filter(TT_type='0')

            for time_table in time_tables:
                today = datetime.date.today()
                date_old = today + datetime.timedelta(days=3)
                piano_room_old = time_table.piano_room
                time_table_new = TimeTable(piano_room=piano_room_old, TT_type='2', date=date_old, Time1=1,
                                           Time2=1, Time3=1, Time4=1, Time5=1, Time6=1,
                                           Time7=1, Time8=1, Time9=1,
                                           Time10=1, Time11=1, Time12=1,
                                           Time13=1,Time14=1)
                time_table_new.save()

            piano_rooms = PianoRoom.objects.all()
            for pianoroom in piano_rooms:
                time_tables = TimeTable.objects.filter(piano_room=pianoroom)
                if len(time_tables) == 0:
                    today = datetime.date.today()
                    today_new = today + datetime.timedelta(days=1)
                    tomorrow_new = today + datetime.timedelta(days=2)
                    after_tomorrow_new = today + datetime.timedelta(days=3)
                    time_table_new = TimeTable(piano_room=pianoroom, TT_type='0', date=today_new, Time1=1,
                                               Time2=1, Time3=1, Time4=1, Time5=1, Time6=1,
                                               Time7=1, Time8=1, Time9=1,
                                               Time10=1, Time11=1, Time12=1,
                                               Time13=1, Time14=1)
                    time_table_new.save()
                    time_table_new = TimeTable(piano_room=pianoroom, TT_type='1', date=tomorrow_new, Time1=1,
                                               Time2=1, Time3=1, Time4=1, Time5=1, Time6=1,
                                               Time7=1, Time8=1, Time9=1,
                                               Time10=1, Time11=1, Time12=1,
                                               Time13=1, Time14=1)
                    time_table_new.save()
                    time_table_new = TimeTable(piano_room=pianoroom, TT_type='2', date=after_tomorrow_new, Time1=1,
                                               Time2=1, Time3=1, Time4=1, Time5=1, Time6=1,
                                               Time7=1, Time8=1, Time9=1,
                                               Time10=1, Time11=1, Time12=1,
                                               Time13=1, Time14=1)
                    time_table_new.save()
        print("已刷新")
    # 监控任务
    register_events(scheduler)
    # 调度器开始
    scheduler.start()
except Exception as e:
    print(e)
    # 报错则调度器停止执行
    scheduler.shutdown()


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

def room(request):
    allroom = []
    all_xinghai = ""
    room_xinghai = PianoRoom.objects.filter(piano_type=PianoRoom.TYPE_XINGHAI)
    if(room_xinghai):
        for room in room_xinghai:
            all_xinghai = all_xinghai + "\n" + room.room_id
        allroom.append({
            "room_type":"星海琴房",
            "room":all_xinghai
        })

    all_big = ""
    room_big = PianoRoom.objects.filter(piano_type=PianoRoom.TYPE_BIG)
    if(room_big):
        for room in room_big:
            all_big = all_big + "\n" + room.room_id
        allroom.append({
            "room_type":"大琴房",
            "room":all_big
        })

    all_small = ""
    room_small = PianoRoom.objects.filter(piano_type=PianoRoom.TYPE_SMALL)
    if(room_small):
        for room in room_small:
            all_small = all_small + "\n" + room.room_id
        allroom.append({
            "room_type":"小琴房",
            "room":all_small
        })
    
    result = {
        'allroom':allroom
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
    if r.json()['openid']:
        result = {
            'openId' : r.json()['openid'] 
        }
        try:
            user = User.objects.get(open_id=result['openId'])
        except:
            #create New User by default:
            user = User.objects.create(open_id=result['openId'])
            user.group = UserGroup.objects.get(group_name='普通用户')
            user.save()
    else:
        result = {
            'errMsg' : '登录失败口..口|||'
        }
    return JsonResponse(result)

def availableTime(request):
    openId = request.GET['openId']
    user = User.objects.filter(open_id = openId).first()
    multiUser = UserGroup.objects.filter(group_name="普通用户").first()
    PianoRoomLists = PianoRoom.objects.all()
    Days = []
    for day in range(0,3):
        date = datetime.date.today() + datetime.timedelta(day)
        Days.append({
            'name': f"{date:%m-%d}",
            'room': []
        })
    for room in PianoRoomLists:
        if(user.group not in room.user_group.all()): #没有权限
            continue
        if(room.piano_type == PianoRoom.TYPE_SMALL):
            money = user.group.smallPR_price
            multiMoney = multiUser.smallPR_price
        elif(room.piano_type == PianoRoom.TYPE_BIG):
            money = user.group.bigPR_price
            multiMoney = multiUser.bigPR_price
        elif(room.piano_type == PianoRoom.TYPE_XINGHAI):
            money = user.group.xinghaiPR_price
            multiMoney = multiUser.xinghaiPR_price
        for day in range(0,3):
            timetable = TimeTable.objects.filter(Q(piano_room=room.room_id) & Q(TT_type=day)).first()
            if(not timetable):
                continue
            disabled = []
            for i in range(1,15):
                if(getattr(timetable,'Time'+str(i)) == TimeTable.TIME_ABLED):
                    disabled.append(False)
                else:
                    disabled.append(True)
            Days[day]['room'].append({
                'name': room.room_id,
                'disabled': disabled,
                'money': money,
                'multiMoney': multiMoney
            })
    for day in Days:
        if(not day['room']):
            Days.remove(day)
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
        if(book.user_quantity):
            people = '单人'
        else:
            people = '多人'
        bookall.append({
            'room':book.piano_room.room_id,
            'useTime':str(book.BR_date) + ' ' + str(book.use_time+7) +':00-' + str(book.use_time+8)+':00',
            'people':people,
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
            if(getattr(timetable,'Time'+str(i)) == TimeTable.TIME_ABLED):
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