
from django.conf.urls import  url,include
from df_user import views
urlpatterns = [
    url(r'^register$',views.register),#注册页面
    url(r'^register_handle$',views.register_handle),#注册请求
    url(r'^register_username$',views.register_username),#查询用户名是否注册
    url(r'^login$',views.login),#跳转至登录页面
    url(r'^login_handle$',views.login_handle),#登录请求
    url(r'^user_center_info$',views.user_center_info),#跳转用户中心
    url(r'^user_center_order$',views.user_center_order),#跳转用户订单
    url(r'^user_center_site$',views.user_center_site),#跳转收货地址
    url(r'^editUesr$',views.editUesr),#修改收货地址请求

]
