from django.shortcuts import render
from django.http import HttpResponse
from df_user import  user_decorator
from df_cart.models import  *
# Create your views here.
@user_decorator.login
def cart(request):
    userId = request.session["user_id"]
    cartlist = CartInfo.objects.filter(user=userId)
    context = {'pagetype':1}
    if len(cartlist)>0:
        context['list']=cartlist
    else:
        context['list']=[]
    return  render(request,'df_cart/cart.html',context)

def count(request):
    # 获取用户的购物车条数
    userId = request.session.get("user_id",'')
    if userId=='':
        return HttpResponse(0)
    else:
        count = CartInfo.objects.filter(user_id=userId).count()
        return HttpResponse(count)

def add(request):
    # 获取用户的购物车条数
    userId = request.session.get("user_id", '')
    goodsid = request.GET.get("goods_id", "")
    print("userId%s"%userId)
    print("goodsid%s"%goodsid)
    if userId!="" and goodsid!="":
         cartsList = CartInfo.objects.filter(user_id=userId, goods_id=goodsid)
         if len(cartsList)>0:
             cart = cartsList[0]
             cart.count = cart.count+1
             cart.save()
         else:
             cart = CartInfo()
             cart.user_id = userId
             cart.goods_id = goodsid
             cart.count = 1
             cart.save()
    return HttpResponse("ok")

def update(request):
    cartId = request.GET.get("cartid", 0)
    count = request.GET.get("count", "0")
    # print("carid:%s,count:%s"%(cartId,count))
    if int(cartId) >0 and int(count) > 0:
        cartlist = CartInfo.objects.filter(pk=cartId)
        if len(cartlist)>0:
            cart = cartlist[0]
            cart.count = count
            cart.save()
            return HttpResponse("ok")
    return HttpResponse("err")

def delete(request):
    cartId = request.GET.get("cartid", 0)
    if int(cartId) > 0 :
        cartlist = CartInfo.objects.filter(pk=cartId)
        if len(cartlist) > 0:
            cart = cartlist[0]
            cart.delete()
            return HttpResponse("ok")
    return HttpResponse("err")
