from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Product(models.Model):
    """
    业务线
    """
    name = models.CharField(max_length=150,verbose_name="业务名称")
    code = models.CharField(max_length=50,verbose_name="业务编码",null=True,blank=True)
    parent = models.ForeignKey("self",on_delete=models.CASCADE,verbose_name="上级业务",null=True,blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_created=True, blank=True)
    modity_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, blank=True)

    class Meta:
        verbose_name = "业务表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Project(models.Model):
    """
    项目表
    """
    name = models.CharField(max_length=150,verbose_name="项目名称")
    code = models.CharField(max_length=50,verbose_name="项目编码",null=True,blank=True)
    product = models.ForeignKey("Product",verbose_name="所属业务线",on_delete=models.CASCADE)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="leader", verbose_name="项目负责人",
                                       blank=True, null=True)
    members = models.ManyToManyField(User, verbose_name="项目成员", blank=True, related_name="members")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_created=True, blank=True)
    modity_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, blank=True)

    class Meta:
        verbose_name = "项目表"
        verbose_name_plural = verbose_name
        unique_together = ("product", "name")

    def __str__(self):
        return "{}-{}".format(self.product.name,self.name)

class IDC(models.Model):
    idc_name  = models.CharField(verbose_name="机房名称",max_length=255,unique=True)
    idc_contact = models.CharField(verbose_name="联系方式",max_length=255,null=True,blank=True)

    class Meta:
        verbose_name = "IDC机房"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.idc_name


class Env(models.Model):
    name = models.CharField(max_length=50,verbose_name="环境名称")
    code = models.CharField(max_length=50,verbose_name="环境标识")

    class Meta:
        verbose_name = "环境信息表"
        verbose_name_plural = verbose_name
        unique_together = ("name","code")

    def __str__(self):
        return self.name

class Asset(models.Model):
    type_choice = (
        ("server", "服务器"),
        ("network", "网络设备"),
        ("storage", "存储设备"),
        ("software", "软件资产"),
    )

    status_choice = (
        (0, "新购"),
        (1, "初始化"),
        (2, "备用"),
        (3, "在线"),
        (4, "故障"),
        (5, "下线"),
    )

    asset_type = models.CharField(choices=type_choice, verbose_name="资产类型", max_length=64, default="server", blank=True)
    name = models.CharField(max_length=150, verbose_name="资产名称")
    sn = models.CharField(max_length=100,verbose_name="资产编码")
    asset_project = models.ForeignKey(to="Project", on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="所属项目", related_name="project")
    status = models.SmallIntegerField(choices=status_choice, verbose_name="资产状态", default=0, blank=True)
    idc = models.ForeignKey(to="IDC", on_delete=models.SET_NULL, related_name="idc", null=True, blank=True,
                                  verbose_name="所属机房")
    create_time = models.DateTimeField(auto_now=True, blank=True, verbose_name="采购时间")
    modity_time = models.DateTimeField(auto_now=True, blank=True, verbose_name="修改时间")
    remark = models.TextField(verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = "资产总表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Server(models.Model):
    sub_type_chioce = (
        (0, "物理机"),
        (1, "虚拟机"),
        (2, "云主机"),
    )

    asset = models.OneToOneField(to="Asset", on_delete=models.CASCADE)  ##与资产信息总表一对一关联
    sub_asset_type = models.SmallIntegerField(choices=sub_type_chioce, default=0, verbose_name="服务器类型")
    server_model = models.CharField(max_length=100, verbose_name="服务器型号", null=True, blank=True)
    hostname = models.CharField(max_length=150, verbose_name="主机名称")
    public_ip = models.GenericIPAddressField(verbose_name="公网地址", unique=True)
    intranet_ip = models.GenericIPAddressField(verbose_name="内网地址", blank=True, null=True)
    host_on = models.ForeignKey(to="self", on_delete=models.CASCADE, related_name="host_on_server", verbose_name="宿主机",
                                null=True, blank=True)
    os = models.CharField(verbose_name="操作系统版本", max_length=100, default="Centos 7.5", blank=True)
    env = models.ForeignKey(to="Env", on_delete=models.SET_NULL, null=True, blank=True, related_name="env")
    cpu = models.CharField(max_length=50, verbose_name="cpu核数", null=True, blank=True)
    memory = models.CharField(max_length=100, verbose_name="内存大小", null=True, blank=True)
    disk = models.CharField(max_length=100, verbose_name="磁盘大小", null=True, blank=True)
    server_remark = models.TextField(verbose_name="服务器备注", null=True, blank=True)

    class Meta:
        verbose_name = "服务器表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}-{}".format(self.asset.name,self.public_ip)

class Service(models.Model):
    type_chioce = (
        (0, "消息队列"),
        (1, "数据库"),
        (2, "中间件"),
    )
    cluster_chioce = (
        ("standlone", "单机模式"),
        ("main-subordinate", "主从模式"),
        ("cluster", "高可用模式"),
    )
    name = models.CharField(verbose_name="服务名称", max_length=100)
    version = models.CharField(verbose_name="服务版本", max_length=100, blank=True)
    service_type = models.SmallIntegerField(choices=type_chioce, default=0, blank=True, verbose_name="服务类型")
    server = models.ForeignKey(to="Server", on_delete=models.CASCADE, related_name="server", verbose_name="部署主机",blank=True,null=True)
    cluster_type = models.CharField(choices=cluster_chioce, max_length=50, verbose_name="集群模式", default="standlone",
                                    blank=True)
    remark = models.TextField(verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = "基础服务表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}:{}".format(self.name, self.version)


class App(models.Model):
    type_chioce = (
        (0, "base"),
        (1, "api"),
        (2, "web"),
    )
    status_chioce = (
        (1, "在线,需监控"),
        (4, "在线,暂停监控"),
        (9, "下线"),
    )
    name = models.CharField(verbose_name="应用服务名称", max_length=100)
    name_cn = models.CharField(verbose_name="应用中文名称", max_length=255, null=True, blank=True)
    app_type = models.SmallIntegerField(choices=type_chioce, verbose_name="应用类型",default=0, help_text="0:基础服务(base);1:api;2:web")
    domain = models.CharField(max_length=255, verbose_name="服务域名", null=True, blank=True)
    service_ports = models.CharField(max_length=100, verbose_name="服务端口", null=True, blank=True)
    parameter = models.CharField(max_length=500, verbose_name="启动参数", default="'-Xms512m -Xmx512m'", blank=True)
    package_name = models.CharField(max_length=100, verbose_name="服务包名", help_text="self.name.jar", blank=True)
    app_status = models.SmallIntegerField(choices=status_chioce, default=4, verbose_name="服务状态", help_text="是否加入监控")
    app_init = models.CharField(max_length=10, verbose_name="是否已初始化", default="n", help_text="n:需要重新初始化,y:已完成初始化")
    project = models.ForeignKey("Project",on_delete=models.CASCADE,verbose_name="所属项目")
    service = models.ManyToManyField("Service",verbose_name="依赖基础服务")
    server = models.ManyToManyField("Server",verbose_name="部署主机")
    class Meta:
        verbose_name = "应用服务表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

