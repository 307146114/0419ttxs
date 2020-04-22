from django.shortcuts import render,redirect
from df_user.models import UserInfo
from django.http import HttpResponse,HttpResponseRedirect
from hashlib import sha1

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
        rendersucess = render(request, "df_user/user_center_info.html",context)
        print(username)
        if post.get('remembername',0) == '1':
            rendersucess.set_cookie('username', username)

            return rendersucess
        else:
            rendersucess.set_cookie('username', "", -1)
            return rendersucess

    else:
        # 密码错误
        return render(request,"df_user/login.html",{"pwd_error":"密码错误"})

def user_center_info(request):
    # 用户中心请求页面
    uid = request.session.get("user_id")
    # print(uid)
    if uid != None:
        user_Db = UserInfo.objects.filter(pk=uid)
        return render(request,"df_user/user_center_info.html",{'user':user_Db[0],'title':'天天生鲜 - 用户中心'})
    else:
        return  HttpResponseRedirect('/user/login')

def user_center_order(request):
     # 用户订单请求页面
     return render(request,"df_user/user_center_order.html",{'title':'天天生鲜 - 用户订单'})

def user_center_site(request):
    # 修改收或地址请求页面
    uid = request.session["user_id"]
    user_Db = UserInfo.objects.filter(pk=uid)

    return render(request,"df_user/user_center_site.html",{'user':user_Db[0],'title':'天天生鲜 - 收货地址'})

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

