# 自定义后台中间件类
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import re

class AdminMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        # 定义网站后台不用登录也可访问的路由url
        urllist = ['/myadmin/login', '/myadmin/dologin', '/myadmin/logout', '/myadmin/verify']
        # 获取当前请求路径
        path = request.path
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match("/myadmin",path) and (path not in urllist):
            # 判断当前用户是否没有登录
            if "adminuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('myadmin_login'))



        # 获取当前请求路径
        path = request.path
        if re.match("/member", path):
            if "username" not in request.session:
                return redirect(reverse('login'))
        if re.match("/cart", path):
            if "username" not in request.session:
                return redirect(reverse('login'))

        # 不登陆或购物车没有商品时，访问收货地址页跳转到购物车页
        if re.match("/orderform", path):
            if "username" not in request.session:
                return redirect(reverse('login'))
        if re.match("/orderform", path):
            if request.session['shoplist'] == {}:
                return redirect(reverse('cart'))

        # 不登陆或购物车没有商品时，访问订单确认页跳转到购物车页
        if re.match("/order", path):
            if "username" not in request.session:
                return redirect(reverse('login'))
        # if re.match("/order", path):
        #     if request.session['shoplist'] == {}:
        #         return redirect(reverse('cart'))






        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response