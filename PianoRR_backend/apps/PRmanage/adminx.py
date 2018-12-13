import xadmin

from .models import PianoRoom, Announcement, TimeTable

#xadmin中这里是继承object，不再是继承admin
class PianoRoomAdmin(object):
    # 显示的列
    list_display = ['room_id', 'piano_type', 'user_group', 'status']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['room_id', 'piano_type', 'user_group']
    # 过滤
    list_filter = ['room_id', 'piano_type', 'user_group', 'status']

    # 不可进入更新界面
    # list_display_links = ['id']

    # 直接编辑
    list_editable = ['status']

    #readonly_fields = ['room_id']

    def get_readonly_fields(self):
        path = self.request.get_full_path()
        if "update" in path:
            return ['room_id', ]  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

    # 是否显示书签
    show_bookmarks = False

xadmin.site.register(PianoRoom, PianoRoomAdmin)

class TimeTableAdmin(object):
    # 显示的列
    list_display = ['piano_room', 'TT_type', 'Time1', 'Time2', 'Time3', 'Time4', 'Time5', 'Time6', 'Time7',
                    'Time8', 'Time9', 'Time10', 'Time11', 'Time12', 'Time13', 'Time14']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['piano_room', 'TT_type', 'Time1', 'Time2', 'Time3', 'Time4', 'Time5', 'Time6', 'Time7',
                     'Time8', 'Time9', 'Time10', 'Time11', 'Time12', 'Time13', 'Time14']
    # 过滤
    list_filter = ['piano_room', 'TT_type', 'date', 'Time1', 'Time2', 'Time3', 'Time4', 'Time5', 'Time6', 'Time7',
                   'Time8', 'Time9', 'Time10', 'Time11', 'Time12', 'Time13', 'Time14']

    # 直接编辑
    list_editable = ['Time1', 'Time2', 'Time3', 'Time4', 'Time5', 'Time6', 'Time7',
                     'Time8', 'Time9', 'Time10', 'Time11', 'Time12', 'Time13', 'Time14']

    # 是否显示书签
    show_bookmarks = False

    # def has_add_permission(self):
    #     return False

    # 不可进入更新界面
   # list_display_links = ['id']

    def get_readonly_fields(self):
        path = self.request.get_full_path()
        if "update" in path:
            return ['piano_room', 'TT_type', 'date']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

xadmin.site.register(TimeTable, TimeTableAdmin)

class AnnouncementAdmin(object):
    # 显示的列
    list_display = ['title', 'published_time', 'published_person']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['title', 'published_person']
    # 过滤
    list_filter = ['title', 'published_time', 'published_person']

    # 是否显示书签
    show_bookmarks = False

xadmin.site.register(Announcement, AnnouncementAdmin)