import time
from datetime import date

from django.db import models


class Main(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=16)

    class Meta:
        abstract = True


class MainWheel(Main):
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


class MainMustBuy(Main):
    # 比购
    class Meta:
        db_table = 'axf_mustbuy'


class MainShow(Main):
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=100)
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16)
    productid1 = models.CharField(max_length=16)
    longname1 = models.CharField(max_length=200, default=0)
    price1 = models.FloatField(default=1)
    marketprice1 = models.FloatField(default=1)
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=200, default=0)
    price2 = models.FloatField(default=1)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=200, default=0)
    price3 = models.FloatField(default=1)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.CharField(max_length=16)  # 商品id
    productimg = models.CharField(max_length=200)  # 商品图片
    productname = models.CharField(max_length=100)  # 名称
    productlongname = models.CharField(max_length=200)  # 规格名称
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)  # 规格
    price = models.FloatField(default=0)  # 折扣价
    marketprice = models.FloatField(default=1)  # 原价
    categoryid = models.CharField(max_length=16)  # 分类id
    childcid = models.CharField(max_length=16)  # 子分类id
    childcidname = models.CharField(max_length=100)  # 名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 排序
    productnum = models.IntegerField(default=1)  # 销量排序

    class Meta:
        db_table = 'axf_goods'


class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    # False 代表女
    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons')  # 头像
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'axf_users'

    # 购物车
class CartModel(models.Model):
    user = models.ForeignKey(UserModel)  # 关联用户
    goods = models.ForeignKey(Goods)  # 挂链商品
    c_num = models.IntegerField(default=1)  # 商品个数
    is_select = models.BooleanField(default=True)  # 是否选择商品

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel)
    o_num = models.CharField(max_length=64)
    # 0表示已下单未付款，1表示已付款未发货，2表示已付款已发货
    o_status = models.IntegerField(default=0)
    o_create = models.DateTimeField(auto_now=True)  # 创建时间

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(OrderModel)  # 关联订单
    goods_num = models.IntegerField(default=1)  # 商品的个数

    class Meta:
        db_table = 'axf_order_goods'


class UserModelTicket(models.Model):
    name = models.ForeignKey(UserModel)
    ticket = models.CharField(max_length=200, null=True)
    out_time = models.DateField()

    class Meta:
        db_table = 'axf_ticket'
