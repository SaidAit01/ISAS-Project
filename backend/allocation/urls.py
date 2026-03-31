from django.urls import path
from . import views 

urlpatterns = [ 
    path('run-algo/', views.run_allocation_algorithm, name='run_allocation'), 
    path('add-student/', views.add_student_api, name='add_student'),
    path('add-supervisor/', views.add_supervisor_api, name='add_supervisor'),
    path('config/', views.get_system_config, name='config'),
    path('suggest-supervisors/', views.suggest_supervisors_api),
    path('my-students/<str:supervisor_name>/', views.get_supervisor_students_api, name='my_students'),
    path('supervisor-profile/<str:supervisor_name>/', views.get_supervisor_profile_api, name='supervisor_profile'),
    path('directory/', views.get_all_supervisors_api, name='supervisor_directory'),

]