# -*- coding: utf-8 -*-
# @Time    : 2019-11-23 12:25
# @Author  : kbsonlong
# @Email   : kbsonlong@gmail.com
# @Blog    : www.alongparty.cn
# @File    : user.py
# @Software: PyCharm

from django.views.generic import ListView
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse

from rbac import models
from rbac.service.decorators import LoginPermissionRequired

class UserListView(LoginPermissionRequired,ListView):
    model = models.UserInfo
    template_name = "users/user_list.html"
    context_object_name = "users"


class RoleListView(LoginPermissionRequired,ListView):
    model = models.Role
    template_name = "users/user-list.html"
    context_object_name = "users"


class PermissionListView(LoginPermissionRequired,ListView):
    model = models.Permission
    template_name = "users/user-list.html"
    context_object_name = "users"


class MenuListView(LoginPermissionRequired,ListView):
    model = models.Menu
    template_name = "users/user-list.html"
    context_object_name = "users"


def create_user(request):
    if request.method == 'POST':
        # print(len(request.POST.get('phone')))
        try:
            user_obj = models.UserInfo.objects.create(
                username=request.POST.get('username'),
                password=make_password('123456'),
                is_superuser=request.POST.get('is_superuser'),
                is_active=request.POST.get('is_active'),
                phone=int(request.POST.get('phone'))
            )

            data = {
                'id': user_obj.id,
                'username': user_obj.username,
                'is_superuser': user_obj.is_superuser,
                'is_active': user_obj.is_active,
                'mobile': user_obj.phone
            }
            print(request.POST)
            groups = request.POST.getlist('groups[]')
            print(groups)
            # if groups:
            #     for i in groups:
            #         group = Group.objects.get(id=i)
            #         user_obj.groups.add(group)

            # user_permissions = request.POST.getlist('user_permissions[]')
            # print(user_permissions)
            # if user_permissions:
            #     for i in user_permissions:
            #         permission = Permission.objects.get(id=i)
            #         user_obj.user_permissions.add(permission)

            return JsonResponse({"code": 200, "data": data, "msg": "用户添加成功！初始密码是123456"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 500, "data": None, "msg": "用户添加失败，原因：{}".format(e)})

def reset_password(request, pk):
    if request.method == 'POST':
        try:
            models.UserInfo.objects.filter(id=pk).update(
                password=make_password('123456')
            )

            return JsonResponse({"code": 200, "data": None, "msg": "密码重置成功！密码为123456"})
        except Exception as e:
            return JsonResponse({"code": 500, "data": None, "msg": "密码重置失败，原因：{}".format(e)})