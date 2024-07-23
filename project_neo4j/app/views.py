from app.models import DataToNeo4j
import os
from project_neo4j import settings
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate

username = 'neo4j'
password = '58094894'
app = DataToNeo4j()


# Create your views here.


# csrf 用于form表单中，作用是跨站请求伪造保护。
@csrf_exempt
def login(request):
    response = {}
    try:

        if request.method == 'POST':
            request = json.loads(request.body.decode('utf-8'))
            if request.get('username') == username and request.get('password') == password:
                # user = authenticate(username=username, password=password)
                # if user is not None:
                #     old_token = Token.objects.filter(user=user)
                #     old_token.delete()
                #     token = Token.objects.create(user=user)
                # else:
                #     user = User.objects.create_user(username=username, password=password)
                #     token = Token.objects.create(user=user)

                response['data'] = '登录neo4j数据库成功'
                response['status'] = 200
                response['token'] = 1
            else:

                response['data'] = '登录账户或密码错误'
                response['status'] = 201
        else:
            response['data'] = '请求格式错误'
            response['error_num'] = 1
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


def example_data(request):
    response = {}
    # token = request.META.get("HTTP_AUTHORIZATION")
    # user = User.objects.filter(token=token)
    # if not user:
    # return 1

    try:
        # app = DataToNeo4j(username, password)
        attr = app.get_example('web of science')
        response['status'] = 200
        response['attr'] = attr
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


def insert_key(request):
    response = {}
    # token = request.META.get("HTTP_AUTHORIZATION")
    # user = User.objects.filter(token=token)
    # if not user:
    # return 1
    try:
        # app = DataToNeo4j(username, password)
        app.key = request.GET.get('key')
        print(request.GET.get('key'))
        response['status'] = 200

    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


def search(request):
    response = {}
    # token = request.META.get("HTTP_AUTHORIZATION")
    # user = User.objects.filter(token=token)
    # if not user:
    # return 1
    try:
        # app = DataToNeo4j(username, password)
        title, author, address, num = app.search(int(request.GET.get('pagenum')),
                                                 int(request.GET.get('pagesize')), request.GET.get('key'))
        response['status'] = 200
        response['title'] = title
        response['author'] = author
        response['address'] = address
        response['num'] = num
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


def create(request):
    response = {}
    try:
        print('begin')
        app.create_node()
        app.create_cooperate_node()
        response['status'] = 200
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


@csrf_exempt
def getfile(request):
    response = {}
    print('11111')
    if request.method == 'POST':
        print('begin')
        file = request.FILES['file']
        # key = file.name.strip('.txt').lower()
        if not os.path.exists(os.path.join(settings.UPLOAD_ROOT, app.key)):
            os.makedirs(os.path.join(settings.UPLOAD_ROOT, app.key))
            print(os.path.join(settings.UPLOAD_ROOT, app.key))
        file = os.path.join(os.path.join(settings.UPLOAD_ROOT, app.key), file.name)
        with open(file, 'wb') as f:
            for file_line in request.FILES['file'].chunks():
                f.write(file_line)
        app.read_wos_txt(file)
        print('ok')
        # app.create_node()
        # app.create_cooperate_node()
    # try:
    #     if request.method == 'POST':
    #         file = request.FILES['file']
    #         file = os.path.join(settings.UPLOAD_ROOT, file.name)
    #         print(file)
    #         with open(file, 'wb') as f:
    #             for file_line in request.FILES['file'].chunks():
    #                 f.write(file_line)
    #         app.read_wos_txt(file)
    #         app.create_node()
    #         response['data'] = '上传成功'
    #         response['status'] = 200
    # except Exception as e:
    #     response['data'] = str(e)
    #     response['status'] = 201
    return JsonResponse(response)


def datadetail(request):
    response = {}
    # token = request.META.get("HTTP_AUTHORIZATION")
    # user = User.objects.filter(token=token)
    # if not user:
    # return 1
    print(request.GET.get('title'))
    attr, value = app.getdetail(request.GET.get('title'))
    try:
        # app = DataToNeo4j(username, password)
        attr, value = app.getdetail(request.GET.get('title'))

        response['status'] = 200
        response['attr'] = attr
        response['value'] = value
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


# def download(request):
#     response = {}
#     if app.search_now is None:
#         response['data'] = '当前下载内容为空'
#         response['status'] = 201
#         return JsonResponse(response)
#     try:
#
#         num = len(os.listdir(settings.DOWNLOAD_ROOT))
#
#         app.write_wos_txt(
#             os.path.join(settings.DOWNLOAD_ROOT, 'download({}).{}'.format(num, request.GET.get('type'))),
#             request.GET.get('type'))
#         response['data'] = '下载成功,文件在{}'.format(
#             os.path.join(settings.DOWNLOAD_ROOT, 'download({}).{}'.format(num, request.GET.get('type'))))
#         response['status'] = 200
#     except Exception as e:
#         response['data'] = str(e)
#         response['status'] = 201
#     return JsonResponse(response)

def download(request):
    response = {}
    if app.search_now is None:
        response['data'] = '当前下载内容为空'
        response['status'] = 201
        return JsonResponse(response)
    try:

        num = len(os.listdir(settings.DOWNLOAD_ROOT))

        app.write_wos_txt(
            os.path.join(settings.DOWNLOAD_ROOT, 'download({}).{}'.format(num, request.GET.get('type'))),
            request.GET.get('type'))
        response['data'] = os.path.join(settings.STATIC_URL + 'download',
                                        'download({}).{}'.format(num, request.GET.get('type')))
        response['status'] = 200
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


def statistics(request):
    response = {}
    try:
        data = app.statistics()
        response['data'] = data
        response['status'] = 200
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


def get_country(request):
    response = {}
    print(request.GET.get('key'))
    try:
        data = app.get_country(request.GET.get('key'))
        response['data'] = data
        response['status'] = 200
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


def get_keyword(request):
    response = {}
    try:
        data = app.get_keyword()
        response['data'] = data
        response['status'] = 200
    except Exception as e:
        response['data'] = str(e)
        response['status'] = 201
    return JsonResponse(response)


from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world!")  # 简单的响应，用于测试
