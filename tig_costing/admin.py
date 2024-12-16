from django.contrib import admin
from .models import ExpenseHead, Department, ExpenseField, Costing, AuditTrail

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


# Admin for Costing
@admin.register(Costing)
class CostingAdmin(admin.ModelAdmin):
    list_display = ("id", 'department', 'expense_field', 'month', 'year', 'cost', 'updated_by', 'updated_at')
    list_filter = ('expense_field', 'department')
    search_fields = ("expense_field__name", "expense_field__department__name")


# Admin for AuditTrail
@admin.register(AuditTrail)
class AuditTrailAdmin(admin.ModelAdmin):
    list_display = ("id", "costing", "change_type", "changed_by", "timestamp")
    search_fields = ("costing__expense_field__name", "change_type")
    list_filter = ("change_type", "timestamp")



