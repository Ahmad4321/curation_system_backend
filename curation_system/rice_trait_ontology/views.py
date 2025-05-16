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
    rto_list = rtoData.objects.all().values('id','tag', 'level', 'cname', 'ename', 'toid', 'parent_id','pubAnnotation_evidence','llm_evidence','rice_alterome_evidence','created_at','updated_at','created_by__username','updated_by__username','created_by__id','updated_by__id')
    data = []

    for line in rto_list:
        data.append({'id': int(line['id']), 'tag': line['tag'], 'level': int(line['level']), 'name': f"{line['cname'] } ({line['ename']})",
                    'ename': line['ename'], 'toid': line['toid'], 'parentId': int(line['parent_id']),
                    'pubAnnotation_evidence': line['pubAnnotation_evidence'],'llm_evidence': line['llm_evidence'],
                    'rice_alterome_evidence': line['rice_alterome_evidence'],'created_at': line['created_at'],'updated_at': line['updated_at'],
                    'created_by': line['created_by__username'],'updated_by': line['updated_by__username'],'created_by_id': line['created_by__id'],'updated_by_id': line['updated_by__id']})

    
    # for line in rto_list:
    #     data.append({'id': int(line.id), 'tag': line.tag, 'level': int(line.level), 'name': f"{line.cname } ({line.ename})",
    #                 'ename': line.ename, 'toid': line.toid, 'parentId': int(line.parent_id),
    #                 'pubAnnotation_evidence': line.pubAnnotation_evidence,'llm_evidence': line.llm_evidence,
    #                 'rice_alterome_evidence': line.rice_alterome_evidence,'created_at': line.created_at,'updated_at': line.updated_at,
    #                 'created_by': line.created_by.username,'updated_by': line.updated_by.username,'created_by_id': line.created_by.id,'updated_by_id': line.updated_by.id})

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
def getevaluation_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        trait_id = data.get("trait_id")
        print("Trait ID:", trait_id)
        all_data = TraitEvaluation.objects.filter(trait_id=trait_id).values('id','evaluation', 'expert_name', 'created_at', 'updated_at', 'created_by_id')
        data = []
        for line in all_data:
            data.append({'id': int(line['id']), 'evaluation': line['evaluation'], 'expert_name': line['expert_name'],
                        'created_at': line['created_at'], 'updated_at': line['updated_at']})
        context = {'code': 0, 'message': 'hello', 'count': len(data), 'data': data}
        return JsonResponse(context, safe=False)

    else:
        context = {'code': 0, 'message': 'hello', 'count': 0, 'data': []}
        return JsonResponse(context, safe=False)

    

@csrf_exempt
def get_data_distinct(request):
    distinct_names = list(rtoData.objects.values('ename').distinct())
        

    # 获取根节点
    root = [item['ename'] for item in distinct_names]


    context = root #{'code': 0, 'message': 'hello', 'count': len(data), 'data': root}

    return JsonResponse(context, safe=False)



def save_evalutation(comment,expert_name,user,trait_id):
    exper_name_value =   user.get("username") if user else expert_name
    user_id =  user.get("id") if user else 1

    rto_instance = rtoData.objects.get(id=trait_id)
    user = User.objects.get(id=user_id)

    # Saving and creating the evaluation against the trait
    evaluation_obj = TraitEvaluation.objects.create(
        evaluation=comment,
        trait_id= rto_instance,
        expert_name= exper_name_value,
        created_by= user,
        updated_by= user,
    )
    evaluation_obj.save()
    return evaluation_obj


def save_action_performed(action_code,action_name,user,trait_reference,is_active,is_resolved):
    rto_instance = rtoData.objects.get(id=trait_reference.get("id"))
    user_instance = User.objects.get(id=user.get("id")) if user else User.objects.get(id=1)

    # parsed_trait_reference = json.loads(trait_reference)
    # trait_reference= parsed_trait_reference

    # Saving and creating the evaluation against the trait
    action_obj = ActionPerformed.objects.create(
        action_name=action_name,
        performed_by= user.get("username"),
        is_active= is_active,
        is_resolved= is_resolved,
        trait_id= rto_instance,
        trait_reference= trait_reference,
        created_by=user_instance,
        updated_by=user_instance
    )
    action_obj.save()
    return action_obj

@csrf_exempt
def save_actions(request):
    if request.method == "POST":
        data = json.loads(request.body)
        comment = data.get("comment")
        expert_name = data.get("expert_name") 
        user = data.get("user")
        trait = data.get("trait")
        trait_id = trait.get("id")
        is_active = True
        is_resolved = True
        action_code = None
        action_name = None
        if data.get("function"):


            if data.get("function") == "add":
                action_code = "1001"
                action_name = data.get("function")  
            elif data.get("function") == "merge":
                action_code = "1002"
                action_name = data.get("function")
            elif data.get("function") == "remove":
                action_code = "1003"
                action_name = data.get("function")    
            elif data.get("function") == "remain":
                action_code = "1004"
                action_name = data.get("function")
            
            if action_code == "1004":
                is_active = False
                is_resolved = False
            
            save_action = save_action_performed(action_code,action_name,user,trait,is_active,is_resolved)
            saved_eval = save_evalutation(comment,expert_name,user,trait_id)

            return JsonResponse({'success': True,"evaluation": "saved", 'action_performed':"saved",'msg': "Thank you for your feedback! Your evaluation has been saved successfully. Incase of add/merge/remove, administrator will review your feedback and take action accordingly."})

        saved_eval = save_evalutation(comment,expert_name,user,trait_id)


        return JsonResponse({'success': True,"evaluation": "saved", 'action_performed':"saved",'msg': "Thank you for your feedback! Your evaluation has been saved successfully.",'evaluation': { 'id': saved_eval.id, 'evaluation': saved_eval.evaluation, 'expert_name': saved_eval.expert_name, 'created_at': saved_eval.created_at}})
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
            
            return JsonResponse({"message": "Login successful",'user': { 'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name }})
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