from django.conf.urls import url

from . import views

urlpatterns = [
    # ===========商品展示==================
    url(r'^$', views.index, name='index'),  # 网站首页
    url(r'^list$', views.list, name='list'),  # 商品列表页
    url(r'^detail/(?P<gid>[0-9]+)$', views.detail, name='detail'),  # 商品详情
    url(r'^login$', views.login, name='login'),  # 登陆
    url(r'^logindl$', views.logindl, name='logindl'),
    url(r'^register$', views.register, name='register'),  # 注册
    url(r'^registerzc$', views.registerzc, name='registerzc'),
    url(r'^loginout$', views.loginout, name='loginout'),  # 退出


    # ===========会员模块==================
    url(r'^member$', views.member, name='member'),  # 个人中心
    url(r'^edit_member$', views.edit_member, name='edit_member'),  # 修改个人信息
    url(r'^edit_memberxg$', views.edit_memberxg, name='edit_memberxg'),  # 修改个人信息


    # ===========购物车模块================
    url(r'^cart$', views.cart, name='cart'),
    url(r'^cartadd/(?P<sid>[0-9]+)$', views.cartadd, name='cartadd'),
    url(r'^cartclaer$', views.cartclear, name='cartclear'),
    url(r'^cartdel/(?P<sid>[0-9]+)$', views.cartdel, name='cartdel'),
    url(r'^cartchange$', views.cartchange, name='cartchange'),


    # ===========订单模块==================
    url(r'^orderform$', views.orderform, name='orderform'),  # 订单表单
    url(r'^orderqr$', views.orderqr, name='orderqr'),  # 收货人信息修改
    # url(r'^orderconfirm$', views.orderconfirm, name='order_confirm'),  # 订单确认页
    url(r'^orderxd$', views.orderxd, name='orderxd'),  # 确认下单
    url(r'^order$',  views.myorder, name='myorder'),  # 我的订单页
    url(r'orderxq$', views.orderxq, name='orderxq'),  # 订单详情
    url(r'orderztxg/(?P<gid>[0-9]+)$', views.orderztxg, name='qt_ztxg')  # 状态修改

]