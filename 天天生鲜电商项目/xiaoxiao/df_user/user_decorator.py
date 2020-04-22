from  django.http import HttpResponseRedirect
# 登录验证
def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            url = request.get_full_path()
            red.set_cookie("url",url)
            return  red

    return login_fun