from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.

# 扩展的用户表
class UserInfo(AbstractUser):
    """用户信息表"""
    id = models.AutoField(primary_key=True)
    gender_type = (("male", "男"), ("female", "女"))
    nickname = models.CharField(max_length=100,verbose_name="用户昵称",blank=True,null=True)
    gender = models.CharField(choices=gender_type, null=True, max_length=12)
    phone = models.CharField(max_length=11, null=True, unique=True)
    role = models.ManyToManyField("Role",blank=True)
    limit = models.IntegerField(default=0, blank=True, verbose_name=_('Login Limit'))
    login_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Login By'))
    valid_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Valid Date'))
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('User Comment'))

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name


# 身份表
class Role(models.Model):
    title = models.CharField(verbose_name="职位", max_length=32)
    permission = models.ManyToManyField("Permission")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name


# 权限表
class Permission(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'权限名')
    url = models.CharField(
        max_length=300,
        verbose_name=u'权限url地址',
        null=True,
        blank=True,
        help_text=u'是否给菜单设置一个url地址'
    )
    icon = models.CharField(
        max_length=32,
        verbose_name='权限图标',
        null=True,
        blank=True
    )
    # 指定属于哪个父级权限
    parent = models.ForeignKey(
        'self',
        verbose_name=u'父级权限',
        null=True,
        blank=True,
        help_text=u'如果添加的是子权限，请选择父权限',
        on_delete=models.CASCADE
    )

    # 指定属于哪个menu
    menu = models.ForeignKey(to="Menu",verbose_name=u'对应菜单',blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        verbose_name = u"权限表"
        verbose_name_plural = u"权限表"
        ordering = ["id"]

# 菜单表
class Menu(models.Model):
    title = models.CharField(max_length=32, verbose_name=u'菜单名')
    # 菜单显示图标
    icon = models.CharField(
        max_length=32,
        verbose_name='菜单图标',
        null=True,
        blank=True
    )
    # 指定属于哪个父级菜单
    parent = models.ForeignKey(
        'self',
        verbose_name=u'父级菜单',
        null=True,
        blank=True,
        help_text=u'如果添加的是子菜单，请选择父菜单',
        on_delete=models.CASCADE
    )

    priority = models.IntegerField(
        verbose_name=u'显示优先级',
        null=True,
        blank=True,
        help_text=u'菜单的显示顺序，优先级越小显示越靠前'
    )
    is_show = models.BooleanField(verbose_name="是否导航栏显示",default=False,blank=True)
    memu_level = models.SmallIntegerField(verbose_name="菜单等级",default=1,blank=True)

    def __str__(self):
        return "{parent}{title}".format(title=self.title, parent="%s-->" % self.parent.title if self.parent else '')

    class Meta:
        verbose_name = u"菜单表"
        verbose_name_plural = u"菜单表"
        ordering = ["priority","id"]  # 根据优先级和id来排序


class RequestRecord(models.Model):
    """
    访问记录
    """
    login_type = (
        (0, 'GET'),
        (1, 'POST'),
    )
    username = models.ForeignKey(to="UserInfo", verbose_name=_("UserName"), blank=True, null=True,
                                 on_delete=models.SET_NULL)
    ipaddr = models.GenericIPAddressField(verbose_name=_("Client Address"))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_("Request Date Time"))
    type = models.IntegerField(choices=login_type, verbose_name=_("Request Type"))
    get_full_path = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("Request Full Path"))
    post_body = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_("Request Post Body"))


    class Meta:
        db_table = "requestrecord"
        verbose_name = _('Request Record')
        verbose_name_plural = _('Request Record')

    def __str__(self):
        return self.username