from django.test import TestCase, Client
from django.utils import timezone
from django.http import HttpResponse,JsonResponse
from django.db import transaction
from django.db.models import Q
from PRmanage.models import Announcement,PianoRoom,TimeTable
from BOOKmanage.models import BookRecord
from USERmanage.models import User,UserGroup,BlackList
from django.core import serializers
from PianoRR_backend.settings import WECHAT_APPID, WECHAT_SECRET
from PRmanage.views import announcement
import json
import requests
import datetime
# Create your tests here.
class getAnnouncementTest(TestCase):
    #初始化
    def setUp(self):
        Announcement.objects.create(title = "test1", content="content1",
                                    published_time=datetime.datetime.now(),
                                    published_person = "admin1")
        Announcement.objects.create(title = "test2",content = "content2",
                                    published_time=datetime.datetime.now(),
                                    published_person = "admin2")

    #测试数量以及内容正确性
    def test_announce(self):
        get_announce = self.client.get("/api/announcement")
        response = json.loads(get_announce.content)
        self.assertEqual(response['announce'][0]['title'],"test2")
        self.assertEqual(response['announce'][0]['content'],"content2")
        self.assertEqual(response['announce'][0]['author'],"admin2")
        self.assertEqual(response['announce'][1]['title'],"test1")
        self.assertEqual(response['announce'][1]['content'],"content1")
        self.assertEqual(response['announce'][1]['author'],"admin1")
        self.assertEqual(len(response['announce']),2)
    
    def clear(self):
        Announcement.objects.all().delete() 

#所有种类琴房均存在且琴房个数不定
class getallRoomTest(TestCase):

    def setUp(self):
        PianoRoom.objects.create(room_id = 101, piano_type = 2,status = True)
        PianoRoom.objects.create(room_id = 202, piano_type = 1,status = True)
        PianoRoom.objects.create(room_id = 505, piano_type = 1,status = True)
        PianoRoom.objects.create(room_id = 606, piano_type = 1,status = True)
        PianoRoom.objects.create(room_id = 303, piano_type = 0,status = True)
        PianoRoom.objects.create(room_id = 404, piano_type = 0,status = True)

    #测试是否获取了所有的琴房以及琴房种类是否正确
    def test_getallroom(self):
        get_room = self.client.get("/api/room")
        response = json.loads(get_room.content)
        self.assertEqual(len(response['allroom']),3)
        self.assertEqual(response['allroom'][0]['room'],"\n101")
        self.assertEqual(response['allroom'][1]['room'],"\n202\n505\n606")
        self.assertEqual(response['allroom'][2]['room'],"\n303\n404")

    def clear(self):
        PianoRoom.objects.all().delete()

#没有琴房
class getNoRoomTest(TestCase):

    def test_getnoroom(self):
        get_room = self.client.get("/api/room")
        response = json.loads(get_room.content)
        self.assertEqual(len(response['allroom']),0)

#只有部分种类琴房 
class getPartRoomTest(TestCase):

    def setUp(self):
        PianoRoom.objects.create(room_id = 101, piano_type = 2,status = True)
        PianoRoom.objects.create(room_id = 202, piano_type = 1,status = True)

    #测试是否获取了所有的琴房以及琴房种类是否正确
    def test_getPartroom(self):
        get_room = self.client.get("/api/room")
        response = json.loads(get_room.content)
        self.assertEqual(len(response['allroom']),2)
        self.assertEqual(response['allroom'][0]['room'],"\n101")
        self.assertEqual(response['allroom'][1]['room'],"\n202")

    def clear(self):
        PianoRoom.objects.all().delete()

#预约情况查询
class getReservation(TestCase):

    def setUp(self):
        PianoRoom.objects.create(room_id = 101, piano_type = 2,status = True)
        room = PianoRoom.objects.get(room_id = 101)
        UserGroup.objects.create(group_name = "艺术团", xinghaiPR_price=1,smallPR_price=2,bigPR_price=3)
        usergroup = UserGroup.objects.get(group_name = "艺术团")
        User.objects.create(open_id = "1",person_id = "123",pwhash = "123",name="user1",group=usergroup)
        User.objects.create(open_id = "2",person_id = "1234",pwhash = "1234",name="user2",group=usergroup)
        User.objects.create(open_id = "3",person_id = "12345",pwhash = "12345",name="user3",group=usergroup)
        BookRecord.objects.create(person_id = "1234",fee = 1,is_pay = True,user_quantity = True,
                                    BR_date=datetime.date.today(), name = 'wtf', pay_id = '',
                                    use_time = 1,status = BookRecord.STATUS_VALID,piano_room=room)
        BookRecord.objects.create(person_id = "12345",fee = 1,is_pay = True,user_quantity = True,
                                    BR_date=datetime.date.today(), name = 'wtf', pay_id = '',
                                    use_time = 1,status = BookRecord.STATUS_VALID,piano_room=room)
        BookRecord.objects.create(person_id = "12345",fee = 1,is_pay = True,user_quantity = False,
                                    BR_date=datetime.date.today(), name = 'wtf', pay_id = '',
                                    use_time = 1,status = BookRecord.STATUS_VALID,piano_room=room)

    #用户不存在
    def test_NoUser(self):
        openId = "111"
        get_reservation = self.client.get("/api/reservation",{'openId':openId})
        response = json.loads(get_reservation.content)
        self.assertEqual(len(response['reserve']),0)
    
    #用户无订单
    def test_NoReservation(self):
        openId = "1"
        get_reservation = self.client.get("/api/reservation",{'openId':openId})
        response = json.loads(get_reservation.content)
        self.assertEqual(len(response['reserve']),0)
    
    #用户有一个订单
    def test_getReservation(self):
        openId = "2"
        get_reservation = self.client.get("/api/reservation",{'openId':openId})
        response = json.loads(get_reservation.content)
        self.assertEqual(len(response['reserve']),1)
        self.assertEqual(response['reserve'][0]['room'],"101")
        self.assertEqual(response['reserve'][0]['people'],"单人")
        self.assertEqual(response['reserve'][0]['user'],"1234")

    #用户有多个订单
    def test_getMoreReservation(self):
        openId = "3"
        get_reservation = self.client.get("/api/reservation",{'openId':openId})
        response = json.loads(get_reservation.content)
        self.assertEqual(len(response['reserve']),2)
        self.assertEqual(response['reserve'][0]['room'],"101")
        self.assertEqual(response['reserve'][0]['people'],"多人")
        self.assertEqual(response['reserve'][0]['user'],"12345")

        self.assertEqual(response['reserve'][1]['room'],"101")
        self.assertEqual(response['reserve'][1]['people'],"单人")
        self.assertEqual(response['reserve'][1]['user'],"12345")

    def clear(self):
        UserGroup.objects.all().delete()
        User.objects.all().delete()
        PianoRoom.objects.all().delete()
        BookRecord.objects.all().delete()

#获取可预约时间
class getTime(TestCase):

    def setUp(self):
        #创建用户组
        UserGroup.objects.create(group_name = "普通用户", xinghaiPR_price = 10, 
                                    smallPR_price=20, bigPR_price = 30)
        UserGroup.objects.create(group_name = "校内学生", xinghaiPR_price = 5,
                                    smallPR_price = 15, bigPR_price = 25)
        UserGroup.objects.create(group_name = "艺术团", xinghaiPR_price = 1,
                                    smallPR_price = 2, bigPR_price = 3)
        usualuser = UserGroup.objects.get(group_name = "普通用户")
        student = UserGroup.objects.get(group_name = "校内学生")
        art = UserGroup.objects.get(group_name = "艺术团")

        #创建用户
        User.objects.create(open_id = "1", person_id = "123", pwhash="123", name = "user1",group = usualuser)
        User.objects.create(open_id = "2", person_id = "1234", pwhash = "1234",name = "user2", group = student)
        User.objects.create(open_id = "3", person_id = "12345",pwhash = "12345",name= "user3", group = art)

        #创建三种琴房
        PianoRoom.objects.create(room_id = 101, piano_type = 2,status = True)
        room1 = PianoRoom.objects.get(room_id = 101)
        room1.user_group.add(usualuser)
        room1.user_group.add(art)
        room1.save()
        PianoRoom.objects.create(room_id = 202, piano_type = 1,status = True)
        room2 = PianoRoom.objects.get(room_id = 202)
        room2.user_group.add(student)
        room2.user_group.add(art)
        room2.save()
        PianoRoom.objects.create(room_id = 303, piano_type = 0,status = True)
        room3 = PianoRoom.objects.get(room_id = 303)
        room3.user_group.add(art)
        room3.save()

        #创建时间表
        TimeTable.objects.create(piano_room = room1, TT_type=0,date = datetime.date.today(),
                                    Time1 = 1,Time2 = 1,Time3 = 1,Time4 = 1,Time5 = 1,
                                    Time6 = 1,Time7 = 1,Time8 = 1,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 1,Time13 = 1,Time14 = 1)
        TimeTable.objects.create(piano_room = room1, TT_type=1,date = datetime.date.today()+datetime.timedelta(1),
                                    Time1 = 0,Time2 = 1,Time3 = 0,Time4 = 1,Time5 = 0,
                                    Time6 = 0,Time7 = 1,Time8 = 0,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 0,Time13 = 0,Time14 = 1)
        TimeTable.objects.create(piano_room = room1, TT_type=2,date = datetime.date.today()+datetime.timedelta(2),
                                    Time1 = 1,Time2 = 1,Time3 = 1,Time4 = 1,Time5 = 1,
                                    Time6 = 1,Time7 = 1,Time8 = 1,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 1,Time13 = 1,Time14 = 1)
        TimeTable.objects.create(piano_room = room2, TT_type=0,date = datetime.date.today(),
                                    Time1 = 0,Time2 = 0,Time3 = 0,Time4 = 0,Time5 = 0,
                                    Time6 = 0,Time7 = 0,Time8 = 0,Time9 = 0,Time10 = 0,
                                    Time11 = 0,Time12 = 0,Time13 = 0,Time14 = 0)
        TimeTable.objects.create(piano_room = room2, TT_type=1,date = datetime.date.today()+datetime.timedelta(1),
                                    Time1 = 1,Time2 = 1,Time3 = 1,Time4 = 1,Time5 = 1,
                                    Time6 = 1,Time7 = 1,Time8 = 1,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 1,Time13 = 1,Time14 = 1)
        #TimeTable.objects.create(piano_room = room2, TT_type=2,date = datetime.date.today()+datetime.timedelta(2),
        #                            Time1 = 1,Time2 = 1,Time3 = 1,Time4 = 1,Time5 = 1,
        #                            Time6 = 1,Time7 = 1,Time8 = 1,Time9 = 1,Time10 = 1,
        #                            Time11 = 1,Time12 = 1,Time13 = 1,Time14 = 1)
        TimeTable.objects.create(piano_room = room3, TT_type=0,date = datetime.date.today(),
                                    Time1 = 1,Time2 = 1,Time3 = 1,Time4 = 1,Time5 = 1,
                                    Time6 = 1,Time7 = 1,Time8 = 1,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 1,Time13 = 1,Time14 = 1)
        TimeTable.objects.create(piano_room = room3, TT_type=1,date = datetime.date.today()+datetime.timedelta(1),
                                    Time1 = 0,Time2 = 1,Time3 = 0,Time4 = 1,Time5 = 0,
                                    Time6 = 0,Time7 = 1,Time8 = 0,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 0,Time13 = 0,Time14 = 1)
        TimeTable.objects.create(piano_room = room3, TT_type=2,date = datetime.date.today()+datetime.timedelta(2),
                                    Time1 = 0,Time2 = 0,Time3 = 0,Time4 = 0,Time5 = 0,
                                    Time6 = 1,Time7 = 1,Time8 = 1,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 1,Time13 = 1,Time14 = 1)

    #用户未绑定
    def test_noUser(self):
        openId = "0"
        get_availableTime = self.client.get("/api/availableTime",{'openId':openId})
        response = json.loads(get_availableTime.content)
        self.assertEqual(response['errMsg'],"您尚未绑定!")

    #普通用户只可以预约琴房101星海琴房
    def test_usualuser(self):
        openId = "1"
        get_availableTime = self.client.get("/api/availableTime",{'openId':openId})
        response = json.loads(get_availableTime.content)
        disabled = []
        for i in range(0,14):
            disabled.append(False)
        self.assertEqual(len(response['Days']),3)
        self.assertEqual(len(response['Days'][0]['room']),1)
        self.assertEqual(len(response['Days'][1]['room']),1)
        self.assertEqual(len(response['Days'][2]['room']),1)

        self.assertEqual(response['Days'][0]['room'][0]['name'],'101')
        for i in range(0,14):
            self.assertEqual(response['Days'][0]['room'][0]['disabled'][i],disabled[i])
        self.assertEqual(response['Days'][0]['room'][0]['money'],10)
        self.assertEqual(response['Days'][0]['room'][0]['multiMoney'],10)

        self.assertEqual(response['Days'][1]['room'][0]['name'],'101')

        self.assertEqual(response['Days'][1]['room'][0]['disabled'][0],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][1],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][2],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][3],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][4],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][5],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][6],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][7],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][8],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][9],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][10],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][11],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][12],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][13],False)

        self.assertEqual(response['Days'][1]['room'][0]['money'],10)
        self.assertEqual(response['Days'][1]['room'][0]['multiMoney'],10)

        self.assertEqual(response['Days'][2]['room'][0]['name'],'101')
        for i in range(0,14):
            self.assertEqual(response['Days'][2]['room'][0]['disabled'][i],disabled[i])
        self.assertEqual(response['Days'][2]['room'][0]['money'],10)
        self.assertEqual(response['Days'][2]['room'][0]['multiMoney'],10)

    #student+两张时间表的big琴房
    def test_student(self):
        openId = "2"
        get_availableTime = self.client.get("/api/availableTime",{'openId':openId})
        response = json.loads(get_availableTime.content)
        disabled1 = []
        disabled2 = []
        for i in range(0,14):
            disabled1.append(False)
            disabled2.append(True)
        self.assertEqual(len(response['Days']),2)
        self.assertEqual(len(response['Days'][0]['room']),1)
        self.assertEqual(len(response['Days'][1]['room']),1)

        self.assertEqual(response['Days'][0]['room'][0]['name'],'202')
        for i in range(0,14):
            self.assertEqual(response['Days'][0]['room'][0]['disabled'][i],disabled2[i])
        self.assertEqual(response['Days'][0]['room'][0]['money'],25)
        self.assertEqual(response['Days'][0]['room'][0]['multiMoney'],30)

        self.assertEqual(response['Days'][1]['room'][0]['name'],'202')
        for i in range(0,14):
            self.assertEqual(response['Days'][1]['room'][0]['disabled'][i],disabled1[i])
        self.assertEqual(response['Days'][1]['room'][0]['money'],25)
        self.assertEqual(response['Days'][1]['room'][0]['multiMoney'],30)

    #艺术团+多个琴房
    def test_art(self):
        openId = "3"
        get_availableTime = self.client.get("/api/availableTime",{'openId':openId})
        response = json.loads(get_availableTime.content)
        disabled1 = []
        disabled2 = []
        for i in range(0,14):
            disabled1.append(False)
            disabled2.append(True)
        self.assertEqual(len(response['Days']),3)
        self.assertEqual(len(response['Days'][0]['room']),3)
        self.assertEqual(len(response['Days'][1]['room']),3)
        self.assertEqual(len(response['Days'][2]['room']),2)

        #琴房101三张时间表获取是否正确
        #art用户组价格回去是否正确
        self.assertEqual(response['Days'][0]['room'][0]['name'],'101')
        for i in range(0,14):
            self.assertEqual(response['Days'][0]['room'][0]['disabled'][i],disabled1[i])
        self.assertEqual(response['Days'][0]['room'][0]['money'],1)
        self.assertEqual(response['Days'][0]['room'][0]['multiMoney'],10)

        self.assertEqual(response['Days'][1]['room'][0]['name'],'101')

        self.assertEqual(response['Days'][1]['room'][0]['disabled'][0],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][1],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][2],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][3],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][4],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][5],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][6],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][7],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][8],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][9],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][10],False)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][11],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][12],True)
        self.assertEqual(response['Days'][1]['room'][0]['disabled'][13],False)

        self.assertEqual(response['Days'][1]['room'][0]['money'],1)
        self.assertEqual(response['Days'][1]['room'][0]['multiMoney'],10)

        self.assertEqual(response['Days'][2]['room'][0]['name'],'101')
        for i in range(0,14):
            self.assertEqual(response['Days'][2]['room'][0]['disabled'][i],disabled1[i])
        self.assertEqual(response['Days'][2]['room'][0]['money'],1)
        self.assertEqual(response['Days'][2]['room'][0]['multiMoney'],10)

        #琴房202两张时间表获取
        self.assertEqual(response['Days'][0]['room'][1]['name'],'202')
        for i in range(0,14):
            self.assertEqual(response['Days'][0]['room'][1]['disabled'][i],disabled2[i])
        self.assertEqual(response['Days'][0]['room'][1]['money'],3)
        self.assertEqual(response['Days'][0]['room'][1]['multiMoney'],30)

        self.assertEqual(response['Days'][1]['room'][1]['name'],'202')
        for i in range(0,14):
            self.assertEqual(response['Days'][1]['room'][1]['disabled'][i],disabled1[i])
        self.assertEqual(response['Days'][1]['room'][1]['money'],3)
        self.assertEqual(response['Days'][1]['room'][1]['multiMoney'],30)

        #琴房303三张表获取情况
        self.assertEqual(response['Days'][0]['room'][2]['name'],'303')
        for i in range(0,14):
            self.assertEqual(response['Days'][0]['room'][2]['disabled'][i],disabled1[i])
        self.assertEqual(response['Days'][0]['room'][2]['money'],2)
        self.assertEqual(response['Days'][0]['room'][2]['multiMoney'],20)

        self.assertEqual(response['Days'][1]['room'][2]['name'],'303')

        self.assertEqual(response['Days'][1]['room'][2]['disabled'][0],True)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][1],False)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][2],True)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][3],False)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][4],True)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][5],True)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][6],False)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][7],True)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][8],False)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][9],False)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][10],False)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][11],True)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][12],True)
        self.assertEqual(response['Days'][1]['room'][2]['disabled'][13],False)

        self.assertEqual(response['Days'][1]['room'][2]['money'],2)
        self.assertEqual(response['Days'][1]['room'][2]['multiMoney'],20)

        self.assertEqual(response['Days'][2]['room'][1]['name'],'303')
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][0],True)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][1],True)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][2],True)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][3],True)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][4],True)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][5],False)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][6],False)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][7],False)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][8],False)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][9],False)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][10],False)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][11],False)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][12],False)
        self.assertEqual(response['Days'][2]['room'][1]['disabled'][13],False)
        self.assertEqual(response['Days'][2]['room'][1]['money'],2)
        self.assertEqual(response['Days'][2]['room'][1]['multiMoney'],20)

    def clear(self):
        UserGroup.objects.all().delete()
        User.objects.all().delete()
        PianoRoom.objects.all().delete()
        TimeTable.objects.all().delete()

#预约
class book(TestCase):
    def setUp(self):
        #创建用户组
        UserGroup.objects.create(group_name = "校内学生", xinghaiPR_price=1,smallPR_price=2,bigPR_price=3)
        student = UserGroup.objects.get(group_name = "校内学生")
        #创建用户
        User.objects.create(open_id = "1",person_id = "123",pwhash = "123",name="user1",group=student)
        User.objects.create(open_id = "2",person_id = "1234",pwhash = "1234",name="user2",group=student)
        badguy = User.objects.create(open_id = "3",person_id = "12345",pwhash = "12345",name="black",group=student)
        #增加黑名单
        BlackList.objects.create(person_id = badguy,name = "black",group = student, reason='whatever')
        #创建琴房
        PianoRoom.objects.create(room_id = 101, piano_type = 2,status = True)
        room = PianoRoom.objects.get(room_id = 101)
        room.user_group.add(student)
        room.save()
        #创建时间表
        TimeTable.objects.create(piano_room = room, TT_type=0,date = datetime.date.today(),
                                    Time1 = 0,Time2 = 0,Time3 = 0,Time4 = 0,Time5 = 0,
                                    Time6 = 0,Time7 = 0,Time8 = 0,Time9 = 0,Time10 = 0,
                                    Time11 = 0,Time12 = 0,Time13 = 0,Time14 = 0)
        TimeTable.objects.create(piano_room = room, TT_type=1,date = datetime.date.today()+datetime.timedelta(1),
                                    Time1 = 1,Time2 = 1,Time3 = 1,Time4 = 1,Time5 = 1,
                                    Time6 = 1,Time7 = 1,Time8 = 1,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 1,Time13 = 1,Time14 = 1)
        TimeTable.objects.create(piano_room = room, TT_type=2,date = datetime.date.today()+datetime.timedelta(2),
                                    Time1 = 1,Time2 = 1,Time3 = 1,Time4 = 1,Time5 = 1,
                                    Time6 = 1,Time7 = 1,Time8 = 1,Time9 = 1,Time10 = 1,
                                    Time11 = 1,Time12 = 1,Time13 = 1,Time14 = 1)

    #用户未绑定
    def test_noUser(self):
        openId = "0"
        single = True 
        booklist = [
            {
                'day': 1,
                'room': '101',
                'time':['Time1','Time2']
            }
        ]
        data = {
            'bookTime':booklist,
            'single':single,
            'openId':openId
        }
        book = self.client.post("/api/book",data,content_type="application/json")
        response = json.loads(book.content)
        self.assertEqual(response['errMsg'],"您尚未绑定!")
    
    #用户黑名单
    def test_black(self):
        openId = "3"
        #单人
        single = True 
        booklist = [
            {
                'day': 1,
                'room': '101',
                'time':['Time1','Time2']
            }
        ]
        data = {
            'bookTime':booklist,
            'single':single,
            'openId':openId
        }
        book = self.client.post("/api/book",data,content_type="application/json")
        response = json.loads(book.content)
        self.assertEqual(response['errMsg'],"您已被加入黑名单,请联系管理员")

    #选择时间已经被使用
    def test_usedTime(self):
        openId = "1"
        single = True 
        booklist = [
            {
                'day': 0,
                'room': '101',
                'time':['Time1','Time2']
            }
        ]
        data = {
            'bookTime':booklist,
            'single':single,
            'openId':openId
        }
        book = self.client.post("/api/book",data,content_type="application/json")
        response = json.loads(book.content)
        self.assertEqual(response['errMsg'],"所选时间已被占用或无法使用!")
    
    #成功预订
    def test_book(self):
        openId = "1"
        single = True 
        booklist = [
            {
                'day': 1,
                'room': '101',
                'time':['Time1','Time2']
            }
        ]
        data = {
            'bookTime':booklist,
            'single':single,
            'openId':openId
        }
        book = self.client.post("/api/book",data,content_type="application/json")
        response = json.loads(book.content)
        disabled1 = []
        disabled2 = []
        for i in range(0,14):
            disabled1.append(False)
            disabled2.append(True)
        self.assertEqual(response['times'][0]['day'],0)
        for i in range(0,14):
            self.assertEqual(response['times'][0]['disabled'][i],disabled2[i])
        self.assertEqual(response['times'][0]['room'],'101')

        self.assertEqual(response['times'][1]['day'],1)
        for i in range(0,2):
            self.assertEqual(response['times'][1]['disabled'][i],True)
        for i in range(2,14):
            self.assertEqual(response['times'][1]['disabled'][i],False)
        self.assertEqual(response['times'][1]['room'],'101')

        self.assertEqual(response['times'][2]['day'],2)
        for i in range(0,14):
            self.assertEqual(response['times'][2]['disabled'][i],disabled1[i])
        self.assertEqual(response['times'][2]['room'],'101')

    def clear(self):
        UserGroup.objects.all().delete()
        User.objects.all().delete()
        BlackList.objects.all().delete()
        PianoRoom.objects.all().delete()
        TimeTable.objects.all().delete()

#是否绑定
class isBind(TestCase):
    def setUp(self):
        UserGroup.objects.create(group_name = "校内学生", xinghaiPR_price=1,smallPR_price=2,bigPR_price=3)
        student = UserGroup.objects.get(group_name = "校内学生")
        User.objects.create(open_id = "1",person_id = "123",pwhash = "123",name="user1",group=student)
    #未绑定
    def test_noUser(self):
        openId = "0"
        response = self.client.get("/api/isBind",{'openId':openId})
        response = json.loads(response.content)
        self.assertEqual(response['errMsg'],"no")
    #已经绑定
    def test_isUser(self):
        openId = "1"
        response = self.client.get("/api/isBind",{'openId':openId})
        response = json.loads(response.content)
        self.assertEqual(response['name'],"user1")
        self.assertEqual(response['personId'],"123")

    def clear(self):
        User.objects.all().delete()
        UserGroup.objects.all().delete()

#取消绑定
class cancelBind(TestCase):
    def setUp(self):
        UserGroup.objects.create(group_name = "校内学生", xinghaiPR_price=1,smallPR_price=2,bigPR_price=3)
        student = UserGroup.objects.get(group_name = "校内学生")
        User.objects.create(open_id = "1",person_id = "123",pwhash = "123",name="user1",group=student)

    def test_noUser(self):
        openId = "0"
        response = self.client.get("/api/notBind",{'openId':openId})
        response = json.loads(response.content)
        self.assertEqual(response['errMsg'],"no") 

    def test_isUser(self):
        openId = "1"
        response = self.client.get("/api/notBind",{'openId':openId})
        response = json.loads(response.content)
        self.assertEqual(response['notBind'],"ok")
    
    def clear(self):
        UserGroup.objects.all().delete()
        User.objects.all().delete()

class Login(TestCase):
    def setUp(self):
        UserGroup.objects.create(group_name = "校内学生", xinghaiPR_price=1,smallPR_price=2,bigPR_price=3)
        student = UserGroup.objects.get(group_name = "校内学生")
        User.objects.create(open_id = "1",person_id = "123",pwhash = "123",name="user1",group=student)

    def test_wrongcellphone(self):
        data = {
            'openId': "1",
            'cellPhone': '1234',
            'hash': '123'
        }
        response = self.client.post("/api/pwlogin",data, content_type = "application/json")
        response = json.loads(response.content)
        self.assertEqual(response['errMsg'],"用户名或密码错误!")

    def test_wronghash(self):
        data = {
            'openId': "1",
            'cellPhone': '123',
            'hash': '1234'
        }
        response = self.client.post("/api/pwlogin",data,content_type="application/json")
        response = json.loads(response.content)
        self.assertEqual(response['errMsg'],"用户名或密码错误!")

    def clear(self):
        UserGroup.objects.all().delete()
        User.objects.all().delete()