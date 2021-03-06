# Generated by Django 2.2.5 on 2019-11-23 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='应用服务名称')),
                ('name_cn', models.CharField(blank=True, max_length=255, null=True, verbose_name='应用中文名称')),
                ('app_type', models.SmallIntegerField(choices=[(0, 'base'), (1, 'api'), (2, 'web')], default=0, help_text='0:基础服务(base);1:api;2:web', verbose_name='应用类型')),
                ('domain', models.CharField(blank=True, max_length=255, null=True, verbose_name='服务域名')),
                ('service_ports', models.CharField(blank=True, max_length=100, null=True, verbose_name='服务端口')),
                ('parameter', models.CharField(blank=True, default="'-Xms512m -Xmx512m'", max_length=500, verbose_name='启动参数')),
                ('package_name', models.CharField(blank=True, help_text='self.name.jar', max_length=100, verbose_name='服务包名')),
                ('app_status', models.SmallIntegerField(choices=[(1, '在线,需监控'), (4, '在线,暂停监控'), (9, '下线')], default=4, help_text='是否加入监控', verbose_name='服务状态')),
                ('app_init', models.CharField(default='n', help_text='n:需要重新初始化,y:已完成初始化', max_length=10, verbose_name='是否已初始化')),
            ],
            options={
                'verbose_name': '应用服务表',
                'verbose_name_plural': '应用服务表',
            },
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(blank=True, choices=[('server', '服务器'), ('network', '网络设备'), ('storage', '存储设备'), ('software', '软件资产')], default='server', max_length=64, verbose_name='资产类型')),
                ('name', models.CharField(max_length=150, verbose_name='资产名称')),
                ('sn', models.CharField(max_length=100, verbose_name='资产编码')),
                ('status', models.SmallIntegerField(blank=True, choices=[(0, '新购'), (1, '初始化'), (2, '备用'), (3, '在线'), (4, '故障'), (5, '下线')], default=0, verbose_name='资产状态')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='采购时间')),
                ('modity_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '资产总表',
                'verbose_name_plural': '资产总表',
            },
        ),
        migrations.CreateModel(
            name='Env',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='环境名称')),
                ('code', models.CharField(max_length=50, verbose_name='环境标识')),
            ],
            options={
                'verbose_name': '环境信息表',
                'verbose_name_plural': '环境信息表',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idc_name', models.CharField(max_length=255, unique=True, verbose_name='机房名称')),
                ('idc_contact', models.CharField(blank=True, max_length=255, null=True, verbose_name='联系方式')),
            ],
            options={
                'verbose_name': 'IDC机房',
                'verbose_name_plural': 'IDC机房',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_created=True, blank=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=150, verbose_name='业务名称')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='业务编码')),
                ('modity_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '业务表',
                'verbose_name_plural': '业务表',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_created=True, blank=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=150, verbose_name='项目名称')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='项目编码')),
                ('modity_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '项目表',
                'verbose_name_plural': '项目表',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '物理机'), (1, '虚拟机'), (2, '云主机')], default=0, verbose_name='服务器类型')),
                ('server_model', models.CharField(blank=True, max_length=100, null=True, verbose_name='服务器型号')),
                ('hostname', models.CharField(max_length=150, verbose_name='主机名称')),
                ('public_ip', models.GenericIPAddressField(unique=True, verbose_name='公网地址')),
                ('intranet_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='内网地址')),
                ('os', models.CharField(blank=True, default='Centos 7.5', max_length=100, verbose_name='操作系统版本')),
                ('cpu', models.CharField(blank=True, max_length=50, null=True, verbose_name='cpu核数')),
                ('memory', models.CharField(blank=True, max_length=100, null=True, verbose_name='内存大小')),
                ('disk', models.CharField(blank=True, max_length=100, null=True, verbose_name='磁盘大小')),
                ('server_remark', models.TextField(blank=True, null=True, verbose_name='服务器备注')),
                ('asset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Asset')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='env', to='cmdb.Env')),
                ('host_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='host_on_server', to='cmdb.Server', verbose_name='宿主机')),
            ],
            options={
                'verbose_name': '服务器表',
                'verbose_name_plural': '服务器表',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='服务名称')),
                ('version', models.CharField(blank=True, max_length=100, verbose_name='服务版本')),
                ('service_type', models.SmallIntegerField(blank=True, choices=[(0, '消息队列'), (1, '数据库'), (2, '中间件')], default=0, verbose_name='服务类型')),
                ('cluster_type', models.CharField(blank=True, choices=[('standlone', '单机模式'), ('master-slave', '主从模式'), ('cluster', '高可用模式')], default='standlone', max_length=50, verbose_name='集群模式')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('server', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='server', to='cmdb.Server', verbose_name='部署主机')),
            ],
            options={
                'verbose_name': '基础服务表',
                'verbose_name_plural': '基础服务表',
            },
        ),
    ]
