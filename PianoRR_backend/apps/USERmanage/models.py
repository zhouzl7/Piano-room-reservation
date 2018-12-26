from django.db import models

from codex.baseerror import LogicError

# Create your models here.

class UserGroup(models.Model):
    group_name = models.CharField(u'组名', max_length=12, unique=True, db_index=True)
    xinghaiPR_price = models.IntegerField(u'星海琴房 元/时')
    smallPR_price = models.IntegerField(u'小琴房 元/时')
    bigPR_price = models.IntegerField(u'大琴房 元/时')

    class Meta:
        verbose_name = '用户组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group_name

class User(models.Model):
    open_id = models.CharField(u'open_id', max_length=64, unique=False, db_index=False, blank=True)
    person_id = models.CharField(u'学号/教职工号/手机号', max_length=32, unique=True, db_index=True)
    pwhash = models.CharField(u'密码', max_length=128, blank=True)
    name = models.CharField(u'姓名', max_length=12)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, verbose_name='用户组')

    @classmethod
    def get_by_personid(cls, personid):
        try:
            return cls.objects.get(person_id=personid)
        except cls.DoesNotExist:
            raise LogicError('User not found')

    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class ArtTroupeMember(models.Model):
    student_id = models.CharField(u'学生证号', max_length=32, unique=True, db_index=True)
    name = models.CharField(u'姓名', max_length=12)

    @classmethod
    def get_by_studentid(cls, studentid):
        try:
            return cls.objects.get(student_id=studentid)
        except cls.DoesNotExist:
            raise LogicError('ArtTroupeMember not found')

    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('ArtTroupeMember not found')

    class Meta:
        verbose_name = '艺术团'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class BlackList(models.Model):
    person_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='学号/工作证号/手机号', to_field='person_id')
    name = models.CharField(u'姓名', max_length=12)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, verbose_name='用户组')
    reason = models.TextField(u'拉黑理由', blank=True)

    @classmethod
    def get_by_personid(cls, personid):
        try:
            return cls.objects.get(person_id=personid)
        except cls.DoesNotExist:
            raise LogicError('BlackList member not found')

    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('BlackList member not found')

    class Meta:
        verbose_name = '黑名单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
