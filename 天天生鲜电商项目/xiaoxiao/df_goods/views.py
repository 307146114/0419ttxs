from django.shortcuts import render
from df_goods.models import *
from django.core.paginator import Paginator
from django.http import  HttpResponseRedirect
# Create your views here.

def index(request,*args):
    # 首页
    type_list = TypeInfo.objects.all()
    type1 = type_list[0]
    # 获取第一类别---水果
    type11 = type1.goodsinfo_set.all()[0:4]
    # 获取水果类别的子类---取前4个
    type2 = type_list[1]
    # 获取第二类别---海鲜水产
    type21 = type2.goodsinfo_set.all()[0:4]
    # 获取海鲜水产类别的子类---取前4个
    type3 = type_list[2]
    # 获取第三类别---猪牛羊肉
    type31 = type3.goodsinfo_set.all()[0:4]
    # 获取猪牛羊肉类别的子类---取前4个
    type4 = type_list[3]
    # 获取第四类别---禽类蛋品
    type41 = type4.goodsinfo_set.all()[0:4]
    # 获取禽类蛋品类别的子类---取前4个
    type5 = type_list[4]
    # 获取第五类别---新鲜蔬菜
    type51 = type5.goodsinfo_set.all()[0:4]
    # 获取新鲜蔬菜类别的子类---取前4个
    type6 = type_list[5]
    # 获取第六类别---速冻食品
    type61 = type6.goodsinfo_set.all()[0:4]
    # 获取速冻食品类别的子类---取前4个
    context = {
        'pagetype':1,
        'titile':'天天生鲜 - 主页',
        'type1':type1,
        'type11':type11,
        'type2':type2,
        'type21':type21,
        'type3':type3,
        'type31':type31,
        'type4':type4,
        'type41':type41,
        'type5':type5,
        'type51':type51,
        'type6':type6,
        'type61':type61,
            }
    return  render(request,'df_goods/index.html',context)

def detail(request):
    # 商品单页
    try:
        goodsid = request.GET.get("goods_id")
        goods = GoodsInfo.objects.get(pk=goodsid)
        # 浏览量+1
        goods.gclick = int(goods.gclick)+1
        goods.save()
        context = {
            'pagetype': 1,
            'titile': '天天生鲜 - ' + goods.gtitle,
            'goods': goods,
        }
        # 设置返回的模板
        red = render(request, 'df_goods/detail.html', context)
        # 获取cookies中存储最近浏览的信息，默认‘’
        goods_ids = request.COOKIES.get("goods_ids", "")
        if goods_ids != "":
            # 当已存在浏览信息 处理
            # 使用，分割当前字符串
            goods_id_list = goods_ids.split(",")
            # 判断当前浏览的页面是否已经存在
            if goods_id_list.count(str(goods.id))>=1:
                # 存在，则删除
                goods_id_list.remove(str(goods.id))
            #     将当前浏览的信息的加入当前结合的最前面
            goods_id_list.insert(0,str(goods.id))
            # 判断当前信息是否大于5条，大于则只保存最新的5条
            if len(goods_id_list)>=6:
                del goods_id_list[5]
            # 设置最近访问网页的cookies
            red.set_cookie("goods_ids", ','.join(goods_id_list))
            return red
        else:
            # 若是第一次保存最近访问，直接设置
            red.set_cookie("goods_ids",goods.id)
            return red
    except Exception:
        # 数据库为查询到或其他非法信息，直接删除
        return HttpResponseRedirect("/")
def list(request):
    # 商品列表
    # 获取排列排列顺序
    type = request.GET.get("type", 0)
    # 获取物品类别id
    goodsStype = request.GET.get("goodstype", 1)
    # 获取要显示页码
    page_num = request.GET.get("page_num", 1)
    # 根据类别id获取类别对象
    type_info = TypeInfo.objects.get(pk=goodsStype)
    # 获取该类别的所有商业
    if type =="1":
        # 按价格排序
        goods_list = type_info.goodsinfo_set.all().order_by('gprice')
    elif type =="2":
        # 按人气排序
        goods_list = type_info.goodsinfo_set.all().order_by('gclick')
    else:
        # 默认排序
        goods_list = type_info.goodsinfo_set.all()
    # goods_list = type_info.goodsinfo_set.all()
    # 分页，每页显示15个对象
    paginator = Paginator(goods_list, 15)
    # 显示第N页的数据
    page = paginator.page(page_num)
    # 获取页码的结合
    page_list = paginator.page_range
    context = {
        'pagetype': 1,#显示购物车
        'titile': '天天生鲜 - ' + type_info.ttitle,
        'page': page,
        'page_list':page_list,
        "goodsStype":type_info.id,
        "type":type,
        "typename":type_info.ttitle
    }
    return render(request, 'df_goods/list.html', context)

