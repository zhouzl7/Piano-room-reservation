import xadmin

from .models import UserGroup, ArtTroupeMember, User, BlackList

#xadmin中这里是继承object，不再是继承admin
class UserGroupAdmin(object):
    # 显示的列
    list_display = ['group_name', 'xinghaiPR_price', 'smallPR_price', 'bigPR_price']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['group_name', 'xinghaiPR_price', 'smallPR_price', 'bigPR_price']
    # 过滤
    list_filter = ['group_name', 'xinghaiPR_price', 'smallPR_price', 'bigPR_price']

xadmin.site.register(UserGroup, UserGroupAdmin)

class ArtTroupeMemberAdmin(object):
    # 显示的列
    list_display = ['name', 'student_id']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'student_id']
    # 过滤
    list_filter = ['name', 'student_id']

xadmin.site.register(ArtTroupeMember, ArtTroupeMemberAdmin)

class UserAdmin(object):
    # 显示的列
    list_display = ['name', 'person_id', 'open_id', 'group']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'person_id', 'open_id', 'group']
    # 过滤
    list_filter = ['name', 'person_id', 'open_id', 'group']

xadmin.site.register(User, UserAdmin)

class BlackListAdmin(object):
    # 显示的列
    list_display = ['name', 'person_id', 'open_id', 'group']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'person_id', 'open_id', 'group']
    # 过滤
    list_filter = ['name', 'person_id', 'open_id', 'group']

xadmin.site.register(BlackList, BlackListAdmin)
