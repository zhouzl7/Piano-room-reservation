from django.db import models

from codex.baseerror import LogicError
from USERmanage.models import UserGroup

# Create your models here.

class PianoRoom(models.Model):
    # 不可用的
    STATUS_DISABLED = -1
    # 被预约的
    STATUS_RESERVED = 0
    # 可预约的
    STATUS_UNRESERVED = 1

    room_id = models.CharField(u'编号', max_length=10, unique=True, db_index=True)
    piano_type = models.CharField(u'类型', max_length=20)
    open_time = models.TimeField(u'开放时间', db_index=True)
    close_time = models.TimeField(u'关闭时间', db_index=True)
    STATUS_ENUM = (
        (STATUS_DISABLED, '停止使用'),
        (STATUS_RESERVED, '已被预约'),
        (STATUS_UNRESERVED, '可被预约'),
    )
    status = models.IntegerField(u'状态', choices=STATUS_ENUM)
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
