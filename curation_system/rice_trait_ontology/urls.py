from django.urls import path

from .views import index,login_view,get_data,get_data_json,get_data_jstree,save_evaluation

    

urlpatterns = [
    path("", index, name="home"),
    path("login/", login_view, name="login"),
    path("get_data/", get_data, name="get_data"),
    path("get_data_json/", get_data_json, name="get_data_json"),
    path("get_data_jstree/",get_data_jstree,name="jstree"),
    path("save_evaluation/", save_evaluation, name="save_evaluation"),
]