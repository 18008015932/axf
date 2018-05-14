from APP import views
from django.conf.urls import url

urlpatterns = [
    url(r'^home/', views.home),
    url(r'^regist/', views.regist),
    url(r'^login/', views.login),
    url(r'^mine/', views.mine),
    url(r'^cart/', views.cart),
    url(r'^logout', views.logout),
    url(r'^market/$', views.market, name='market'),
    url(r'^marketparams/(\d+)/(\d+)/(\d+)/', views.marketparams, name='marketparams'),
    url(r'^addgoods/', views.add_goods, name='addgoods'),
    url(r'^subgoods/', views.sub_goods, name='subgoods'),
    #购物车
    url(r'^cart/',views.cart,name='cart'),
    url(r'^changeCartSelect/',views.changeCartSelect,name='changeCartSelect'),
    #生成订单
    url(r'^makeOrder/',views.makeOrder,name='makeOrder'),
    #进入付款
    url(r'^payOrder/(\d+)/',views.payOrder,name='payOrder'),
    #付款
    url(r'^Pay/(\d+)/',views.pay,name='Pay'),

    # 待付款
    url(r'^waitPay',views.wait_pay,name='wait_pay'),

    #待收货
    url(r'^waitget/',views.wait_get,name='wait_get'),



    ]