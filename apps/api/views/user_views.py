from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from api.serializers.user_serializers import *
# Create your views here.
from rbac import models

class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.UserInfo.objects.all().order_by('id')
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = models.Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = models.Menu.objects.all().order_by('id')
    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAuthenticated,)