
from django.conf.urls import  url,include
from df_goods import views
urlpatterns = [
    url(r"^(index)?(\.html)?$",views.index),
    url(r"^detail$",views.detail),
    url(r"^list$",views.list),

]
