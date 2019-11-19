

### 注册rbac到项目

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rbac.apps.RbacConfig',  ##注册rbac
]
```

### 添加中间件
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middlewares.permission.PermissionMiddleware',  ##添加自定义中间件
]

```


### 配置认证用户表和白名单

```python
AUTH_USER_MODEL = "rbac.UserInfo"

# 配置白名单
WHITE_URL_LIST = [
    r'^/',
    r'^/admin/.*',  # 放行admin应用url
    r'^/login/',
    r'^/register/',
    r'^/get_auth_img/',
]
```


### 动态加载菜单栏

```html
<ul class="sidebar-menu" data-widget="tree">
    {% load rbac %}
    {% get_menu request %}
</ul>
```