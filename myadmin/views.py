from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from myadmin.models import Users


import time

def index(request):
    return render(request, "myadmin/index.html")


# ==========后台会员信息管理===========================
# 浏览会员
# def usersindex(request):
#     # 执行数据查询，并放置到模板中
#     list = Users.objects.all()
#     context = {"userslist":list}
#     #return HttpResponse(list)
#     return render(request, 'myadmin/users/index.html', context)

def usersindex(request,pIndex=1):
    list = Users.objects.all()
    #判断并封装搜索学生信息
    where = []
    if request.GET.get('name','') != '':
        list = list.filter(name__contains=request.GET['name'])
        where.append('name='+request.GET['name'])
    #传入数据和页的大小来创建对象
    p = Paginator(list,5)
    #判断页号没有初始值时初始化1
    if pIndex == '':
        pIndex = '1'
    pIndex = int(pIndex) #类型转换int
    list2 = p.page(pIndex)#获取当前页数据
    plist = p.page_range#获取页码信息
    #封装分页信息
    context = {'userslist':list2,'plist':plist,'pIndex':pIndex,'where':where}
    return render(request,'myadmin/users/index.html',context)

# 会员信息添加表单
def usersadd(request):
    return render(request, 'myadmin/users/add.html')


# 执行会员信息添加
def usersinsert(request):
    try:
        ob = Users()
        ob.username = request.POST['username']
        ob.name = request.POST['name']
        # 获取密码并md5
        import hashlib
        m = hashlib.md5()
        m.update(bytes(request.POST['password'],encoding="utf8"))
        ob.password = m.hexdigest()
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = 1
        ob.addtime = time.time()
        ob.save()
        context = {'info': '添加成功！'}
    except:
        context = {'info': '添加失败！'}

    return render(request, "myadmin/info.html", context)


# 执行会员信息删除
def usersdel(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.delete()
        context = {'info': '删除成功！'}
    except:
        context = {'info': '删除失败！'}
    return render(request, "myadmin/info.html", context)


# 打开会员信息编辑表单
def usersedit(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        context = {'user': ob}
        return render(request, "myadmin/users/edit.html", context)
    except:
        context = {'info': '没有找到要修改的信息！'}
    return render(request, "myadmin/info.html", context)


# 执行会员信息编辑
def usersupdate(request, uid):
    try:
        ob = Users.objects.get(id=uid)
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.state = request.POST['state']
        ob.save()
        context = {'info': '修改成功！'}
    except:
        context = {'info': '修改失败！'}
    return render(request, "myadmin/info.html", context)


# ===========后台管理员的登录退出操作=========================
# 会员登录表单
def login(request):
    return render(request, 'myadmin/login.html')


# 会员执行登录
def dologin(request):
    # 校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code'].lower()
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"myadmin/login.html",context)

    try:
        # 根据账号获取登录者信息
        user = Users.objects.get(username=request.POST['username'])
        # 判断当前用户是否是后台管理员用户
        if user.state == 0:
            # 验证密码
            import hashlib
            m = hashlib.md5()
            m.update(bytes(request.POST['password'], encoding="utf8"))
            if user.password == m.hexdigest():
                # 此处登录成功，将当前登录信息放入到session中，并跳转页面
                request.session['adminuser'] = user.name
                # print(json.dumps(user))
                return redirect(reverse('myadmin_index'))
            else:
                context = {'info':'登录密码错误！'}
        else:
            context = {'info':'此用户非后台管理用户！'}
    except:
        context = {'info': '登录账号错误！'}
    return render(request, "myadmin/login.html", context)


# 会员退出
def logout(request):
    # 清除登录的session信息
    del request.session['adminuser']
    # 跳转登录页面（url地址改变）
    return redirect(reverse('myadmin_login'))
    # 加载登录页面(url地址不变)
    # return render(request,"myadmin/login.html")


# ==============后台管理员操作====================
# 会员登录表单
def verify(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    # bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    bgcolor = (150, 154, 194)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点

    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = 'ABCDEFGHIJasdfghjk'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('static/fonts/STXIHEI.TTF', 23)
    # font = ImageFont.load_default().font
    for i in range(0, 4):
        # 构造字体颜色
        fontcolor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        # 绘制4个字
        draw.text((5 + i * 24, -4), rand_str[i], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str.lower()
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


