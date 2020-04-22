from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class TypeInfo(models.Model):       #index首页商品分类信息
    ttitle = models.CharField('类型名称',max_length=20,db_column='标题')
    isDelete = models.BooleanField('是否删除', default=False,db_column='是否删除')   #是否删除,默认不删
    def __str__(self):
        return self.ttitle
    class Meta:
        verbose_name = '分类信息'
        verbose_name_plural = '分类信息'

class GoodsInfo(models.Model):      #商品信息
    gtitle = models.CharField('商品名称', max_length=20,db_column='标题')
    gpic = models.ImageField('商品图片',upload_to='df_goods',db_column='图片位置')      #商品图片
    gprice = models.DecimalField('商品价格',max_digits=5, decimal_places=2,db_column='价格')        #总共最多有7位,小数占2位
    gunit = models.CharField('商品单位',max_length=20, default='500g',db_column='单位')     #商品的单位
    gclick = models.IntegerField('点击量',db_column='点击数量')          #商品点击量,便于排人气
    isDelete = models.BooleanField('是否删除',default=False,db_column='是否删除')
    gjianjie = HTMLField('简介',db_column='简介')     #商品简介
    gkucun = models.IntegerField('库存',db_column='库存')          #商品库存
    gcontent = HTMLField('详细介绍',db_column='详细情况')                  #商品详细内容
    gtype = models.ForeignKey(TypeInfo, verbose_name='所属分类', on_delete=models.CASCADE)     #商品所属类型
    # gadv = models.BooleanField(default=False,db_column='')   #商品推荐
    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'