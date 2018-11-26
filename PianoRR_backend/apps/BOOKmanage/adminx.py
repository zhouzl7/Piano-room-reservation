import xadmin

from .models import BookRecord

#xadmin中这里是继承object，不再是继承admin
class BookRecordAdmin(object):
    # 显示的列
    list_display = ['user', 'fee', 'is_pay', 'user_quantity', 'start_time', 'end_time', 'status', 'piano_room']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['user', 'fee', 'is_pay', 'user_quantity', 'status', 'piano_room']
    # 过滤
    list_filter = ['user', 'fee', 'is_pay', 'user_quantity', 'start_time', 'end_time', 'status', 'piano_room']

xadmin.site.register(BookRecord, BookRecordAdmin)
