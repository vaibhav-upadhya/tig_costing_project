from tig_costing.models import Department, ExpenseHead, ExpenseField, Costing
from django.contrib.auth.models import User
from decimal import Decimal

# 1. Populate departments
finance = Department.objects.get_or_create(name="Finance", is_dynamic=False)[0]
sales = Department.objects.get_or_create(name="Sales", is_dynamic=False)[0]
it = Department.objects.get_or_create(name="IT", is_dynamic=False)[0]
admin = Department.objects.get_or_create(name="Admin", is_dynamic=False)[0]
hr = Department.objects.get_or_create(name="HR", is_dynamic=False)[0]
marketing = Department.objects.get_or_create(name="Marketing", is_dynamic=False)[0]

# 2. Populate expense heads and expense fields
bank_charges = ExpenseHead.objects.get_or_create(name="Bank Charges", description="Expenses for bank charges")[0]
ExpenseField.objects.get_or_create(name="Finance Related Bank Charges", department=finance, expense_head=bank_charges)

business_development = ExpenseHead.objects.get_or_create(name="Business Development", description="Expenses for business growth")[0]
ExpenseField.objects.get_or_create(name="Sales Related Business Development", department=sales, expense_head=business_development)

consulting_accounting = ExpenseHead.objects.get_or_create(name="Consulting & Accounting", description="Consulting and accounting expenses")[0]
ExpenseField.objects.get_or_create(name="Finance Related Consulting & Accounting", department=finance, expense_head=consulting_accounting)

credit_funding = ExpenseHead.objects.get_or_create(name="Credit Funding", description="Credit funding expenses")[0]
ExpenseField.objects.get_or_create(name="Finance Related Credit Funding Cost", department=finance, expense_head=credit_funding)

domain = ExpenseHead.objects.get_or_create(name="Domain", description="Domain-related expenses")[0]
ExpenseField.objects.get_or_create(name="IT Related Domain", department=it, expense_head=domain)

email_website = ExpenseHead.objects.get_or_create(name="Email & Website", description="Email and website expenses")[0]
ExpenseField.objects.get_or_create(name="IT Email & Website", department=it, expense_head=email_website)

electricity = ExpenseHead.objects.get_or_create(name="Electricity", description="Electricity expenses")[0]
ExpenseField.objects.get_or_create(name="Admin Related Electricity", department=admin, expense_head=electricity)

employee_engagement = ExpenseHead.objects.get_or_create(name="Employee Engagement", description="Employee engagement expenses")[0]
ExpenseField.objects.get_or_create(name="HR Related Employee Engagement", department=hr, expense_head=employee_engagement)

employee_insurance = ExpenseHead.objects.get_or_create(name="Employee Insurance", description="Employee insurance expenses")[0]
ExpenseField.objects.get_or_create(name="HR Related Employee Insurance", department=hr, expense_head=employee_insurance)

freight_courier = ExpenseHead.objects.get_or_create(name="Freight & Courier", description="Freight and courier expenses")[0]
ExpenseField.objects.get_or_create(name="Admin Related Flight & Courier", department=admin, expense_head=freight_courier)

insurance = ExpenseHead.objects.get_or_create(name="Insurance", description="Insurance expenses")[0]
ExpenseField.objects.get_or_create(name="Admin Related Insurance", department=admin, expense_head=insurance)

legal_professional_exps = ExpenseHead.objects.get_or_create(name="Legal & Professional Exps", description="Legal and professional expenses")[0]
ExpenseField.objects.get_or_create(name="Finance Related Legal & Professional Exps", department=finance, expense_head=legal_professional_exps)

marketing_expenses = ExpenseHead.objects.get_or_create(name="Marketing", description="Marketing expenses")[0]
ExpenseField.objects.get_or_create(name="Marketing Related Marketing", department=marketing, expense_head=marketing_expenses)

recruitment = ExpenseHead.objects.get_or_create(name="Recruitment Expenses", description="Recruitment-related expenses")[0]
ExpenseField.objects.get_or_create(name="HR Related Recruitment Expenses", department=hr, expense_head=recruitment)

rent = ExpenseHead.objects.get_or_create(name="Rent", description="Rent expenses")[0]
ExpenseField.objects.get_or_create(name="Admin Related Rent", department=admin, expense_head=rent)

repairs_maintenance = ExpenseHead.objects.get_or_create(name="Repairs and Maintenance", description="Repairs and maintenance expenses")[0]
ExpenseField.objects.get_or_create(name="Admin Related Repairs and Maintenance", department=admin, expense_head=repairs_maintenance)

salary_wages = ExpenseHead.objects.get_or_create(name="Salary & Wages", description="Salary and wages expenses")[0]
ExpenseField.objects.get_or_create(name="HR Related Salary & Wages", department=hr, expense_head=salary_wages)

it_subscription = ExpenseHead.objects.get_or_create(name="IT Subscription", description="IT subscription expenses")[0]
ExpenseField.objects.get_or_create(name="IT Related Subscription", department=it, expense_head=it_subscription)

finance_subscription = ExpenseHead.objects.get_or_create(name="Finance Subscription", description="Finance subscription expenses")[0]
ExpenseField.objects.get_or_create(name="Finance Related Subscription", department=finance, expense_head=finance_subscription)

# 3. Add test Costing data
# Ensure a user exists to associate with the Costing entry
user = User.objects.get_or_create(username="admin", is_staff=True, is_superuser=True, password="adminpassword")[0]

# Add test Costing entries
Costing.objects.get_or_create(
    department=finance,
    expense_field=ExpenseField.objects.get(name="Finance Related Bank Charges"),
    expense_head=bank_charges,
    month="January",
    year=2024,
    cost=Decimal("1500.00"),
    updated_by=user
)

Costing.objects.get_or_create(
    department=sales,
    expense_field=ExpenseField.objects.get(name="Sales Related Business Development"),
    expense_head=business_development,
    month="February",
    year=2024,
    cost=Decimal("2000.00"),
    updated_by=user
)

Costing.objects.get_or_create(
    department=hr,
    expense_field=ExpenseField.objects.get(name="HR Related Employee Engagement"),
    expense_head=employee_engagement,
    month="March",
    year=2024,
    cost=Decimal("1200.00"),
    updated_by=user
)

Costing.objects.get_or_create(
    department=it,
    expense_field=ExpenseField.objects.get(name="IT Related Domain"),
    expense_head=domain,
    month="April",
    year=2024,
    cost=Decimal("1800.00"),
    updated_by=user
)

Costing.objects.get_or_create(
    department=admin,
    expense_field=ExpenseField.objects.get(name="Admin Related Electricity"),
    expense_head=electricity,
    month="May",
    year=2024,
    cost=Decimal("800.00"),
    updated_by=user
)

print("Data population completed successfully, including Costing records.")
