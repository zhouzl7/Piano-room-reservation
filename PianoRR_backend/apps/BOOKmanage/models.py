from django.db import models

from codex.baseerror import LogicError
from USERmanage.models import User
from PRmanage.models import PianoRoom

# Create your models here.

class BookRecord(models.Model):
    # 取消预约
    STATUS_CANCELLED = 0
    # 未赴约
    STATUS_VALID = 1
    # 已赴约
    STATUS_USED = 2
 
    user = models.CharField(u'学号/教职工号/手机号', max_length=32)
    fee = models.IntegerField(u'费用 /元')
    is_pay = models.BooleanField(u'缴费情况', choices=((
                                            True, '已缴费'), (False, '待缴费')))
    user_quantity = models.BooleanField(u'单人/多人', choices=((True, '单人'), (False, '多人')))
    BR_date = models.DateField(u'日期')
    use_time = models.IntegerField(u'时间段', choices=((1, u'8-9'), (2, u'9-10'), (3, u'10-11'), (4, u'11-12'),
                                                    (5, u'12-13'), (6, u'13-14'), (7, u'14-15'), (8, u'15-16'),
                                                    (9, u'16-17'), (10, u'17-18'), (11, u'18-19'), (12, u'19-20'),
                                                    (13, u'20-21'), (14, u'21-22'))
                                   )
    status = models.IntegerField(u'状态', choices=((
                                    STATUS_CANCELLED, '已取消'), (STATUS_VALID, '未赴约'), (STATUS_USED, '已赴约')))
    piano_room = models.ForeignKey(PianoRoom, on_delete=models.CASCADE, verbose_name='琴房')
    pay_id = models.CharField(max_length=32)
    class Meta:
        verbose_name = '预约记录'
        verbose_name_plural = verbose_name

