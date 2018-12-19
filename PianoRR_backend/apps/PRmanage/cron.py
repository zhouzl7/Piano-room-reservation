# _*_ coding: utf-8 _*_
# Create your views here.
from PRmanage.models import PianoRoom, TimeTable

import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import datetime

try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")


    # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
    # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次
    @register_job(scheduler, 'cron', minute='59', second='59', id='task_time')
    def test_job():
        t_now = time.localtime()
        all_time_tables = TimeTable.objects.all()

        hour_now = t_now.tm_hour

        if int(hour_now) >= 7 and int(hour_now) <= 20:
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

        if int(hour_now) == 23:
            time_tables = TimeTable.objects.filter(TT_type='0')

            for time_table in time_tables:
                time_table.delete()

            time_tables = TimeTable.objects.filter(TT_type='1')

            for time_table in time_tables:
                time_table.TT_type = '0'
                time_table.date = datetime.date.today() + datetime.timedelta(days=1)
                time_table.save()

            time_tables = TimeTable.objects.filter(TT_type='2')

            for time_table in time_tables:
                time_table.TT_type = '1'
                time_table.date = datetime.date.today() + datetime.timedelta(days=2)
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
                                           Time13=1, Time14=1)
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
