from django.db import models

# Create your models here.
class OrderInfo(models.Model):
    oid = models.CharField(max_length=40,primary_key=True)
    oUser = models.ForeignKey('df_user.UserInfo',on_delete=None)
    oIsPay = models.BooleanField(default=False)
    oDate = models.DateTimeField(auto_now=True)
    oAdress = models.CharField(max_length=150)
    oTotal = models.DecimalField(max_digits=6,decimal_places=2)

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo',on_delete=None)
    order = models.ForeignKey(OrderInfo,on_delete=None)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
