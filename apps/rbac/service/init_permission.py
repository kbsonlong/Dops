# -*- coding: utf-8 -*-
# @Time    : 2019-10-12 17:39
# @Author  : kbsonlong
# @Email   : kbsonlong@gmail.com
# @Blog    : www.alongparty.cn
# @File    : init_permission.py
# @Software: PyCharm

from rbac import models


def init_permission(request, user):
    """
    在登录函数验证通过后，在session中注入用户权限和用户菜单权限。
    :param request: 用户登录请求时的wsgi请求对象
    :param user: 用户登录验证通过后的用户账号名
    :return: none，
    """
    permissions = models.Permission.objects.filter(
        role__userinfo__username=user,
        menu__memu_level__lte=2).values(
        "pk", "name", "url", "icon",
        "parent_id", "menu__pk",
        "menu__title", "menu__icon",
        "menu__priority","menu__parent__id"
    ).order_by("menu__priority").distinct()
    # menu__memu_level__lte=2 查找一级和二级菜单, lte:小于等于,并根据menu__priority菜单显示优先级排序并去重

    permissions_list = []  # 定义权限列表
    menus_dict = {}  # 定义菜单列表

    print("当前用户权限>>>")
    for permission in permissions:  # 遍历权限列表

        # 获取用户权限的数据结构，列表套字典，一个字典代表一个权限
        permissions_list.append({
            "pk": permission["pk"],
            "name": permission["name"],
            "url": permission["url"],
            "parent_id": permission["parent_id"],
        })

        # 获取菜单权限的数据结构，字典套字典，一个字典代表一个菜单
        if not permission["parent_id"]:   # 当没有父节点时，说明此菜单为一级菜单
            menus_dict[permission["menu__pk"]] = {
                "pk": permission["menu__pk"],
                "title": permission["menu__title"],
                "icon": permission["menu__icon"],
                "parent_id": permission["menu__parent__id"],
                "priority": permission["menu__priority"],
                "children": []
                # "children": [{
                #     "pk": permission["pk"],
                #     "name": permission["name"],
                #     "url": permission["url"],
                #     "icon": permission["icon"],
                #     "parent_id": permission["parent_id"],
                # }]  # 定义一个父级菜单包含所有儿子菜单的空列表
            }

        else:   # 所有二级菜单加入到一级菜单的children列表
            menus_dict[permission["parent_id"]]["children"].append({
                "pk": permission["pk"],
                "name": permission["name"],
                "url": permission["url"],
                "icon": permission["icon"],
                "parent_id": permission["parent_id"],
            })

    print("权限列表",permissions_list)
    # print("菜单权限",menus_dict)

    # session中注入权限数据
    request.session["permissions_list"] = permissions_list

    # session中注入菜单数据
    request.session["menus_dict"] = menus_dict

