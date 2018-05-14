import random

import time
from datetime import timedelta, datetime

from APP.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, UserModel, UserModelTicket, OrderModel, \
    FoodType, Goods, CartModel, OrderGoodsModel

from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse


def home(request):
    wheelList = MainWheel.objects.all()
    navList = MainNav.objects.all()
    mustBuyList = MainMustBuy.objects.all()
    shopList = MainShop.objects.all()
    shopList1 = shopList[0]
    shopList2 = shopList[1:3]
    shopList3 = shopList[3:7]
    shopList4 = shopList[7:11]
    mainShow = MainShow.objects.all()
    mainShow1 = mainShow[0]
    mainShow2 = mainShow[1]
    mainShow3 = mainShow[2]
    mainShow4 = mainShow[3]
    mainShow5 = mainShow[4]
    mainShow6 = mainShow[5]
    data = {
        'wheelList': wheelList,
        'navList': navList,
        'mustBuyList': mustBuyList,
        'shopList': shopList,
        # 'shopList1': shopList1,
        # 'shopList2': shopList2,
        # 'shopList3': shopList3,
        # 'shopList4': shopList4,
        'mainShow1': mainShow1,
        'mainShow2': mainShow2,
        'mainShow3': mainShow3,
        'mainShow4': mainShow4,
        'mainShow5': mainShow5,
        'mainShow6': mainShow6,
    }
    return render(request, 'home/home.html', data)


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                ticket = ''
                s = '1234567890qwertyuiopasdfghjklmnbvcxz'
                for _ in range(15):
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK_' + ticket + str(now_time)
                response = HttpResponseRedirect('/axf/home/')
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                UserModelTicket.objects.create(ticket=ticket,
                                               out_time=out_time, name_id=user.id)
                user.save()
                return response
            else:
                return render(request, 'user/user_login.html', {'password': '用户密码错误'})

        else:
            return render(request, 'user/user_login.html', {'username': '用户不存在'})


def regist(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        sex = request.POST.get('sex')
        sex = 1 if sex else 0
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)
        icon = request.FILES.get('icon')
        UserModel.objects.create(
            username=username,
            password=password,
            email=email,
            icon=icon,
            sex=sex
        )
        return HttpResponseRedirect('/axf/login/')


def mine(request):
    if request.method == 'GET':
        user = request.user
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user_id = UserModelTicket.objects.get(ticket=ticket).name_id
            user = UserModel.objects.get(id=user_id)
            if user.id:
                orders = user.ordermodel_set.all()
                wait_pay, payed = 0, 0
                for order in orders:
                    if order.o_status == 0:
                        wait_pay += 1
                    elif order.o_status == 1:
                        payed += 1
                # data['wait_pay']: wait_pay
                # data['payed']: payed
                # data['id']: user.id
                data = {"id": user.id,
                        "username": user.username,
                        "wait_pay": wait_pay,
                        "payed": payed,
                        "icon": user.icon
                        }
                return render(request, 'mine/mine.html', data)
        else:
            user.id = False
            return render(request, 'mine/mine.html')


def cart(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            return render(request, 'cart/cart.html')
        else:
            return HttpResponseRedirect('/axf/login/')


def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/axf/home/')
        response.delete_cookie('ticket')
        ticket = request.COOKIES.get('ticket')
        UserModelTicket.objects.filter(ticket=ticket).delete()
        return response


def market(request):
    return HttpResponseRedirect(reverse('axf:marketparams', args=('104749', '0', '0')))


def marketparams(request, typeid, cid, sort_id):
    data = {}
    if request.method == 'GET':

        foodtypes = FoodType.objects.all()
        foodtypes_childnames = FoodType.objects.filter(typeid=typeid).first()
        childtypenames = foodtypes_childnames.childtypenames
        childtypenames_list = childtypenames.split('#')
        child_type_list = []
        for childtypename in childtypenames_list:
            child_type_list.append(childtypename.split(':'))
        if cid == '0':
            goods_types = Goods.objects.filter(categoryid=foodtypes_childnames.typeid)
        else:
            goods_types = Goods.objects.filter(categoryid=foodtypes_childnames.typeid, childcid=cid)
        if sort_id == '0':
            pass
        elif sort_id == '1':
            goods_types = goods_types.order_by('productnum')
        elif sort_id == '2':
            goods_types = goods_types.order_by('-price')
        elif sort_id == '3':
            goods_types = goods_types.order_by('price')
            data["goods_types"] = goods_types
        data = {
            "foodtypes": foodtypes,
            "goods_types": goods_types,
            "child_type_list": child_type_list,
            "sort_id": sort_id,
            "typeid": typeid,
            "cid": cid
        }
    else:
        HttpResponseRedirect('axf/login/')

    return render(request, 'market/market.html', data)


def add_goods(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user_id = UserModelTicket.objects.get(ticket=ticket).name_id
            user = UserModel.objects.get(id=user_id)
            print(user)
            if user and user.id:
                goods_id = request.POST.get('goods_id')
                # 获取购物车信息
                user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
                # 如果用户选了商品
                if user_carts:
                    user_carts.c_num += 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
                else:
                    # 如果用户没选商品，就创建
                    CartModel.objects.create(user=user,
                                             goods_id=goods_id,
                                             c_num=1)
                    data['c_num'] = 1
            return JsonResponse(data)


def sub_goods(request):
    if request.method == "POST":
        data = {
            "code": '200',
            "msg": "请求成功"
        }
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user_id = UserModelTicket.objects.get(ticket=ticket).name_id
            user = UserModel.objects.get(id=user_id)
            if user and user.id:
                goods_id = request.POST.get('goods_id')
                user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
                if user_carts:
                    if user_carts.c_num == 1:
                        user_carts.delete()
                        data["c_num"] = 0
                    else:
                        user_carts.c_num -= 1

                        data["c_num"] = user_carts.c_num
                        user_carts.save()
            return JsonResponse(data)


def cart(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user_id = UserModelTicket.objects.get(ticket=ticket).name_id
            user = UserModel.objects.get(id=user_id)
            if user and user.id:
                data = {}
                # 如果用户已经登录，则加载购物车的数据
                carts = CartModel.objects.filter(user=user)
                data['carts']=carts
                allmoney = changeMoney(carts)
                data['allmoney']=allmoney
                return render(request, 'cart/cart.html', data)
            else:
                return HttpResponseRedirect('/axf/login/')


def changeCartSelect(request):
    if request.method == 'POST':
        data = {
            "code": "200",
            "msg": "请求成功"
        }
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user_id = UserModelTicket.objects.get(ticket=ticket).name_id
            user = UserModel.objects.get(id=user_id)
            cart_id = request.POST.get('cart_id')
            if user and user.id:
                data["username"] = user.username
                cart = CartModel.objects.filter(id=cart_id).first()
                if cart.is_select:
                    cart.is_select = False
                else:
                    cart.is_select = True
                cart.save()
                data["is_select"] = cart.is_select
            return JsonResponse(data)


def makeOrder(request):
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user_id = UserModelTicket.objects.get(ticket=ticket).name_id
            user = UserModel.objects.get(id=user_id)
            if user and user.id:
                # 在购物车中筛选被勾中的数据
                cart_goods = CartModel.objects.filter(is_select=True)


                order = OrderModel.objects.create(user_id=user_id, o_status=0)

                for cart_good in cart_goods:
                    OrderGoodsModel.objects.create(
                        order=order,
                        goods_id=cart_good.goods_id,
                        goods_num=cart_good.c_num

                    )
                cart_goods.delete()

                return HttpResponseRedirect(reverse('axf:payOrder', args=(str(order.id),)))


def payOrder(request, order_id):
    if request.method == 'GET':
        orders = OrderModel.objects.filter(pk=order_id).first()
        data = {
            'order_id': order_id,
            'orders': orders
        }

        return render(request, 'order/order_info.html', data)


def pay(request, order_id):
#  修改订单状态
    if request.method=='GET':
        OrderModel.objects.filter(id=order_id).update(o_status=1)

        return HttpResponseRedirect('/axf/mine/')


def wait_pay(request):

    if request.method =='GET':
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user_id = UserModelTicket.objects.get(ticket=ticket).name_id
            user = UserModel.objects.get(id=user_id)
            if user and user.id:
                orders = OrderModel.objects.filter(o_status=0,user_id=user_id)


                return render(request, 'order/order_list_wait_pay.html', {'orders': orders})


def wait_get(request):
    if request.method == 'GET':

        user = request.user
        ticket = request.COOKIES.get('ticket')
        if ticket:
            user_id = UserModelTicket.objects.get(ticket=ticket).name_id
            user = UserModel.objects.get(id=user_id)
            if user and user.id:
                orders = OrderModel.objects.filter(user=user, o_status=1)

                return render(request, 'order/order_list_payed.html', {'orders': orders})

def changeMoney(carts):
    carts = CartModel.objects.filter(is_select=True)
    allmoney = 0
    for cart in carts:
        allmoney += cart.goods.price * cart.c_num

    return float(allmoney)




