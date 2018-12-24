# _*_ coding: utf-8 _*_
# Create your views here.
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from BOOKmanage.models import BookRecord
from PRmanage.models import TimeTable

def is_pay(id_List):
    for record_id in id_List:
        record = BookRecord.objects.get(id=record_id)
        if not record.is_pay:
            piano_room = record.piano_room
            date = record.BR_date
            use_time = record.use_time
            time_table = TimeTable.objects.get(piano_room=piano_room, date=date)
            print(time_table.piano_room.room_id)
            time1 = datetime.datetime.now()
            time_delta = datetime.timedelta(seconds=300)
            time1 = time1 - time_delta
            if use_time == 1:
                time_table.Time1 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 7 and time1.minute >= 55:
                        time_table.Time1 = TimeTable.TIME_DISABLED
            elif use_time == 2:
                time_table.Time2 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 8 and time1.minute >= 55:
                        time_table.Time2 = TimeTable.TIME_DISABLED
            elif use_time == 3:
                time_table.Time3 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 9 and time1.minute >= 55:
                        time_table.Time3 = TimeTable.TIME_DISABLED
            elif use_time == 4:
                time_table.Time4 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 10 and time1.minute >= 55:
                        time_table.Time4 = TimeTable.TIME_DISABLED
            elif use_time == 5:
                time_table.Time5 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 11 and time1.minute >= 55:
                        time_table.Time5 = TimeTable.TIME_DISABLED
            elif use_time == 6:
                time_table.Time6 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 12 and time1.minute >= 55:
                        time_table.Time6 = TimeTable.TIME_DISABLED
            elif use_time == 7:
                time_table.Time7 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 13 and time1.minute >= 55:
                        time_table.Time7 = TimeTable.TIME_DISABLED
            elif use_time == 8:
                time_table.Time8 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 14 and time1.minute >= 55:
                        time_table.Time8 = TimeTable.TIME_DISABLED
            elif use_time == 9:
                time_table.Time9 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 15 and time1.minute >= 55:
                        time_table.Time9 = TimeTable.TIME_DISABLED
            elif use_time == 10:
                time_table.Time10 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 16 and time1.minute >= 55:
                        time_table.Time10 = TimeTable.TIME_DISABLED
            elif use_time == 11:
                time_table.Time11 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 17 and time1.minute >= 55:
                        time_table.Time11 = TimeTable.TIME_DISABLED
            elif use_time == 12:
                time_table.Time12 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 18 and time1.minute >= 55:
                        time_table.Time12 = TimeTable.TIME_DISABLED
            elif use_time == 13:
                time_table.Time13 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 19 and time1.minute >= 55:
                        time_table.Time13 = TimeTable.TIME_DISABLED
            elif use_time == 14:
                time_table.Time14 = TimeTable.TIME_ABLED
                if time_table.TT_type == TimeTable.TODAY:
                    if time1.hour == 20 and time1.minute >= 55:
                        time_table.Time14 = TimeTable.TIME_DISABLED
            time_table.save()
            record.status = record.STATUS_CANCELLED
            record.save()


# 倒计时5分钟，未支付则取消预约订单
def countDown(id_List):
    scheduler = BackgroundScheduler()
    print(datetime.datetime.now())
    run_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
    scheduler.add_job(is_pay, 'date', run_date=run_date, args=[id_List])
    scheduler.start()