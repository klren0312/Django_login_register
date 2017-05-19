# Django 简单登录注册

## 1. 安装django 1.11
```
pip install django
```

## 2.安装pymysql
>我是Python3.5，所以必须用pymysql

```
pip install pymysql
```

## 3.用PyCharm新建项目
>项目名为finally，用`python manage.py startapp mysite`新建名为mysite的app。
用`python manage.py createsuperuser`创建后台用户。
具体目录结构

![目录.jpg](http://upload-images.jianshu.io/upload_images/2245742-bda4a17689ac57ed.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 4.配置数据库为mysql
```
文件路径 finally/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  'django',//数据库名
        'USER':'root',//mysql用户名
        'PASSWORD':'root',//mysql密码
        'HOST':'127.0.0.1',
        'PORT':'3306'
    }
}
```
还要引入包
```
文件路径 finally/__init__.py

import pymysql
pymysql.install_as_MySQLdb()

```

## 5.数据表生成
>Django 1.7以上 要用两句话来同步数据库
```
python manage.py makemigrations
python manage.py migrate
```

```
文件路径：mysite/models.py

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()

```

## 6.视图配置

 - 就是一些登录注册的路由，此处我关了csrf（具体可以在下面的相关问题解决处查看）
 - 很无奈，很多教程还在用render_to_response，但是我查了资料。render()方法是render_to_response的一个崭新的快捷方式，前者会自动使用RequestContext。而后者必须coding出来，这是最明显的区别，当然前者更简洁。


```
文件路径：mysite/views.py

from django.shortcuts import render
from django.http import HttpResponse
from mysite.models import User
from django.views.decorators.csrf import csrf_exempt
 
   #注册
@csrf_exempt
def regist(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        #此处遇坑
        k = User.objects.create(username=username,password=password,email=email)
        k.save()
        return HttpResponse('regist success!!!')
    else:
        return render(request, 'regist.html')
    return render(request, 'regist.html')

 #登录
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username__exact=username,password__exact=password)
        if user:
            return render(request,"index.html")
        else:
            return HttpResponse('用户密码错误，请再次登录')
    else:
        return render(request,"login.html")
    return render(request,"login.html")

 #首页
def index(request):
    return render(request,"index.html")
```

## 7.配置urls路径
```
文件路径：finally/urls.py

from django.conf.urls import url
from django.contrib import admin
from mysite import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^regist/$',views.regist),
    url(r'^index/$',views.index),
    url(r'^login/$',views.login),
]

```

## 8.相关页面
>没意思的部分

```
文件路径：templates/index.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>

    <style>
        html,body{
            text-align: center;
            margin: 0px auto;
        }
    </style>
</head>
<body>
    <h1>主界面</h1>
</body>
</html>
```
```
文件路径：templates/regist.html

<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>regist</title>

    <style>
        html,body{
            text-align: center;
            margin: 0px auto;
        }
    </style>
</head>
<body>
    <h1>注册界面</h1>
    <form method="post" action="http://127.0.0.1:8000/regist/" enctype="multipart/form-data">
        <label for="username">username:</label>
        <input type="text" name="username" id="username">
        <label for="password">password:</label>
        <input type="password" name="password" id="password">
        <label for="email">email:</label>
        <input type="email" name="email" id="email">
        <input type="submit" value="Regist">
    </form>
</body>
</html>
```
```
文件路径：templates/login.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>

    <style>
        html,body{
            text-align: center;
            margin: 0px auto;
        }
    </style>
</head>
<body>
    <h1>登录页面</h1>
    <form method="post" action="http://127.0.0.1:8000/login/">
        <label for="username">username:</label>
        <input type="text" name="username" id="username">
        <label for="password">password:</label>
        <input type="password" name="password" id="password">
        <input type="submit" value="Login">
    </form>
</body>
</html>
```

## 9.运行结果

![注册页面.jpg](http://upload-images.jianshu.io/upload_images/2245742-83f1283b0eba470b.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![注册成功.jpg](http://upload-images.jianshu.io/upload_images/2245742-e2cb1048147937ba.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![数据库.jpg](http://upload-images.jianshu.io/upload_images/2245742-9d8a8b8fa99a5dfc.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 10.遇到的问题

 - 报错`save() missing 1 required positional argument: 'self'`

原代码
```
        User.objects.create(username=username,password=password,email=email)
        User.save()
```

改后代码
```
        k = User.objects.create(username=username,password=password,email=email)
        k.save()
```

 - 2`[CSRF token missing or incorrect] `
>我很无奈，直接禁用。
在views.py中引入包
```
from django.views.decorators.csrf import csrf_exempt
```
在函数上面加`@csrf_exempt`


@治电小白菜20170518