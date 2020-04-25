from django.shortcuts import render,redirect
from df_user.models import UserInfo
from django.http import HttpResponse,HttpResponseRedirect
from hashlib import sha1
from . import user_decorator
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator
# Create your views here.

def register(request):
    # 注册请求页面
    return  render(request,'df_user/register.html',{'title':'天天生鲜 - 注册'})
def register_username(request):
    # 验证账号
    username = request.GET.get('username')
    count = UserInfo.objects.filter(username=username).count()
    print(count)
    return HttpResponse({'count':count})

def register_handle(request):
    # 注册页面
    user_name = request.POST.get("user_name")
    pwd = request.POST.get("pwd")
    cpwd = request.POST.get("cpwd")
    email = request.POST.get("email")
    if pwd !=cpwd:
        return redirect('/user/register')
    else:
        user_info = UserInfo()
        user_info.username = user_name
        # 给密码加密
        s1 = sha1()
        s1.update(pwd.encode('utf8'))
        pwd = s1.hexdigest()
        user_info.password = pwd
        user_info.email =email
        # 保存密码
        user_info.save()
        return redirect('/user/login')

def login(request):
    # 登录请求页面
    return render(request,'df_user/login.html',{'title':'天天生鲜 - 登录'})
def login_handle(request):
    # 登录页面
    post = request.POST
    context ={}
    username = post.get('username')
    pwd = post.get('pwd')
    # print(post.get('remembername'))
    s1 = sha1()
    s1.update(pwd.encode('utf8'))
    pwd = s1.hexdigest()
    user_Db = UserInfo.objects.filter(username=username)
    if len(user_Db)==0:
        # 账号不存在
        return render(request,"df_user/login.html",{"user_error":"账号不存在"})
    elif user_Db[0].password == pwd:
        # 登录成功
        # print(post.get('remembername',0))
        request.session["user_id"] = user_Db[0].id
        request.session["user_name"] = user_Db[0].username
        context ={'user':user_Db[0],'title':'天天生鲜 - 用户中心'}
        # 获取之前访问的页面
        url = request.COOKIES.get("url", '/')
        # del request.COOKIES['url']
        red = HttpResponseRedirect(url)
        # print(username)
        if post.get('remembername',0) == '1':
            red.set_cookie('username', username)
            return red
        else:
            red.set_cookie('username', "", -1)
            return red

    else:
        # 密码错误
        return render(request,"df_user/login.html",{"pwd_error":"密码错误"})
@user_decorator.login
def user_center_info(request):
    session_id = request.session["user_id"]
    user = UserInfo.objects.get(pk=session_id)
    goods_ids = request.COOKIES.get("goods_ids", "")
    list = []
    if goods_ids !="":
        goods_ids_list = goods_ids.split(",")
        for goodsId in goods_ids_list:
            list.append( GoodsInfo.objects.get(pk=goodsId))

    return render(request,"df_user/user_center_info.html",{'title':'天天生鲜 - 用户中心','list':list,'user':user,'pagetype':2})
@user_decorator.login
def user_center_order(request):
    try:
        # 获取用户id
        userId = request.session['user_id']
        # 获取订单显示第几页
        pageNum = request.GET.get('page_num', 1)
        # 根据用户信息查询订单
        orderlist = OrderInfo.objects.filter(oUser_id=userId).order_by('oIsPay')
        # 设置分页
        paginator = Paginator(orderlist,3)
        page = paginator.page(pageNum)
        page_list = paginator.page_range
        # 用户订单请求页面
        return render(request, "df_user/user_center_order.html", {'title': '天天生鲜 - 用户订单','page':page,'page_list':page_list,'pagetype':2})
    except Exception:
        return HttpResponseRedirect('/user/user_center_order')
@user_decorator.login
def user_center_site(request):
    # 修改收或地址请求页面
    uid = request.session["user_id"]
    user_Db = UserInfo.objects.filter(pk=uid)

    return render(request,"df_user/user_center_site.html",{'user':user_Db[0],'title':'天天生鲜 - 收货地址','pagetype':2})

def editUesr(request):
    post = request.POST
    uid = request.session.get("user_id")
    user = UserInfo.objects.get(pk=uid)
    name = post.get('name')
    adress = post.get('adress')
    youbian = post.get('youbian')
    tel = post.get('tel')
    user.name  =name
    user.adress = adress
    user.youbian = youbian
    user.tel = tel
    user.save()
    return  redirect('/user/user_center_site')

def logout(request):
    # 注销请求
    # 清空缓存 注销登录
    request.session.flush()
    # print(url)
    return HttpResponseRedirect("/")

