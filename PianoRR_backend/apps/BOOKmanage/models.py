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

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    fee = models.IntegerField(u'费用 /元')
    is_pay = models.BooleanField(u'缴费情况', choices=((
                                            True, '已缴费'), (False, '待缴费')))
    user_quantity = models.IntegerField(u'人数')
    start_time = models.DateTimeField(u'开始时间')
    end_time = models.DateTimeField(u'结束时间')
    status = models.IntegerField(u'状态', choices=((
                                    STATUS_CANCELLED, '已取消'), (STATUS_VALID, '未赴约'), (STATUS_USED, '已赴约')))
    piano_room = models.ForeignKey(PianoRoom, on_delete=models.CASCADE, verbose_name='琴房')

    class Meta:
        verbose_name = '预约记录'
        verbose_name_plural = verbose_name

