from tig_costing.models import Department, ExpenseHead, ExpenseField, Costing
from django.contrib.auth.models import User

# Fetch a user to associate with the costing records
user = User.objects.first()  # Replace with your logic to fetch or create a user

if not user:
    raise ValueError("No user exists in the database. Please create a user first.")

# Define costing data to populate
costing_data = [
    {"department": "Sales", "expense_head": "Business Development", "expense_field": "Sales Related Business Development", "month": "January", "year": 2025, "cost": 100.00},
    {"department": "Finance", "expense_head": "Bank Charges", "expense_field": "Finance Related Bank Charges", "month": "February", "year": 2025, "cost": 200.00},
    {"department": "IT", "expense_head": "Domain", "expense_field": "IT Related Domain", "month": "March", "year": 2025, "cost": 300.00},
    {"department": "Admin", "expense_head": "Electricity", "expense_field": "Admin Related Electricity", "month": "April", "year": 2025, "cost": 400.00},
    {"department": "HR", "expense_head": "Employee Engagement", "expense_field": "HR Related Employee Engagement", "month": "May", "year": 2025, "cost": 500.00},
    {"department": "Marketing", "expense_head": "Marketing", "expense_field": "Marketing Related Marketing", "month": "June", "year": 2025, "cost": 600.00},
]

# Populate costing data
for entry in costing_data:
    try:
        # Fetch required objects
        department = Department.objects.get(name=entry["department"])
        expense_head = ExpenseHead.objects.get(name=entry["expense_head"])
        expense_field = ExpenseField.objects.get(name=entry["expense_field"])

        # Create costing record
        costing = Costing.objects.create(
            department=department,
            expense_head=expense_head,
            expense_field=expense_field,
            month=entry["month"],
            year=entry["year"],
            cost=entry["cost"],
            updated_by=user,
        )
        print(f"Costing created: {costing}")
    except Department.DoesNotExist:
        print(f"Department '{entry['department']}' does not exist.")
    except ExpenseHead.DoesNotExist:
        print(f"Expense Head '{entry['expense_head']}' does not exist.")
    except ExpenseField.DoesNotExist:
        print(f"Expense Field '{entry['expense_field']}' does not exist.")
    except Exception as e:
        print(f"Error creating costing for {entry}: {e}")

print("Costing data population completed successfully.")
