from django.shortcuts import render
from django.http import  HttpResponse
from df_cart.models import *
from df_user.models import *
from df_user import user_decorator
from django.db import transaction
from df_order.models import *
from hashlib import md5
from datetime import datetime
import random
# Create your views here.
@user_decorator.login
def order(request):
    # 获取用户id
    userId = request.session['user_id']
    # 通过id获取用户
    user = UserInfo.objects.get(pk=userId)
    # 修改用电话格式
    text = user.tel[3:7]
    user.tel=user.tel.replace(text,"****")
    # 获取购物车id
    cartid_list = request.GET.getlist('cartid')
    # 获取所有购物车信息
    cart_list = CartInfo.objects.filter(pk__in=cartid_list)

    context ={
        'pagetype': 1,
        'list':cart_list,
        'user':user,
        }
    return  render(request,"df_order/place_order.html",context)
@transaction.atomic
@user_decorator.login
def addorder(request):
    # 设置失误保存点
    saveid = transaction.savepoint()
    try:
        # 获取购物车id
        cartids = request.POST.get('cartids', '')
        # id不为“” 继续执行
        if cartids != "":
            # 获取运费值
            yunfei = request.POST.get('yunfei', 0)
            # 获取用户id
            userId = request.session['user_id']
            # 根据id获取用户信息
            user = UserInfo.objects.get(pk=userId)
            # 根据用户信息拼写订单地址
            address = user.adress + "("+user.name+" 收)"+user.tel
            # 获取当前时间
            time = datetime.now()
            # 获取一个随机数
            rand = random.randint(0,9999999)
            # 随机生成一个md5数值作为主键保存
            md = md5()
            str_id = "%s%s%s"%(user.username,time,rand)
            md.update(str_id.encode("utf8"))
            id = md.hexdigest()
            # 创建一个定订单对象并复制，总价暂时不标明
            order_info = OrderInfo()
            order_info.oid = id
            order_info.oUser=user
            order_info.oAdress=address
            order_info.oTotal = 0
            order_info.save()
            # 记录总价格
            total = float(yunfei)
            # 切割订单中的购物车id
            cartid_list = cartids.split(',')
            # 查询所有订单中的购物车信息
            carts = CartInfo.objects.filter(pk__in=cartid_list)
            # 遍历所有购物车信息
            for cart in carts:
                # 判断库存是否满足订单需求
                if cart.goods.gkucun >= cart.count:
                    # 设置一个订单详细信息的对象 并赋值
                    order_detail = OrderDetailInfo()
                    order_detail.price = cart.goods.gprice
                    order_detail.count = cart.count
                    order_detail.order = order_info
                    order_detail.goods = cart.goods
                    order_detail.save()
                    total += float(cart.goods.gprice) * float(cart.count)
                    # 减去商品库存
                    cart.goods.gkucun -= cart.count
                    cart.goods.save()
                    cart.delete()
                else:
                    # 无库存直接返回 错误信息
                    transaction.rollback(saveid)
                    return HttpResponse('err')
                order_info.oTotal = total
                order_info.save()
            return HttpResponse("ok")
    except Exception:
        transaction.rollback(saveid)
        return HttpResponse("err")
    transaction.rollback(saveid)
    return HttpResponse('err')
