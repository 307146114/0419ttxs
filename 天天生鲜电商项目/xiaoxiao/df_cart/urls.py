
from django.conf.urls import  url,include
from df_cart import views
urlpatterns = [
    url(r'^$',views.cart),#购物车信息
    url(r'^count$',views.count),#获取当前用户保存的购物车信息条数
    url(r'^add$',views.add),#添加购物车信息
    url(r'^update$',views.update),#修改购物城信息
    url(r'^delete$',views.delete),#删除购物车信息
    url(r'^kucun$',views.kucun),#查看购物车商品库数据


]
