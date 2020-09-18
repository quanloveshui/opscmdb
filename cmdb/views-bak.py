from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import json

from cmdb.models import Table



#登录
def acc_login(request):

    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print(request.POST)
        #仅认证
        user = authenticate(username=username, password=password)
        if user:
            print("passed authencation", user)
            #认证通过后登录
            login(request, user)
            return redirect('/')
        else:
            error_msg = "Wrong username or password!"
    return render(request, 'cmdb/login.html', {'error_msg': error_msg})


#登出
def acc_logout(request):
    logout(request)
    return redirect("/login/")



@login_required
def table(request):
    if request.method == 'GET':
        _lists = Table.objects.all().order_by('id')

        return render(request, 'cmdb/table.html', {'lPage': _lists})


def change_table(request):
    if request.method == 'GET':
        try:
            _data = get_object_or_404(Table, id=request.GET.get('id'))

            jsondata = model_to_dict(_data, exclude=['create_time', 'update_time'])
            print(">>>>>>>jsondata:",jsondata)
            return JsonResponse({'state': 1, 'message': jsondata})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Get Error: ' + str(e)})

    if request.method == 'POST':
        print(request.body.decode('utf-8'))

        postdata = {}
        for key, value in json.loads(request.body.decode('utf-8')).items():
            # 将接收到的json数据去掉csrf之后的数据存入字典postdata
            if key != 'csrfmiddlewaretoken':
                postdata[key] = value if value != '' else None
        print('>>>>>',postdata)



        try:
            # 根据传入的ID判断是新建还是更新   update_or_create(defaults=None, **kwargs)  defaults是用来更新的， kwargs是用来查询的
            object, created = Table.objects.update_or_create(
                id=postdata.get('id'),
                defaults=postdata
            )

            print('>>>>object',object)
            print('>>>>created', created)

            if created:
                return JsonResponse({'state': 1, 'message': '创建成功!'})
            else:
                return JsonResponse({'state': 1, 'message': '更新成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Error: ' + str(e)})


def delete_table(request):
    if request.method == 'POST':
        try:
            _t = Table.objects.filter(id=request.POST.get('id'))
            _t.delete()

            return JsonResponse({'state': 1, 'message': '删除成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Error: ' + str(e)})



