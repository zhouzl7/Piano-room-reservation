# _*_ coding: utf-8 _*_
# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from PRmanage.models import Announcement, PianoRoom, TimeTable
from BOOKmanage.models import BookRecord
from USERmanage.models import User, UserGroup, BlackList, ArtTroupeMember
from PianoRR_backend.settings import WECHAT_APPID, WECHAT_SECRET
from PianoRR_backend.settings import client_appid,client_secret,Mch_id,Mch_key
import os
import json
import re
import requests
import bcrypt
import datetime, time
import hashlib
import xml.etree.ElementTree as ET
from .countDown import countDown

def announcement(request):
    announceall = []
    announcements = Announcement.objects.all()
    for announcement in announcements:
        announceall.append({
            'title': announcement.title,
            'time': str(announcement.published_time),
            'author': announcement.published_person,
            'content': announcement.content
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
        'appid': client_appid,
        'secret': client_secret,
        'grant_type': 'authorization_code',
    }
    data['js_code'] = request.GET['code']
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=data)
    if 'openid' in r.json():
        print(r.json())
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
    user = User.objects.filter(open_id=openId).first()
    if(user):
        bookLists = BookRecord.objects.filter(person_id=user.person_id)
        for book in bookLists:
            if book.user_quantity:
                people = '单人'
            else:
                people = '多人'
            if book.status == BookRecord.STATUS_CANCELLED:
                record_status = u'已取消'
            elif book.status == BookRecord.STATUS_USED:
                record_status = u'已赴约'
            elif book.status == BookRecord.STATUS_VALID:
                record_status = u'未赴约'
            bookall.append({
                'room': book.piano_room.room_id,
                'useTime': str(book.BR_date) + ' ' + str(book.use_time+7) +':00-' + str(book.use_time+8)+':00',
                'people': people,
                'user': book.person_id,
                'is_pay': u'已付款' if book.is_pay else u'待付款',
                'status': record_status
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
        return JsonResponse({'errMsg': '您尚未绑定!'})
    person_id = User.objects.get(open_id=body['openId']).person_id
    if BlackList.objects.filter(person_id=person_id).exists():
        return JsonResponse({'errMsg': '您已被加入黑名单,请联系管理员'})
    available = False
    query = Q()
    bookTime = body['bookTime']
    for i in bookTime:
        timeQuery = Q(piano_room=i['room']) & Q(TT_type=i['day'])
        for j in i['time']:
            timeQuery.children.append((j, TimeTable.TIME_ABLED))
        query = query | timeQuery
    result = TimeTable.objects.select_for_update().filter(query)
    with transaction.atomic():
        if len(result) == len(bookTime):
            available = True
            for i in result:
                for j in bookTime:
                    if (j['day'] == i.TT_type) and (j['room'] == i.piano_room.room_id):
                        for t in j['time']:
                            setattr(i, t, TimeTable.TIME_BOOKED)
                        break
                i.save()
        else:
            available = False
    
    resData = {
        'times': []
    }
    for timetable in TimeTable.objects.all():
        disable = []
        for i in range(1,15):
            if(getattr(timetable,'Time'+str(i)) == TimeTable.TIME_ABLED):
                disable.append(False)
            else:
                disable.append(True)
        resData['times'].append({
            'day': timetable.TT_type,
            'room': timetable.piano_room.room_id,
            'disabled': disable
        })
    if available == True:
        money = 0
        payOrderId = getWxPayOrderID()
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
            recordId_List = []
            for j in i['time']:
                record = BookRecord.objects.create(person_id=user.person_id, fee=price, name = user.name,
                                                   is_pay=False, user_quantity=body['single'],pay_id=payOrderId,
                                                   BR_date=datetime.date.today()+datetime.timedelta(days=i['day']),
                                                   use_time=int(j[4:]), status=BookRecord.STATUS_VALID, piano_room=room)
                record.save()
                recordId_List.append(record.id)
            countDown(recordId_List)        
        param = {
            'price': money,
            'openId': body['openId'],
            'payOrderId':  payOrderId
        }
        payParam = payOrder(param)
        resData['payParam'] = payParam
    else:
        resData['errMsg'] = '所选时间已被占用或无法使用!'
    #refresh the availableTime
    return JsonResponse(resData)

def isBind(request):
    openId = request.GET['openId']
    user = User.objects.filter(open_id = openId).first()
    if (user):
        return JsonResponse({'name': user.name, 'personId': user.person_id, 'userGroup': user.group.group_name,
                             'bigPrice': user.group.bigPR_price, 'smallPrice': user.group.smallPR_price,
                             'xinghaiPrice': user.group.xinghaiPR_price})
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

def bindRedirect(request):
    if 'ticket' not in request.GET:
        return HttpResponse(status=404)
    context = {
        'ticket': request.GET['ticket']
    }
    return render(request, 'bindRedirect.html', context)

def bindCampus(request):
    if 'openId' not in request.GET:
        return HttpResponse(status=404)
    if 'ticket' in request.GET:
        print(request.GET)
        url = 'https://id-tsinghua-test.iterator-traits.com/thuser/authapi/checkticket/PIANO/'
        url += request.GET['ticket']
        url += '/'+'140_143_57_245'
        res = requests.get(url).text
        print(res)
        regExp = re.findall('([^:=]*)=([^:=]*)',res)
        data = {}
        for i in regExp:
            data[i[0]] = i[1]
        if('yhm' not in data):
            return JsonResponse({'errMsg' : '登录超时,请稍后重试'})
        oldUsers = User.objects.filter(open_id=request.GET['openId'])
        for i in oldUsers:
            i.open_id = ''
            i.save()
        user = User.objects.filter(person_id=data['zjh']).first()
        if(user):
            user.open_id = request.GET['openId']
            user.save()
            return JsonResponse({
                'name': data['xm'],
                'personId': data['zjh']
            })
        else:
            teacherCode = ['J0000','H0000','J0054']
            studentCode = ['X0011','X0021','X0031']
            if data['yhlb'] in teacherCode:
                group = UserGroup.objects.filter(group_name='教职工').first()
            elif data['yhlb'] in studentCode:
                group = UserGroup.objects.filter(group_name='校内学生').first()
                if ArtTroupeMember.objects.filter(student_id=data['zjh']).exists():
                    group = UserGroup.objects.filter(group_name='艺术团').first()
            user = User.objects.create(open_id=request.GET['openId'], person_id=data['zjh'], name=data['xm'], group=group)
            user.save()
            return JsonResponse({
                'name': data['xm'],
                'personId': data['zjh']
            })
    else:
        return HttpResponse(status=404)

def getNonceStr():
    import random
    data="123456789zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP"
    nonce_str  = ''.join(random.sample(data , 30))
    return nonce_str
#生成签名的函数
def paysign(appid,body,mch_id,nonce_str,notify_url,openid,out_trade_no,spbill_create_ip,total_fee):
    ret= {
        "appid": appid,
        "body": body,
        "mch_id": mch_id,
        "nonce_str": nonce_str,
        "notify_url":notify_url,
        "openid":openid,
        "out_trade_no":out_trade_no,
        "spbill_create_ip":spbill_create_ip,
        "total_fee":total_fee,
        "trade_type": 'JSAPI'
    }
 
    #处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k))for k in sorted(ret)])
    stringSignTemp = '{0}&key={1}'.format(stringA,Mch_key)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()
#生成商品订单号，方式一：
def getWxPayOrderID(): 
    date=datetime.datetime.now()
    #根据当前系统时间来生成商品订单号。时间精确到微秒
    payOrderId=date.strftime("%Y%m%d%H%M%S%f") + os.urandom(5).hex()
    return payOrderId
#获取返回给小程序的paySign
def get_paysign(prepay_id,timeStamp,nonceStr):
    pay_data={
                'appId': client_appid,
                'nonceStr': nonceStr,
                'package': "prepay_id="+prepay_id,
                'signType': 'MD5',
                'timeStamp':timeStamp
    }
    stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k))for k in sorted(pay_data)])
    stringSignTemp = '{0}&key={1}'.format(stringA,Mch_key)
    sign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest()
    return sign.upper()

#获取全部参数信息，封装成xml,传递过来的openid和客户端ip，和价格需要我们自己获取传递进来
def getBodyData(openid,clientIp,price,payOrderId):
    body = 'Mytest'                    #商品描述
    notify_url = "https://166628.iterator-traits.com/api/wxPayConfirm"      #填写支付成功的回调地址，微信确认支付成功会访问这个接口
    nonce_str =getNonceStr()           #随机字符串
    out_trade_no = payOrderId    #商户订单号
    total_fee = str(price)              #订单价格，单位是 分
    #获取签名                                        
    sign=paysign(client_appid,body,Mch_id,nonce_str,notify_url,openid,out_trade_no,clientIp,total_fee) 
 
    bodyData = '<xml>'
    bodyData += '<appid>' + client_appid + '</appid>' 
    print(client_appid)            # 小程序ID
    bodyData += '<body>' + body + '</body>'                         #商品描述
    bodyData += '<mch_id>' + Mch_id + '</mch_id>'   
    print(Mch_id)       #商户号
    bodyData += '<nonce_str>' + nonce_str + '</nonce_str>' 
    print(nonce_str)        #随机字符串
    bodyData += '<notify_url>' + notify_url + '</notify_url>'      
    print(notify_url)#支付成功的回调地址
    bodyData += '<openid>' + str(openid) + '</openid>'  
    print(openid)                 #用户标识
    bodyData += '<out_trade_no>' + out_trade_no + '</out_trade_no>'
    print(out_trade_no)#商户订单号
    bodyData += '<spbill_create_ip>' + clientIp + '</spbill_create_ip>'
    print(clientIp)#客户端终端IP
    bodyData += '<total_fee>' + total_fee + '</total_fee>' 
    print(total_fee)        #总金额 单位为分
    bodyData += '<trade_type>JSAPI</trade_type>'                   #交易类型 小程序取值如下：JSAPI
 
    bodyData += '<sign>' + sign + '</sign>'
    print(sign)
    bodyData += '</xml>'
    print(bodyData)
 
    return bodyData
def xml2Dict(xml_data):
    '''
    xml to dict
    :param xml_data:
    :return:
    '''
    xml_dict = {}
    root = ET.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict
def dict2Xml(dict_data):
    '''
    dict to xml
    :param dict_data:
    :return:
    '''
    xml = ["<xml>"]
    for k, v in dict_data.items():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)

#统一下单支付接口
def payOrder(param):
        #获取价格
    price=param["price"]*100
        #获取客户端ip
    clientIp='140.143.57.245'
        #获取小程序openid
    openid= param["openId"]
    payOrderId = param["payOrderId"]
    print(openid)
        #请求微信的url
    url= 'https://api.mch.weixin.qq.com/sandbox/pay/unifiedorder'
        #拿到封装好的xml数据
    bodyData = getBodyData(openid,clientIp,price,payOrderId)
        #获取时间戳
    timeStamp=str(int(time.time()))
 
    #请求微信接口下单
    response=requests.post(url,bodyData,headers={'Content-Type': 'application/xml'})
    #回复数据为xml,将其转为字典
    content= xml2Dict(response.content)
    print(content["return_code"])
    if content["return_code"]=='SUCCESS':
        #获取预支付交易会话标识
        prepay_id =content.get("prepay_id")
        #获取随机字符串
        nonceStr =content.get("nonce_str")
 
        #获取paySign签名，这个需要我们根据拿到的prepay_id和nonceStr进行计算签名
        paySign=get_paysign(prepay_id,timeStamp,nonceStr)

        #封装返回给前端的数据
        data={"package":"prepay_id="+str(prepay_id),"nonceStr":nonceStr,"paySign":paySign,"timeStamp":timeStamp,'status':100}
        print(data)
        return data 
    else:
        return {"errMsg":"请求支付失败"}

def wxPayConfirm(request):
    content = xml2Dict(request.body)
    print(content)
    if content['return_code'] == 'SUCCESS':
        #签名验证
        keys = list(content.keys())
        #清理空参数
        for k in keys:
            if not content[k]:
                content.pop(k)
        recvSign = content.pop('sign')
        stringA = '&'.join('='.join(i) for i in sorted(content.items()))
        stringSign = stringA + '&key=' + Mch_key
        sign = hashlib.md5(stringSign.encode("utf-8")).hexdigest().upper()
        print(sign)
        if recvSign == sign :
            print('签名验证通过')
            #金钱验证:
            record = BookRecord.objects.select_for_update().filter(pay_id=content['out_trade_no'])
            with transaction.atomic():
                for i in record:
                    print(i)
                money = 0
                for r in record:
                    money += r.fee
                    if r.is_pay == True:
                        reply = {
                            'return_code': 'SUCCESS',
                            'return_msg': 'OK'
                        }
                        xml = dict2Xml(reply)
                        return HttpResponse(xml, content_type='application/xml')
                money *= 100
                print(money)
                if str(money) == content['total_fee']:
                    for r in record:
                        print(r.is_pay)
                        r.is_pay = True
                        r.save()
                else:
                    reply = {
                        'return_code': 'FAIL',
                        'return_msg': 'FEEERROR'
                    }
                    xml = dict2Xml(reply)
                    return HttpResponse(xml, content_type='application/xml')
        else:
            reply = {
                'return_code': 'FAIL',
                'return_msg': 'SIGNERROR'
            }
            return HttpResponse(dict2Xml(reply), content_type='application/xml')
    reply = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }
    xml = dict2Xml(reply)
    return HttpResponse(xml, content_type='application/xml')
