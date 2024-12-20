# tig_costing/urls.py

from django.urls import path
from . import views
from .views import get_costing_data
from .views import generate_excel

urlpatterns = [

    # Home page
    path('', views.home, name='home'),
    
    # Costing Management
    path('add_costing/<int:expense_head_id>/', views.add_costing, name='add_costing'),

    # View costing page
    path('view_costing/<int:expense_head_id>/', views.view_costing, name='view_costing'),

    # API Endpoints for dynamic dropdowns (if using AJAX, otherwise not needed)
    path('load-expense-fields/', views.load_expense_fields, name='load_expense_fields'),
    path('load-expense-heads/', views.load_expense_heads, name='load_expense_heads'),

    path('api/costing/<int:expense_head_id>/', get_costing_data, name='get_costing_data'),

    # Admin Features (e.g., creating dynamic fields)
    path('admin/create-field/', views.create_dynamic_field, name='create_dynamic_field'),

    path('costing-structure/', views.generate_nested_costing_structure, name='costing_structure'),

    # Testing Views (optional, can be removed in production)
    path('test/', views.test_view, name='test_view'),

    #creating costing automaticaly when expense_type created

    path('add_expense_type/', views.add_expense_type, name='add_expense_type'),

    #download excel Functinality
    path('download-excel/', generate_excel, name='download_excel'),
]
2