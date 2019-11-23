from django.contrib import admin

# Register your models here.

from rbac import models


class RoleAdmin(admin.ModelAdmin):
    list_display = ['title']
    filter_horizontal = ("permission",)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name','url',]

class MenuAdmin(admin.ModelAdmin):
    list_display = ['title','icon','priority']

class UserAdmin(admin.ModelAdmin):
    list_display = ["username","nickname","phone","last_login"]
    filter_horizontal = ("role","user_permissions","groups",)
    search_fields = ['username',"role__title"]
    #
    # def get_readonly_fields(self,request,obj=None):
    #     """限制普通用户修改"""
    #     if request.user.is_superuser:
    #         self.readonly_fields = []
    #     return self.readonly_fields

    readonly_fields = ("password",)

admin.site.register(models.UserInfo,UserAdmin)
admin.site.register(models.Role,RoleAdmin)
admin.site.register(models.Menu,MenuAdmin)
admin.site.register(models.Permission,PermissionAdmin)

#修改网页title和站点header。
admin.site.site_title = "运维管理平台"
admin.site.site_header = "运维管理平台"