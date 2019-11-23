# -*- coding: utf-8 -*-
# @Time    : 2019-11-23 10:57
# @Author  : kbsonlong
# @Email   : kbsonlong@gmail.com
# @Blog    : www.alongparty.cn
# @File    : decorators.py
# @Software: PyCharm
import traceback
from django.contrib.auth.mixins import AccessMixin,LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from rbac.models import RequestRecord,Role

User = get_user_model()

class LoginPermissionRequired(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            iUser = User.objects.get(username="{}".format(request.user))
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ipaddr = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ipaddr = request.META['REMOTE_ADDR']

            if request.method == "POST":
                request_type = 1
            else:
                request_type = 0
            ##写入访问记录
            h = RequestRecord(ipaddr=ipaddr, type=request_type, get_full_path=request.get_full_path())
            h.username = iUser
            h.save()
        except Exception as e:
            traceback.print_exc()
            return HttpResponseRedirect(settings.LOGIN_URL)

        return super().dispatch(request, *args, **kwargs)