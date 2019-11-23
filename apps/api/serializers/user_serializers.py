# -*- coding: utf-8 -*-
# @Time    : 2019-07-29 18:05
# @Author  : kbsonlong
# @Email   : kbsonlong@gmail.com
# @Blog    : www.alongparty.cn
# @File    : user_serializers.py
# @Software: PyCharm
from rest_framework import serializers

from rbac import models


class UsersSerializer(serializers.ModelSerializer):
    """
    用户管理
    """
    class Meta:
        model = models.UserInfo
        fields = ('id', 'username', 'phone', 'is_superuser', 'is_active', 'groups', 'user_permissions')



class PermissionSerializer(serializers.ModelSerializer):
    """
    权限管理
    """
    class Meta:
        model = models.Permission
        fields = ('id', 'name')


class RoleSerializer(serializers.ModelSerializer):
    """
    用户角色管理
    """
    class Meta:
        model = models.Role
        fields = ('id', 'name', 'user_set', 'permissions')


class MenuSerializer(serializers.ModelSerializer):
    """
    菜单管理
    """
    class Meta:
        model = models.Menu
        fields = '__all__'

