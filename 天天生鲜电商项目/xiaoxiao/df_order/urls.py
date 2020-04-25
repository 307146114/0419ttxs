
from django.conf.urls import  url,include
from df_order import views
urlpatterns = [
    url(r'^$',views.order),#购物车信息
    url(r'^addorder$',views.addorder),#购物车信息


]
