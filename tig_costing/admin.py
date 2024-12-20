from datetime import datetime
from django.contrib import admin
from .models import ExpenseHead, Department, ExpenseField, Costing, AuditTrail, ExpenseType

# Inline for ExpenseField under ExpenseHead
class ExpenseFieldInline(admin.TabularInline):
    model = ExpenseField
    extra = 1  # Number of empty fields to show by default in the admin panel
    show_change_link = True  # Allow linking to ExpenseField's admin page

    # Custom handling for "Other Department"
    def save_new_instance(self, request, obj, form, change):
        if obj.department.name.lower() == "other department":
            # Handle dynamic department creation
            new_department_name = form.cleaned_data.get("new_department_name")
            if new_department_name:
                department, created = Department.objects.get_or_create(
                    name=new_department_name, is_dynamic=True
                )
                obj.department = department
        super().save_new_instance(request, obj, form, change)


# Admin for ExpenseHead
@admin.register(ExpenseHead)
class ExpenseHeadAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")  # Show these columns in admin listing
    search_fields = ("name",)  # Add a search bar for the name field
    inlines = [ExpenseFieldInline]  # Allow adding fields inline under an expense head


# Admin for Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_dynamic")
    list_filter = ("is_dynamic",)  # Filter for static or dynamic departments
    search_fields = ("name",)  # Add search functionality for department names


# Admin for ExpenseField
@admin.register(ExpenseField)
class ExpenseFieldAdmin(admin.ModelAdmin):
    list_display = ("id", "name",  "department")  # Show key fields in admin list view
    search_fields = ("name", "department__name")  # Allow search by expense field and department name
    list_filter = ("department",)  # Filters for expense head and department

    # Custom validation to handle dynamic department creation
    def save_model(self, request, obj, form, change):
        if obj.department.name.lower() == "other department":
            # Check for dynamic department creation
            new_department_name = form.cleaned_data.get("new_department_name")
            if new_department_name:
                department, created = Department.objects.get_or_create(
                    name=new_department_name, is_dynamic=True
                )
                obj.department = department
        super().save_model(request, obj, form, change)


# Admin for ExpenseType
@admin.register(ExpenseType)
class ExpenseTypeAdmin(admin.ModelAdmin):
    list_display = ('expense_name', 'get_department')  # Custom method for department
    search_fields = ('expense_name', 'expense_field__department__name')  # Search by related department name
    list_filter = ('expense_field__department',)  # Filter by department through related ExpenseField model

    def get_department(self, obj):
        return obj.expense_field.department.name if obj.expense_field else None
    get_department.admin_order_field = 'expense_field__department'  # Allows ordering by department
    get_department.short_description = 'Department'  # Display name in the admin interface


# Admin for Costing
@admin.register(Costing)
class CostingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_department',
        'get_expense_field',  # Use custom method to display expense field
        'month',
        'year',
        'get_cost',  # Use custom method to display cost
        'get_updated_by',  # Use custom method to display updated_by
        'updated_at'
    )

    # Custom method for department (if applicable)
    def get_department(self, obj):
        return obj.expense_type.expense_field.department.name
    get_department.admin_order_field = 'expense_type__expense_field__department'  # Allows ordering by department
    get_department.short_description = 'Department'

    # Custom method for expense_field (if related)
    def get_expense_field(self, obj):
        return obj.expense_type.expense_field.name
    get_expense_field.admin_order_field = 'expense_type__expense_field'  # Allows ordering by expense field
    get_expense_field.short_description = 'Expense Field'

    # Custom method for month (if applicable)
    def get_month(self, obj):
        return obj.month  # Assuming 'month' is a field on Costing
    get_month.admin_order_field = 'month'  # Allows ordering by month
    get_month.short_description = 'Month'

    # Custom method for cost (if applicable)
    def get_cost(self, obj):
        return obj.cost  # Assuming 'cost' is a field on Costing
    get_cost.admin_order_field = 'cost'  # Allows ordering by cost
    get_cost.short_description = 'Cost'

    # Custom method for updated_by (if it's a foreign key)
    def get_updated_by(self, obj):
        return obj.updated_by.username if obj.updated_by else "N/A"
    get_updated_by.admin_order_field = 'updated_by'  # Allows ordering by updated_by
    get_updated_by.short_description = 'Updated By'



# Admin for AuditTrail
@admin.register(AuditTrail)
class AuditTrailAdmin(admin.ModelAdmin):
    list_display = ("id", "costing", "change_type", "changed_by", "timestamp")
    search_fields = ("costing__expense_field__name", "change_type")
    list_filter = ("change_type", "timestamp")
