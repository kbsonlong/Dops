"""Dops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from cmdb import views

app_name = "cmdb"
urlpatterns = [
    path('product/list/', views.ProductListView.as_view(), name='product_list'),
    path('project/list/', views.ProjectListView.as_view(), name='project_list'),
    path('idc/list/', views.IdcListView.as_view(), name='idc_list'),
    path('env/list/', views.EnvListView.as_view(), name='env_list'),
    path('asset/list/', views.AssetListView.as_view(), name='asset_list'),
    path('asset-dumps/', views.assets_dumps, name='assets_dumps'),
]
