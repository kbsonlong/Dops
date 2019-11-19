# -*- coding: utf-8 -*-
# @Time    : 2019-10-12 17:37
# @Author  : kbsonlong
# @Email   : kbsonlong@gmail.com
# @Blog    : www.alongparty.cn
# @File    : permission.py
# @Software: PyCharm

import re
from django.shortcuts import HttpResponse,redirect,render
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class PermissionMiddleware(MiddlewareMixin):
    """自定义权限分配中间件"""
    def process_request(self,request):
        # 对权限进行校验
        # 1. 当前访问的URL在不在白名单
        for i in settings.WHITE_URL_LIST:
            ret = re.search(i,request.path)
            if ret:
                return None

        # 获取当前用户的所有权限
        user = request.user
        if not user:
            return redirect("login")

        # 获取用户权限列表
        permissions_list = request.session.get("permissions_list")
        if permissions_list:
            for permission in permissions_list:  # 遍历权限列表，匹配当前路径，匹配上放行
                url = permission['url']
                if re.search(f"^{url}",request.path):
                    # 请求子权限路径，父级权限和父级菜单激活样式设置
                    request.session['show_id'] = permission["parent_id"]
                    return None

        # 没有匹配上，提示没有权限
        return HttpResponse("没有权限")