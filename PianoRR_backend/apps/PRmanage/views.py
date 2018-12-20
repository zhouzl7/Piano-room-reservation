# _*_ coding: utf-8 _*_
# Create your views here.
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from PRmanage.models import Announcement, PianoRoom, TimeTable
from BOOKmanage.models import BookRecord
from USERmanage.models import User, UserGroup, BlackList
from PianoRR_backend.settings import WECHAT_APPID, WECHAT_SECRET
import json
import requests
import bcrypt
import datetime

def announcement(request):
    announceall = []
    announcements = Announcement.objects.all()
    for announcement in announcements:
        announceall.append({
            'title':announcement.title,
            'time':str(announcement.published_time),
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
    print(request.GET)
    data = {
        'appid': WECHAT_APPID,
        'secret': WECHAT_SECRET,
        'grant_type': 'authorization_code',
    }
    data['js_code'] = request.GET['code']
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=data)
    print(r.json())
    if r.json()['openid']:
        result = {
            'openId' : r.json()['openid']
        }
    else:
        result = {
            'errMsg' : '登录失败口..口|||'
        }
    return JsonResponse(result)

def availableTime(request):
    openId = request.GET['openId']
    user = User.objects.filter(open_id = openId).first()
    if(not user):
        return JsonResponse({'errMsg':'您尚未绑定!'})
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
    bookall = []
    openId = request.GET['openId']
    user = User.objects.filter(open_id = openId).first()
    if(user):
        bookLists = BookRecord.objects.filter(user = user.person_id)
        for book in bookLists:
            if(book.user_quantity):
                people = '单人'
            else:
                people = '多人'
            bookall.append({
                'room':book.piano_room.room_id,
                'useTime':str(book.BR_date) + ' ' + str(book.use_time+7) +':00-' + str(book.use_time+8)+':00',
                'people':people,
                'user':book.user
            })
        bookall.reverse()
    result = {
        'reserve': bookall
    }
    return JsonResponse(result)

def book(request):
    #check if the times are available
    body = json.loads(request.body)
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
                record = BookRecord.objects.create(user=user.person_id,fee=price,
                        is_pay=True,user_quantity=body['single'],
                        BR_date=datetime.date.today()+datetime.timedelta(days=i['day']),
                        use_time=int(j[4:]),status=BookRecord.STATUS_VALID,piano_room=room)
                #TODO: is_pay should be false by default, but there's no pay model
                record.save()
    else:
        resData['errMsg'] = '所选时间已被占用或无法使用!'
    #refresh the availableTime
    return JsonResponse(resData)

def isBind(request):
    openId = request.GET['openId']
    user = User.objects.filter(open_id = openId).first()
    if(user):  
        print(user.open_id)
        return JsonResponse({'name':user.name,'personId':user.person_id})
    else:
        return JsonResponse({'errMsg':'no'})

def notBind(request):
    openId = request.GET['openId']
    user = User.objects.filter(open_id = openId)
    if(not user):
        return JsonResponse({'errMsg':'no'})
    else:
        for i in user:
            i.open_id = ''
            i.save()
        return JsonResponse({'notBind':'ok'})


def salt(request):
    result = {}
    if('cellPhone' in request.GET):
        try:
            user = User.objects.get(person_id=request.GET['cellPhone'])
        except:
            result['errMsg'] = '用户不存在!'
            return JsonResponse(result)
        result['salt'] = user.pwhash[0:30]
    else:
        result['salt'] = bcrypt.gensalt(10).decode('utf-8')
    return JsonResponse(result)

def register(request):
    data = json.loads(request.body)
    if(User.objects.filter(person_id=data['cellPhone']).exists()):
        return JsonResponse({
            'errMsg': '手机号已被注册!'
        })
    else:
        group = UserGroup.objects.filter(group_name='普通用户').first()
        print(group)
        user = User.objects.create(open_id=data['openId'],person_id=data['cellPhone'],
                            pwhash=data['hash'],name=data['name'],group=group)
        user.save()
        return JsonResponse({})

def pwLogin(request):
    data = json.loads(request.body)
    try:
        user = User.objects.get(person_id=data['cellPhone'])
    except:
        return JsonResponse({
            'errMsg': '用户名或密码错误!'
        })
    if(user.pwhash != data['hash']):
        return JsonResponse({
            'errMsg': '用户名或密码错误!'
        })
    oldUsers = User.objects.filter(open_id=data['openId'])
    for i in oldUsers:
        i.open_id = ''
        i.save()
    user.open_id = data['openId']
    user.save()
    return JsonResponse({})