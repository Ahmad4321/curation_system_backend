from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):
    return render(request,'index.html')



@csrf_exempt
@csrf_protect
def home_tabs(request):
    return render(request, "home_tab.html")

@csrf_exempt
@csrf_protect
def test(request):
    return render(request, "test2.html")


@csrf_exempt
def get_data(request):
    all_data = RTOdata.objects.all().values()
    data = []
    for line in all_data:
        data.append({'id': int(line['id']), 'tag': line['TAG'], 'level': int(line['LEVEL']), 'name': f"{line['CNAME'] } ({line['ENAME']})",
                    'ename': line['ENAME'], 'TOID': line['TOID'], 'parentId': int(line['PARENTID'])})

    # data = [
    #     {'id': 1, 'tag': '1', 'level': 1, 'name': '植株性状', 'ename': 'Plant trait', 'TOID': 'TO:0000387',
    #      'parentId': 0},
    #     {'id': 2, 'tag': '1.1', 'level': 2, 'name': '受力性状', 'ename': 'Stress trait', 'TOID': 'TO:0000164',
    #      'parentId': 1},
    #     {'id': 3, 'tag': '1.1.1', 'level': 3, 'name': '非生物胁迫特性', 'ename': 'Abiotic stress trait',
    #      'TOID': 'TO:0000168', 'parentId': 2}
    # ]

    # 构建树状结构
    tree = {}
    for item in data:
        item['children'] = []
        tree[item['id']] = item

    for item in data:
        parent_id = item['parentId']
        if parent_id in tree:
            tree[parent_id]['children'].append(item)

    # 获取根节点
    root = [item for item in tree.values() if item['parentId'] == 0]

    context = {'code': 0, 'message': 'hello', 'count': len(data), 'data': root}

    return JsonResponse(context, safe=False)

@csrf_exempt
def get_data_json(request):
    all_data = RTOdata.objects.all().values()
    data = []
    count = 0
    for line in all_data:
        val = {}
        data.append({'id': int(line['id']), 'tag': line['TAG'], 'level': int(line['LEVEL']), 'name': f"{line['CNAME'] } ({line['ENAME']})",
                    'ename': line['ENAME'], 'TOID': line['TOID'], 'parentId': int(line['PARENTID'])})


    # 构建树状结构
    tree = {}
    for item in data:
        item['children'] = []
        tree[item['id']] = item

    for item in data:
        parent_id = item['parentId']
        if parent_id in tree:
            tree[parent_id]['children'].append(item)

    # 获取根节点
    root = [item for item in tree.values() if item['parentId'] == 0]

    viewdata = {
        "name": "Root",
        "children": root
    }

    viewdata = viewdata #{'code': 0, 'message': 'hello', 'count': len(data), 'data': root}

    return JsonResponse(viewdata, safe=False)



@csrf_exempt
def get_data_jstree(request):
    all_data = RTOdata.objects.all().values()
    data = []
    count = 0
    
    for line in all_data:
        state = True if int(line['level']) < 3 else False
        data.append({'id': int(line['id']), 'tag': line['TAG'], 'level': int(line['LEVEL']), 'name': f"{line['CNAME'] } ({line['ENAME']})",
                    'ename': line['ENAME'], 'TOID': line['TOID'], 'parentId': int(line['PARENTID'])})
        
    # 构建树状结构
    tree = {}
    for item in data:
        item['children'] = []
        tree[item['id']] = item

    for item in data:
        parent_id = item['parentId']
        if parent_id in tree:
            tree[parent_id]['children'].append(item)

    # 获取根节点
    root = [item for item in tree.values() if item['parentId'] == 0]


    context = root #{'code': 0, 'message': 'hello', 'count': len(data), 'data': root}

    return JsonResponse(root, safe=False)


@csrf_protect
@csrf_exempt
def save_evaluation(request):
    if request.method == "POST":
        print("Here")
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        evaluation = body_data.get('evaluation')
        id = body_data.get('id')
        print(evaluation)

        # 在这里进行保存到数据库的逻辑
        evaluation_obj = RTOdata.objects.get(id=id)
        evaluation_obj.evaluation = evaluation
        evaluation_obj.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



def login(request):
    return render(request, "login.html")
