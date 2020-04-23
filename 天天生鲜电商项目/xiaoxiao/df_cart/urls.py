
from django.conf.urls import  url,include
from df_cart import views
urlpatterns = [
    url(r'^$',views.cart),
    url(r'^count$',views.count),
    url(r'^add$',views.add),
    url(r'^update$',views.update),
    url(r'^delete$',views.delete),


]
