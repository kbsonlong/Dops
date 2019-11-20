# -*- coding: utf-8 -*-
# @Time    : 2019-11-20 22:29
# @Author  : kbsonlong
# @Email   : kbsonlong@gmail.com
# @Blog    : www.alongparty.cn
# @File    : utils.py
# @Software: PyCharm

from django.contrib.auth import get_user_model
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import AccessMixin,LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from rbac.models import Role,Permission

User = get_user_model()

class LoginPermissionRequired(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            iUser = User.objects.get(email="{}".format(request.user))
            if not iUser.is_superuser:
                role_permission = Role.objects.get(name=iUser.role.name)
                role_permission_list = role_permission.permission.all()
                matchUrl = []
                for x in role_permission_list:
                    if request.path == x.url or request.path.rstrip('/') == x.url:
                        matchUrl.append(x.url)
                    elif request.path.startswith(x.url):
                        matchUrl.append(x.url)

                if len(matchUrl) == 0:
                    return HttpResponseRedirect('/')
        except Exception as e:
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)
