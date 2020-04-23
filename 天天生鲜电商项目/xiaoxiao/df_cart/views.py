from django.shortcuts import render
from django.http import HttpResponse
from df_user import  user_decorator
from df_cart.models import  *
# Create your views here.
@user_decorator.login
def cart(request):
    #获取用户id，已经做过登录判断，不会出现找不到id，报错
    userId = request.session["user_id"]
    # 通过id获取用户列表
    cartlist = CartInfo.objects.filter(user=userId)
    # 设置当前页面是否显示购物车图标
    context = {'pagetype':1}
    # 当查询找到信息 直接返回结合
    if len(cartlist)>0:
        context['list']=cartlist
    else:
        # 没有找到返回空集合
        context['list']=[]
    return  render(request,'df_cart/cart.html',context)

def count(request):
    # 获取用户的购物车条数
    userId = request.session.get("user_id",'')
    # 用户id未找到
    if userId=='':
        # 返回购物车信息条数0
        return HttpResponse(0)
    else:
        # 否则返回当前购物车信息条数
        count = CartInfo.objects.filter(user_id=userId).count()
        return HttpResponse(count)

def add(request):
    # 获取用户的购物车条数
    userId = request.session.get("user_id", '')
    # 获取购物车id 默认返回空
    goodsid = request.GET.get("goods_id", "")
    # 当用户id和购物车信息id不为空时调用
    if userId!="" and goodsid!="":
         # 根据购物车信息id查询
         cartsList = CartInfo.objects.filter(user_id=userId, goods_id=goodsid)
         # 查询到 修改数量+1
         if len(cartsList)>0:
             cart = cartsList[0]
             cart.count = cart.count+1
             cart.save()
         else:
             # 未查询到，创建的购物车信息，保存值数据库
             cart = CartInfo()
             cart.user_id = userId
             cart.goods_id = goodsid
             cart.count = 1
             cart.save()
    return HttpResponse("ok")

def update(request):
    # 修改购物车信息
    # 获取要修改的购物车信息id
    cartId = request.GET.get("cartid", 0)
    # 获取修改成的数量
    count = request.GET.get("count", 0)
    # 判断要修改的购物车信息id 和数量合法操作数据库
    if int(cartId) >0 and int(count) > 0:
        cartlist = CartInfo.objects.filter(pk=cartId)
        if len(cartlist)>0:
            cart = cartlist[0]
            cart.count = count
            cart.save()
            return HttpResponse("ok")
    # 否则返回错误信息
    return HttpResponse("err")

def delete(request):
    # 删除购物车信息
    # 获取要修改的购物车信息id
    cartId = request.GET.get("cartid", 0)
    # 获取要修改的购物车信息id 判断是否合法
    if int(cartId) > 0 :
        # 查询数据是否能找到当前购物车信息
        cartlist = CartInfo.objects.filter(pk=cartId)
        # 找到后直接删除，返回ok
        if len(cartlist) > 0:
            cart = cartlist[0]
            cart.delete()
            return HttpResponse("ok")
    # 其他情况返回错误
    return HttpResponse("err")
