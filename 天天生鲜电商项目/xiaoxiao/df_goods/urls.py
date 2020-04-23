
from django.conf.urls import  url,include
from df_goods import views
urlpatterns = [
    url(r"^(index)?(\.html)?$",views.index),#首页
    url(r"^detail$",views.detail),#商品详细信息
    url(r"^list$",views.list),#商品的类别表

]
