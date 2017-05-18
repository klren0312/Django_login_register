from django.shortcuts import render
from django.http import HttpResponse
from mysite.models import User
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
#render()方法是render_to_response的一个崭新的快捷方式，前者会自动使用RequestContext。
# 而后者必须coding出来，这是最明显的区别，当然前者更简洁。
@csrf_exempt
def regist(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        k = User.objects.create(username=username,password=password,email=email)

        k.save()

        return HttpResponse('regist success!!!')
    else:
        return render(request, 'regist.html')
    return render(request, 'regist.html')

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

def index(request):
    return render(request,"index.html")


