import xadmin

from .models import BookRecord

#xadmin中这里是继承object，不再是继承admin
class BookRecordAdmin(object):
    # 显示的列
    list_display = ['name', 'person_id', 'piano_room', 'BR_date', 'use_time', 'fee', 'is_pay', 'user_quantity', 'status']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'person_id', 'piano_room__room_id', 'use_time', 'fee', 'is_pay', 'user_quantity', 'status']
    # 过滤
    list_filter = ['name', 'person_id', 'piano_room', 'BR_date', 'use_time', 'fee', 'is_pay', 'user_quantity', 'status']

    # 是否显示书签
    show_bookmarks = False

    # 直接编辑
    list_editable = ['is_pay', 'status']

    # 不可进入更新界面
   # list_display_links = ['id']

    def get_readonly_fields(self):
        path = self.request.get_full_path()
        if "update" in path:
            return ['name', 'person_id', 'piano_room', 'BR_date', 'use_time', 'fee', 'user_quantity', 'pay_id']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

    def has_add_permission(self):
        return False

xadmin.site.register(BookRecord, BookRecordAdmin)
