from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.Project)
admin.site.register(models.Asset)
admin.site.register(models.Server)
admin.site.register(models.Service)
admin.site.register(models.App)
admin.site.register(models.Env)