"""CRM URL Configuration

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
from django.urls import path,include
from rbac.views import login,user


app_name="rbac"

urlpatterns = [
    path('login/', login.UserLoginView.as_view(), name='login'),
    path('logout/', login.UserLogoutView.as_view(), name='logout'),
    path("get_auth_img/",login.GetAuthImg.as_view(),name="get_auth_img"),
    path("user/list/",user.UserListView.as_view(),name="user_list"),
    path("user/add/",user.create_user,name="user_add"),
    path("user/reset_pwd/<int:pk>/",user.reset_password,name="user_reset_pwd"),
    path("premission/list/",user.PermissionListView.as_view(),name="premission_list"),
    path("role/list/",user.RoleListView.as_view(),name="role_list"),
    path("menu/list/",user.MenuListView.as_view(),name="menu_list"),
    path("dept/list/",user.UserListView.as_view(),name="dept_list"),
]
