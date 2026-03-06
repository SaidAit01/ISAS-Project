from django.urls import path
from . import views 

urlpatterns = [ 
    path('run-algo/', views.run_allocation_algorithm, name='run_allocation'), 
    path('add-student/', views.add_student_api, name='add_student'),
    path('add-supervisor/', views.add_supervisor_api, name='add_supervisor'),
    
    # --- OUR NEW CONFIGURATION ENDPOINT ---
    path('get-config/', views.get_system_config, name='get_config'),
]