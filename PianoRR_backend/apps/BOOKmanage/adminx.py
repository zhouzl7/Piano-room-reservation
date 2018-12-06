import xadmin

from .models import BookRecord

#xadmin中这里是继承object，不再是继承admin
class BookRecordAdmin(object):
    # 显示的列
    list_display = ['user', 'piano_room', 'BR_date', 'use_time', 'fee', 'is_pay', 'user_quantity', 'status']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['user', 'piano_room', 'use_time', 'fee', 'is_pay', 'user_quantity', 'status']
    # 过滤
    list_filter = ['user', 'piano_room', 'BR_date', 'use_time', 'fee', 'is_pay', 'user_quantity', 'status']

    # 是否显示书签
    show_bookmarks = False

xadmin.site.register(BookRecord, BookRecordAdmin)
