from django.urls import path
from .import views 

urlpatterns = [ 
    path('run-algo/', views.run_allocation_algorithm, name =  'run_allocation'), 
]