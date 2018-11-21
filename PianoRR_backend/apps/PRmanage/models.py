from django.db import models

from codex.baseerror import LogicError
from USERmanage.models import UserGroup
import datetime

# Create your models here.

class PianoRoom(models.Model):
    room_id = models.CharField(u'编号', max_length=10, unique=True, db_index=True)
    # 小琴房
    TYPE_SMALL = 0
    # 大琴房
    TYPE_BIG = 1
    # 星海钢琴
    TYPE_XINGHAI = 2
    piano_type = models.IntegerField(u'类型', choices=((0, '小琴房'), (1, '大琴房'), (2, '星海琴房')))
    status = models.BooleanField(u'状态', choices=((True, '开放使用'), (False, '关闭使用')), default=True)
    user_group = models.ManyToManyField(UserGroup, verbose_name='允许用户组')

    @classmethod
    def get_by_roomid(cls, roomid):
        try:
            return cls.objects.get(room_id=roomid)
        except cls.DoesNotExist:
            raise LogicError('Room not found')

    class Meta:
        verbose_name = '琴房信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.room_id

class TimeTable(models.Model):
    # 今天
    TODAY = 0
    # 明天
    TOMORROW = 1
    # 后天
    AFTER_TOMORROW = 2

    # 停止使用
    TIME_DISABLED = -1
    # 已被预约
    TIME_BOOKED = 0
    # 可被预约
    TIME_ABLED = 1

    piano_room = models.ForeignKey(PianoRoom, on_delete=models.CASCADE, default=None, verbose_name='琴房')
    date = models.IntegerField(u'日期', choices=((0, '今天'), (1, '明天'), (2, '后天')), default=0)
    Time1 = models.IntegerField(u'08-09', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time2 = models.IntegerField(u'09-10', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time3 = models.IntegerField(u'10-11', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time4 = models.IntegerField(u'11-12', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time5 = models.IntegerField(u'12-13', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time6 = models.IntegerField(u'13-14', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time7 = models.IntegerField(u'14-15', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time8 = models.IntegerField(u'15-16', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time9 = models.IntegerField(u'16-17', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time10 = models.IntegerField(u'17-18', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time11 = models.IntegerField(u'18-19', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time12 = models.IntegerField(u'19-20', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time13 = models.IntegerField(u'20-21', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)
    Time14 = models.IntegerField(u'21-22', choices=((-1, '停止使用'), (0, '已被预约'), (1, '可被预约')), default=1)

    class Meta:
        verbose_name = '时间表'
        verbose_name_plural = verbose_name

class Announcement(models.Model):
    title = models.CharField(u'标题', max_length=128)
    content = models.TextField(u'内容')
    published_time = models.DateTimeField(u'发布时间')
    published_person = models.CharField(u'发布者', max_length=12)
    class Meta:
        verbose_name = '琴房公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
