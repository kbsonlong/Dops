#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
# by leoiceo

from __future__ import unicode_literals
import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView,View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.conf import settings
from rbac.service import init_permission, authcode

User = get_user_model()

class UserLoginView(FormView):
    template_name = 'login.html'
    model = User

    def get_context_data(self, **kwargs):
        context = {}
        kwargs.update(context)

    def get(self, request, *args, **kwargs):
        next_url = self.request.GET.get('next')
        request.session['next_url'] = next_url
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        check_code = self.request.POST.get('authcode')
        user = authenticate(username=username, password=password)
        # session_code = request.session["authcode"]
        session_code = check_code

        # if check_code.strip().lower() != session_code.lower():
        if check_code.lower() != session_code.lower():
            login_err = _('Did you slip the wrong hand? try again')
        else:
            if user is not None:  # pass authencation
                if user.is_active == False:
                    login_err = _('Warning, {} has been disabled'.format(user.username))
                    return render(request, 'login.html', {'login_err': login_err})
                login(self.request, user)
                init_permission.init_permission(request, user)  # 调用权限注入函数，注入用户权限

                login_limit_info = User.objects.filter(username=username)
                login_limit_info.update(limit=0,login_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                next_url =  request.session.get('next_url')
                if next_url:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect('/')
            else:
                try:
                    limit_num = 5
                    curr_login_limit = User.objects.get(username=username).login_limit
                    new_login_limit = int(curr_login_limit) + 1
                    login_limit_info = User.objects.filter(username=username)
                    if new_login_limit == 5:
                        login_limit_info.update(limit=new_login_limit, is_active=0)
                        login_err = _("Warning: {} has been disabled, please contact the administrator".format(username))
                    else:
                        login_limit_info.update(limit=new_login_limit)
                        login_err = _("Warning: {} remaining attempts are {}".format(username, limit_num - new_login_limit))
                except Exception as e:
                    login_err = _('Verification failed? Think again ^.^')

        return render(request, 'login.html', {'login_err': login_err})



class UserLogoutView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(settings.LOGIN_URL)

    def get_context_data(self, **kwargs):
        context = {
            'messages': 'Logout success',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

# 验证码视图类
class GetAuthImg(View):
    """获取验证码视图类"""

    def get(self, request):
        data = authcode.get_authcode_img(request)
        print("验证码：", request.session.get("authcode"))
        return HttpResponse(data)