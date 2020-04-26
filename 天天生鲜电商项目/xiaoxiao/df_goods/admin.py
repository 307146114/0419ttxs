from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.TypeInfo)
class GoodstypeInfo(admin.ModelAdmin):
    list_display = ['ttitle','isDelete']
    search_fields = ['ttitle']
    list_filter = ['isDelete',]
    list_per_page = 10
@admin.register(models.GoodsInfo)    
class GoodsInfo(admin.ModelAdmin):
    list_display = ['gtitle','gprice','gkucun','isDelete']
    search_fields = ['gtitle']
    list_filter = ['isDelete',]
    list_per_page = 10