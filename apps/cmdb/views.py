import os,xlrd
from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import ListView,DetailView
from django.http import JsonResponse,StreamingHttpResponse
from pure_pagination import PageNotAnInteger, Paginator
from django.conf import settings
# Create your views here.

from . import models
from .utils import CellWriter


def file_iterator(file_name, chunk_size=512):
    f = open(file_name, "rb")
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break
    f.close()

def index(request):
    product = models.Product.objects.first()
    return render(request,"chart.html",{"product":product})

class AssetListView(ListView):
    model = models.Asset
    template_name = "asset-list.html"
    ordering = ("id",)
    context_object_name = 'assets'

    def get_context_data(self, **kwargs):
        context = super(AssetListView,self).get_context_data( **kwargs)
        return context

def assets_dumps(request):
    if request.method == "POST":
        dRbt = CellWriter('assets_dumps.xls')
        serSheet = dRbt.workbook.add_sheet('服务器资产',cell_overwrite_ok=True)
        netSheet = dRbt.workbook.add_sheet('网络设备资产',cell_overwrite_ok=True)
        bList = ['资产类型','资产编码','资产名称','采购时间','修改时间','资产状态','所属项目','所属机房','所属环境','主机名称','公网地址',
                 '内网地址','宿主机','操作系统版本','cpu核数','内存大小','磁盘大小']
        nList = ['资产类型','资产编码','资产名称','采购时间','修改时间','资产状态','所属项目','所属机房','所属环境']
        dRbt.writeBanner(sheetName=serSheet, bList=bList)
        dRbt.writeBanner(sheetName=netSheet, bList=nList)
        count = 1
        for ast in eval(request.POST.get('assetsIds')):
            try:
                assets = models.Asset.objects.select_related().get(id=int(ast))
            except Exception as ex:
                print(ex)
                continue
            if assets.asset_type in ['vmser','server']:
                sheet = serSheet
                sheet.write(count,9,assets.server.hostname,dRbt.bodySttle())
                sheet.write(count,10,assets.server.public_ip,dRbt.bodySttle())
                sheet.write(count,11,assets.server.intranet_ip,dRbt.bodySttle())
                sheet.write(count,12,assets.server.host_on,dRbt.bodySttle())
                sheet.write(count,13,assets.server.os,dRbt.bodySttle())
                sheet.write(count,14,assets.server.cpu,dRbt.bodySttle())
                sheet.write(count,15,assets.server.memory,dRbt.bodySttle())
                sheet.write(count,16,assets.server.disk,dRbt.bodySttle())
            else:
                sheet = netSheet
            if assets.asset_type == 'vmser':sheet.write(count,0,'虚拟机',dRbt.bodySttle())
            elif assets.asset_type == 'server':sheet.write(count,0,'服务器',dRbt.bodySttle())
            elif assets.asset_type == 'switch':sheet.write(count,0,'交换机',dRbt.bodySttle())
            elif assets.asset_type == 'route':sheet.write(count,0,'路由器',dRbt.bodySttle())
            elif assets.asset_type == 'printer':sheet.write(count,0,'打印机',dRbt.bodySttle())
            elif assets.asset_type == 'scanner':sheet.write(count,0,'扫描仪',dRbt.bodySttle())
            elif assets.asset_type == 'firewall':sheet.write(count,0,'防火墙',dRbt.bodySttle())
            elif assets.asset_type == 'storage':sheet.write(count,0,'存储设备',dRbt.bodySttle())
            elif assets.asset_type == 'wifi':sheet.write(count,0,'无线设备',dRbt.bodySttle())
            sheet.write(count,1,assets.sn,dRbt.bodySttle())
            sheet.write(count,2,assets.name,dRbt.bodySttle())
            sheet.write(count,3,str(assets.create_time),dRbt.bodySttle())
            sheet.write(count,4,str(assets.modity_time),dRbt.bodySttle())
            if assets.status == 0: sheet.write(count,5,"新购",dRbt.bodySttle())
            elif assets.status == 1: sheet.write(count,5,"初始化",dRbt.bodySttle())
            elif assets.status == 2: sheet.write(count,5,"备用",dRbt.bodySttle())
            elif assets.status == 3: sheet.write(count,5,"在线",dRbt.bodySttle())
            elif assets.status == 4: sheet.write(count,5,"故障",dRbt.bodySttle())
            elif assets.status == 5: sheet.write(count,5,"下线",dRbt.bodySttle())
            sheet.write(count,6,assets.asset_project.name,dRbt.bodySttle())
            sheet.write(count,7,assets.idc,dRbt.bodySttle())
            sheet.write(count,8,assets.server.env.name,dRbt.bodySttle())
            count = count + 1
        dRbt.save()
        response = StreamingHttpResponse(file_iterator('assets_dumps.xls'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="{file_name}'.format(file_name='assets_dumps.xls')
        return response

def assets_import(request):
    if request.method == "POST":
        f = request.FILES.get('import_file')
        filename = os.path.join(os.getcwd() + '/upload/',f.name)
        if os.path.isdir(os.path.dirname(filename)) is not True:os.makedirs(os.path.dirname(filename))
        fobj = open(filename,'wb')
        for chrunk in f.chunks():
            fobj.write(chrunk)
        fobj.close()
        #读取上传的execl文件内容方法
        def getAssetsData(fname=filename):
            bk = xlrd.open_workbook(fname)
            dataList = []
            try:
                server = bk.sheet_by_name("server")
                net = bk.sheet_by_name("net")
                for i in range(1,server.nrows):
                    dataList.append(server.row_values(i))
                for i in range(1,net.nrows):
                    dataList.append(net.row_values(i))
            except Exception as e:
                return []
            return dataList
        dataList = getAssetsData(fname=filename)
        #获取服务器列表
        for data in dataList:
            assets = {
                      'assets_type':data[0],
                      'name':data[1],
                      'sn':data[2],
                      'buy_user':int(data[5]),
                      'management_ip':data[6],
                      'manufacturer':data[7],
                      'model':data[8],
                      'provider':data[9],
                      'status':int(data[10]),
                      'put_zone':int(data[11]),
                      'group':int(data[12]),
                      'project':int(data[13]),
                      'business':int(data[14]),
                      }
            if data[3]:assets['buy_time'] = xlrd.xldate.xldate_as_datetime(data[3],0)
            if data[4]:assets['expire_date'] = xlrd.xldate.xldate_as_datetime(data[4],0)
            if assets.get('assets_type') in ['vmser','server']:
                server_assets = {
                          'ip':data[15],
                          'keyfile':data[16],
                          'username':data[17],
                          'passwd':data[18],
                          'hostname':data[19],
                          'port':data[20],
                          'raid':data[21],
                          'line':data[22],
                          }
            else:
                net_assets = {
                            'ip':data[15],
                            'bandwidth':data[16],
                            'port_number': data[17],
                            'firmware':data[18],
                            'cpu':data[19],
                            'stone':data[20],
                            'configure_detail': data[21]
                              }
            count = models.Asset.objects.filter(name=assets.get('name')).count()
            if count == 1:
                assetsObj = models.Asset.objects.get(name=assets.get('name'))
                models.Asset.objects.filter(name=assets.get('name')).update(**assets)
                try:
                    if assets.get('assets_type') in ['vmser','server']:
                        models.Server.objects.filter(assets=assetsObj).update(**server_assets)

                except  Exception as ex:
                    print("批量更新资产失败: {ex}".format(ex=str(ex)))
            else:
                try:
                    assetsObj = models.Asset.objects.create(**assets)
                except Exception as  ex:
                    print("批量写入资产失败: {ex}".format(ex=str(ex)))
                if assetsObj:
                    try:
                        if assets.get('assets_type') in ['vmser','server']:
                            models.Server.objects.create(assets=assetsObj,**server_assets)

                    except Exception as ex:
                        assetsObj.delete()
        return HttpResponseRedirect('/assets_list')