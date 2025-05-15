from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request,'index.html')


@csrf_exempt
def get_data(request):
    all_data = rtoData.objects.all().values()
    data = []
    for line in all_data:
        data.append({'id': int(line['id']), 'tag': line['TAG'], 'level': int(line['LEVEL']), 'name': f"{line['CNAME'] } ({line['ENAME']})",
                    'ename': line['ENAME'], 'TOID': line['TOID'], 'parentId': int(line['PARENTID'])})
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
    rto_list = rtoData.objects.prefetch_related('trait_evaluations').all().values(
        'id', 'tag', 'level', 'cname', 'ename', 'toid', 'parent_id',
        'pubAnnotation_evidence', 'llm_evidence', 'rice_alterome_evidence',
        'created_at', 'updated_at', 'created_by__username', 'updated_by__username','created_by__id', 'updated_by__id'
    )
    data = []
    
    for line in rto_list:
        data.append({'id': int(line['id']), 'tag': line['tag'], 'level': int(line['level']), 'name': f"{line['cname'] } ({line['ename']})",
                    'ename': line['ename'], 'toid': line['toid'], 'parentId': int(line['parent_id']),
                    'pubAnnotation_evidence': line['pubAnnotation_evidence'],'llm_evidence': line['llm_evidence'],
                    'rice_alterome_evidence': line['rice_alterome_evidence'],'created_at': line['created_at'],'updated_at': line['updated_at'],'evaluations': list(line.pop('trait_evaluations', [])),
                    'created_by': line['created_by__username'],'updated_by': line['updated_by__username'],'created_by_id': line['created_by__id'],'updated_by_id': line['updated_by__id']})

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

    return JsonResponse(root, safe=False)



@csrf_exempt
def get_data_distinct(request):
    distinct_names = list(rtoData.objects.values('ename').distinct())
        

    # 获取根节点
    root = [item['ename'] for item in distinct_names]


    context = root #{'code': 0, 'message': 'hello', 'count': len(data), 'data': root}

    return JsonResponse(context, safe=False)


@csrf_protect
@csrf_exempt
def save_actions(request):
    if request.method == "POST":


        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        
        evaluation_object = body_data.get('evaluation')
        id = body_data.get('id')
        # Saving and creating the evaluation against the trait
        evaluation_obj = trait_evaluation.objects.create(
            evaluation=evaluation_object.evaluation,
            trait_id=rtoData.objects.get(id=evaluation_object.id),
            expert_name=evaluation_object.expert_name,
            created_by=evaluation_object.created_by,
            updated_by= evaluation_object.updated_by,
        )
        evaluation_obj.save()


        # Saving the action performed
        action_object = body_data.get('action_performed')
        action_performed_obj = ActionPerformed(
            action_code=action_object.action_code,
            action_name=action_object.action_name,
            trait_name=action_object.trait_name,
            performed_by=action_object.performed_by,
            is_active=True,
            is_resolved=True,
            created_by=action_object.created_by,
            updated_by=action_object.updated_by,
            trait_id=rtoData.objects.get(id=action_object.id),
            trait_reference=action_object.trait_reference,
            # Assuming you want to set the created_at and updated_at fields automatically
        )
        action_performed_obj.save()




        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Sigup module
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({"message": "User created successfully"})


# Sign in module
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # optional: sets session
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

# Logoutform
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    else:            
        return JsonResponse({'error': 'Invalid request method'}, status=400)