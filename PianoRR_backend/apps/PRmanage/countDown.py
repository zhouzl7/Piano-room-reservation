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
            setattr(time_table, 'Time' + str(use_time), TimeTable.TIME_ABLED)
            if time_table.TT_type == TimeTable.TODAY:
                if time1.hour == (use_time + 6) and time1.minute >= 55:
                    setattr(time_table, 'Time' + str(use_time), TimeTable.TIME_DISABLED)
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
