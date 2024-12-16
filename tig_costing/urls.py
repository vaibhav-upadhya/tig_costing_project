# tig_costing/urls.py

from django.urls import path
from . import views

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

    # Admin Features (e.g., creating dynamic fields)
    path('admin/create-field/', views.create_dynamic_field, name='create_dynamic_field'),

    # Testing Views (optional, can be removed in production)
    path('test/', views.test_view, name='test_view'),
]
