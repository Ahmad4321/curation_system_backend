from django.urls import path

from .views import index,login_view,get_data,get_data_json,get_data_distinct,save_actions,register_view,logout_view,getevaluation_data

    

urlpatterns = [
    path("", index, name="home"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("get_data/", get_data, name="get_data"),
    path("fetch_trait_evalutation/", getevaluation_data, name="getevaluation_data"),
    path("get_data_json/", get_data_json, name="get_data_json"),
    path("curation_system_trait/",get_data_distinct,name="trait_list"),
    path("save_action_evaluation/",save_actions , name="save_actions"),
]