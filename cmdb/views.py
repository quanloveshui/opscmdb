from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import json

from cmdb.models import Table,Info



def register(request):
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            error_msg='用户已经存在'
            return render(request, 'cmdb/register.html', {'error_msg': error_msg})
        else:
            User.objects.create_user(
                username=username,
                password=password,
            )
        return redirect('/')

    return render(request, 'cmdb/register.html', {'error_msg': error_msg})

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
        """
        field_obj = Info._meta.fields  # 获取字段对象
        field_list = [field_obj[i].name for i in range(len(field_obj))]  # 所有字段名组成列表
        print('>>>', field_list)
        field_list = field_list[1:]
        filed_name = [field_obj[i].verbose_name for i in range(len(field_obj))]  # 所有字段中文名组成列表
        filed_name = filed_name[1:]  # 去除第一个ID
        field_dic = dict(zip(field_list, filed_name))
        """
        try:
            _data = get_object_or_404(Table, id=request.GET.get('id'))

            jsondata = model_to_dict(_data, exclude=['create_time', 'update_time'])#用于将model实例转换为dict _data-><class 'cmdb.models.Table'>
            #print(">>>>>>>jsondata:",jsondata)
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
        #print('>>>>>',postdata)

        try:
            # 根据传入的ID判断是新建还是更新   update_or_create(defaults=None, **kwargs)  defaults是用来更新的， kwargs是用来查询的
            object, created = Table.objects.update_or_create(
                id=postdata.get('id'),
                defaults=postdata
            )

            #print('>>>>object',object)
            #print('>>>>created', created)

            if created:
                return JsonResponse({'state': 1, 'message': '创建成功!'})
            else:
                return JsonResponse({'state': 1, 'message': '更新成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Error: ' + str(e)})


def detail_table(request):
    if request.method == 'GET':
        try:
            _data = get_object_or_404(Table, id=request.GET.get('id'))

            table_data = model_to_dict(_data, exclude=['create_time', 'update_time'])
            try:
                info_data=model_to_dict(Info.objects.get(ip=_data.host))
                #info_all=dict(info_data,**table_data)
                #print(info_data)
                return JsonResponse({'state': 1, 'message': table_data})
            except:
                return JsonResponse({'state': 2, 'message': table_data})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Get Error: ' + str(e)})


def delete_table(request):
    if request.method == 'POST':
        try:
            _t = Table.objects.filter(id=request.POST.get('id'))
            _t.delete()

            return JsonResponse({'state': 1, 'message': '删除成功!'})
        except Exception as e:
            return JsonResponse({'state': 0, 'message': 'Error: ' + str(e)})



