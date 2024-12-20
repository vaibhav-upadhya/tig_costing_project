from tig_costing.models import Department, ExpenseHead, ExpenseField, ExpenseType, Costing
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime

# 1. Populate departments
finance = Department.objects.get_or_create(name="Finance", is_dynamic=False)[0]
sales = Department.objects.get_or_create(name="Sales", is_dynamic=False)[0]
it = Department.objects.get_or_create(name="IT", is_dynamic=False)[0]
admin = Department.objects.get_or_create(name="Admin", is_dynamic=False)[0]
hr = Department.objects.get_or_create(name="HR", is_dynamic=False)[0]
marketing = Department.objects.get_or_create(name="Marketing", is_dynamic=False)[0]

# 2. Populate expense heads and expense fields
bank_charges = ExpenseHead.objects.get_or_create(name="Bank Charges", description="Expenses for bank charges")[0]
finance_bank_charges = ExpenseField.objects.get_or_create(
    name="Finance Related Bank Charges", department=finance, expense_head=bank_charges
)[0]

business_development = ExpenseHead.objects.get_or_create(name="Business Development", description="Expenses for business growth")[0]
sales_business_dev = ExpenseField.objects.get_or_create(
    name="Sales Related Business Development", department=sales, expense_head=business_development
)[0]

employee_engagement = ExpenseHead.objects.get_or_create(name="Employee Engagement", description="Employee engagement expenses")[0]
hr_employee_engagement = ExpenseField.objects.get_or_create(
    name="HR Related Employee Engagement", department=hr, expense_head=employee_engagement
)[0]

domain = ExpenseHead.objects.get_or_create(name="Domain", description="Domain-related expenses")[0]
it_domain = ExpenseField.objects.get_or_create(
    name="IT Related Domain", department=it, expense_head=domain
)[0]

electricity = ExpenseHead.objects.get_or_create(name="Electricity", description="Electricity expenses")[0]
admin_electricity = ExpenseField.objects.get_or_create(
    name="Admin Related Electricity", department=admin, expense_head=electricity
)[0]


# Populate Expense Types
ExpenseType.objects.get_or_create(
    expense_field=finance_bank_charges,
    expense_name="Bank Charges"
)

ExpenseType.objects.get_or_create(
    expense_field=sales_business_dev,
    expense_name="Business Development"
)

ExpenseType.objects.get_or_create(
    expense_field=hr_employee_engagement,
    expense_name="Employee Engagement"
)

ExpenseType.objects.get_or_create(
    expense_field=it_domain,
    expense_name="Domain"
)

ExpenseType.objects.get_or_create(
    expense_field=admin_electricity,
    expense_name="Electricity"
)

# Populate test Costing entries for various months and years
user = User.objects.get_or_create(username="admin", is_staff=True, is_superuser=True, password="adminpassword")[0]

# Example: Costing for Finance Bank Charges
Costing.objects.get_or_create(
    expense_type=ExpenseType.objects.get(expense_name="Bank Charges"),
    month="January",
    year=2024,
    cost=Decimal("1500.00"),
    updated_by=user
)

# Example: Costing for Sales Business Development
Costing.objects.get_or_create(
    expense_type=ExpenseType.objects.get(expense_name="Business Development"),
    month="February",
    year=2024,
    cost=Decimal("2000.00"),
    updated_by=user
)

# Example: Costing for HR Employee Engagement
Costing.objects.get_or_create(
    expense_type=ExpenseType.objects.get(expense_name="Employee Engagement"),
    month="March",
    year=2024,
    cost=Decimal("1200.00"),
    updated_by=user
)

# Example: Costing for IT Domain
Costing.objects.get_or_create(
    expense_type=ExpenseType.objects.get(expense_name="Domain"),
    month="April",
    year=2024,
    cost=Decimal("1800.00"),
    updated_by=user
)

# Example: Costing for Admin Electricity
Costing.objects.get_or_create(
    expense_type=ExpenseType.objects.get(expense_name="Electricity"),
    month="May",
    year=2024,
    cost=Decimal("800.00"),
    updated_by=user
)

print("Data population completed successfully, including Costing records.")


from tig_costing.models import AuditTrail

# Example: When a Costing record is updated, log the changes in AuditTrail
costing_instance = Costing.objects.get(id=some_costing_id)  # Get the instance you're updating
old_data = str(costing_instance)  # Convert the old data to a string (or JSON if needed)
new_data = "Updated Cost"  # New data (or the new instance data)

AuditTrail.objects.create(
    costing=costing_instance,
    change_type="Update",
    old_data=old_data,
    new_data=new_data,
    changed_by=user
)







