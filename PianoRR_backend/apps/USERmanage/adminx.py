import xadmin
from xadmin.layout import Fieldset

from .models import UserGroup, ArtTroupeMember, User, BlackList

#xadmin中这里是继承object，不再是继承admin
class UserGroupAdmin(object):
    # 显示的列
    list_display = ['group_name', 'xinghaiPR_price', 'smallPR_price', 'bigPR_price']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['group_name', 'xinghaiPR_price', 'smallPR_price', 'bigPR_price']
    # 过滤
    list_filter = ['group_name', 'xinghaiPR_price', 'smallPR_price', 'bigPR_price']

    # 直接编辑
    list_editable = ['xinghaiPR_price', 'smallPR_price', 'bigPR_price']

    # 是否显示书签
    show_bookmarks = False

    # 不可进入更新界面
   # list_display_links = ['id']

    def get_readonly_fields(self):
        path = self.request.get_full_path()
        if "update" in path:
            return ['group_name']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

xadmin.site.register(UserGroup, UserGroupAdmin)

class ArtTroupeMemberAdmin(object):
    # 显示的列
    list_display = ['name', 'student_id']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'student_id']
    # 过滤
    list_filter = ['name', 'student_id']

    # 是否显示书签
    show_bookmarks = False

xadmin.site.register(ArtTroupeMember, ArtTroupeMemberAdmin)

class UserAdmin(object):
    # 显示的列
    list_display = ['name', 'person_id', 'group']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'person_id', 'group__group_name']
    # 过滤
    list_filter = ['name', 'person_id', 'group']

    # 是否显示书签
    show_bookmarks = False

    # 不可进入更新界面
   # list_display_links = ['id']

    def has_add_permission(self):
         return False

    def get_readonly_fields(self):
        path = self.request.get_full_path()
        if "update" in path:
            return ['name', 'person_id', 'pwhash', 'open_id']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

xadmin.site.register(User, UserAdmin)

class BlackListAdmin(object):
    # 显示的列
    list_display = ['name', 'person_id', 'group']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'person_id', 'group__group_name']
    # 过滤
    list_filter = ['name', 'person_id', 'group']

    # 是否显示书签
    show_bookmarks = False

    # 不可进入更新界面
   # list_display_links = ['id']

    def get_readonly_fields(self):
        path = self.request.get_full_path()
        if "update" in path:
            return ['name', 'person_id', 'group']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

xadmin.site.register(BlackList, BlackListAdmin)
