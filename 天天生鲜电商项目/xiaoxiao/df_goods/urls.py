
from django.conf.urls import  url,include
from df_goods import views
from df_goods.MySearchView import*
urlpatterns = [
    url(r"^(index)?(\.html)?$",views.index),#首页
    url(r"^detail$",views.detail),#商品详细信息
    url(r"^list$",views.list),#商品的类别表
    # url(r'^search/', MySeachView.as_view(), name='search_view'),#2.4版本后自定义context
    url(r'^search/', MySeachView(), name='search_view'),#2.4版本前自定义context
    # url(r'^search/', include('haystack.urls')),#商品的类别表

]
