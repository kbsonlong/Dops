#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
# by leoiceo

from __future__ import unicode_literals
import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate,login,logout,get_user_model

from rbac.models import RequestRecord

User = get_user_model()

class UserLoginView(FormView):
    template_name = 'rbac/login.html'
    model = User

    def get_context_data(self, **kwargs):
        context = {}
        kwargs.update(context)

    def post(self, request, *args, **kwargs):

        if 'HTTP_X_FORWARDED_FOR' in self.request.META:
            ipaddr = self.request.META['HTTP_X_FORWARDED_FOR']
        else:
            ipaddr = self.request.META['REMOTE_ADDR']
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")
        check_code = request.POST.get('checkcode')
        user = authenticate(username=username, password=password)
        session_code = request.session["authcode"]

        if check_code.strip().lower() != session_code.lower():
            login_err = _('Did you slip the wrong hand? try again')
        else:
            if user is not None:  # pass authencation
                if user.is_active == False:
                    login_err = _('Warning, {} has been disabled'.format(user.username))
                    return render(request, 'login.html', {'login_err': login_err})
                login(self.request, user)
                userprofile = User.objects.get(username=user.username)
                h = RequestRecord(ipaddr=ipaddr, type=1, get_full_path=self.request.get_full_path())
                h.username = userprofile
                h.save()
                login_limit_info = User.objects.filter(username=username)
                login_limit_info.update(limit=0,login_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = {
            'messages': 'Logout success',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)