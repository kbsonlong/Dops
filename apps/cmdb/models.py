from django.db import models

# Create your models here.

class Product(models.Model):
    """
    业务线
    """
    name = models.CharField(max_length=150,verbose_name="业务名称")
    code = models.CharField(max_length=50,verbose_name="业务编码",null=True,blank=True)
    parent = models.ForeignKey("self",on_delete=models.CASCADE,verbose_name="上级业务",null=True,blank=True)

    class Meta:
        verbose_name = "业务表"
        verbose_name_plural = verbose_name
        db_table = "product"

    def __str__(self):
        return self.name

class Project(models.Model):
    """
    项目表
    """
    name = models.CharField(max_length=150,verbose_name="项目名称")
    code = models.CharField(max_length=50,verbose_name="项目编码",null=True,blank=True)
    product = models.ForeignKey("Product",verbose_name="所属业务线",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "项目表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=150, verbose_name="资产名称")
    sn = models.CharField(max_length=100,verbose_name="资产编码")

    class Meta:
        verbose_name = "资产总表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Server(models.Model):
    asset = models.OneToOneField("Asset",verbose_name="资产名称",on_delete=models.CASCADE)
    hostname =  models.CharField(max_length=150,verbose_name="主机名称")
    public_ip = models.GenericIPAddressField(verbose_name="公网地址",null=True,blank=True)
    inside_ip = models.GenericIPAddressField(verbose_name="内网地址",null=True,blank=True)

    class Meta:
        verbose_name = "服务器表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}-{}".format(self.asset.name,self.public_ip)

class Service(models.Model):
    name = models.CharField(max_length=150,verbose_name="基础服务名称")
    version = models.CharField(max_length=50,verbose_name="基础服务版本")
    Server = models.ManyToManyField("Server",verbose_name="部署主机")
    class Meta:
        verbose_name = "基础服务表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=150,verbose_name="应用服务名称")
    project = models.ForeignKey("Project",on_delete=models.CASCADE,verbose_name="所属项目")
    service = models.ManyToManyField("Service",verbose_name="依赖基础服务")
    server = models.ManyToManyField("Server",verbose_name="部署主机")
    class Meta:
        verbose_name = "应用服务表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
