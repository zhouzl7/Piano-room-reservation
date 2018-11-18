import xadmin

from .models import PianoRoom, Announcement

#xadmin中这里是继承object，不再是继承admin
class PianoRoomAdmin(object):
    # 显示的列
    list_display = ['room_id', 'piano_type', 'open_time', 'close_time', 'user_group', 'status']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['room_id', 'piano_type', 'user_group']
    # 过滤
    list_filter = ['room_id', 'piano_type', 'open_time', 'close_time', 'user_group', 'status']

xadmin.site.register(PianoRoom, PianoRoomAdmin)

class AnnouncementAdmin(object):
    # 显示的列
    list_display = ['title', 'published_time', 'published_person']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['title', 'published_person']
    # 过滤
    list_filter = ['title', 'published_time', 'published_person']

xadmin.site.register(Announcement, AnnouncementAdmin)