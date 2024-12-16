from django.shortcuts import render
from django.shortcuts import render, redirect , get_object_or_404
from .models import ExpenseHead, ExpenseField, Costing, Department, AuditTrail
from .forms import CostingForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from tig_costing.models import ExpenseHead, ExpenseField
from .models import ExpenseField
from .models import ExpenseHead
from django.http import JsonResponse
from django.urls import reverse
from collections import defaultdict



def home(request):
    return render(request, 'tig_costing/home.html')



# def add_costing(request, id):
#     departments = Department.objects.all()
#     expense_heads = ExpenseHead.objects.all()
#     expense_fields = ExpenseField.objects.filter(department__id=id)
    
#     if request.method == "POST":
#         form = CostingForm(request.POST)
#         if form.is_valid():
#             # Process the form and save to DB
#             department = form.cleaned_data['department']
#             expense_head = form.cleaned_data['expense_head']
#             expense_field = form.cleaned_data['expense_field']
#             month = form.cleaned_data['month']
#             year = form.cleaned_data['year']
#             cost = form.cleaned_data['cost']

#             # Save the data to the Costing model
#             Costing.objects.create(
#                 department=department,
#                 expense_head=expense_head,
#                 expense_field=expense_field,
#                 month=month,
#                 year=year,
#                 cost=cost,
#                 updated_by=request.user
#             )
#             return redirect('costing_view')  # Redirect to your costing view
#     else:
#         form = CostingForm()

#     return render(request, 'tig_costing/add_costing.html', {
#         'form': form,
#         'departments': departments,
#         'expense_heads': expense_heads,
#         'expense_fields': expense_fields
#     })

#---------------testing through forms ------------------------

# @login_required
# def add_costing(request, expense_head_id=None):
#     departments = Department.objects.all()
    
#     expense_fields = []
#     expense_heads = []
    
#     if request.method == "POST":
#         form = CostingForm(request.POST)
#         if form.is_valid():
#             department = form.cleaned_data['department']
#             expense_head = form.cleaned_data['expense_head']
#             expense_field = form.cleaned_data['expense_field']
#             month = form.cleaned_data['month']
#             year = form.cleaned_data['year']
#             cost = form.cleaned_data['cost']

#             # Save to the Costing model
#             Costing.objects.create(
#                 department=department,
#                 expense_field=expense_field,
#                 expense_head=expense_head,
#                 month=month,
#                 year=year,
#                 cost=cost,
#                 updated_by=request.user
#             )
#             return redirect('view_costing', expense_head_id=expense_head.id)
#     else:
#         # For GET request, initialize an empty form with dynamic fields
#         department_id = request.GET.get('department')  # Get the department id from query parameters (optional)
#         form = CostingForm(department_id=department_id)

#         # Dynamically populate expense fields and heads based on department
#         if department_id:
#             expense_fields = ExpenseField.objects.filter(department__id=department_id)
#             expense_heads = ExpenseHead.objects.filter(expensefield__department__id=department_id).distinct()

#     return render(request, 'tig_costing/add_costing.html', {
#         'form': form,
#         'departments': departments,
#         'expense_heads': expense_heads,
#         'expense_fields': expense_fields
#     })


# AJAX view to load Expense Fields dynamically based on selected Expense Head
def load_expense_fields(request):
    expense_head_id = request.GET.get('expense_head')
    expense_fields = ExpenseField.objects.filter(expense_head__id=expense_head_id)
    data = {"expense_fields": [{"id": field.id, "name": field.name} for field in expense_fields]}
    print("load_expense_fields view was called")

    return JsonResponse(data)

def load_expense_heads(request):
    department_id = request.GET.get('department')
    if not department_id:
        return JsonResponse({"error": "Department ID not provided"}, status=400)

    try:
        expense_heads = ExpenseHead.objects.filter(expensefield__department__id=department_id).distinct()
    except Department.DoesNotExist:
        return JsonResponse({"error": "Invalid department ID"}, status=400)

    data = {"expense_heads": [{"id": head.id, "name": head.name} for head in expense_heads]}
    return JsonResponse(data)


#===================NEWONE===============================================

# @login_required
# def add_costing(request):
#     if request.method == "POST":
#         form = CostingForm(request.POST)
#         if form.is_valid():
#             # Extract data from the form
#             department = form.cleaned_data['department']
#             expense_head = form.cleaned_data['expense_head']
#             expense_field = form.cleaned_data['expense_field']
#             month = form.cleaned_data['month']
#             year = form.cleaned_data['year']
#             cost = form.cleaned_data['cost']

#             # Save to the Costing model
#             Costing.objects.create(
#                 department=department,
#                 expense_head=expense_head,
#                 expense_field=expense_field,
#                 month=month,
#                 year=year,
#                 cost=cost,
#                 updated_by=request.user
#             )
#             return redirect('view_costing', expense_head_id=expense_head.id)  # Redirect to the costing view

#     else:
#         # For GET request, initialize an empty form
#         department_id = request.GET.get('department')
#         expense_head_id = request.GET.get('expense_head')
#         form = CostingForm(department_id=department_id, expense_head_id=expense_head_id)

#     return render(request, 'tig_costing/add_costing.html', {'form': form})




@login_required
def add_costing(request, expense_head_id=None):
    departments = Department.objects.all()
    expense_heads = ExpenseHead.objects.all()  # Fetch all Expense Heads
    expense_fields = ExpenseField.objects.all()

    if request.method == "POST":
        
        form = CostingForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data['department']
            expense_head = form.cleaned_data['expense_head']
            expense_field = form.cleaned_data['expense_field']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            cost = form.cleaned_data['cost']

            # Save the data to the Costing model
            Costing.objects.create(
                department=department,
                expense_head=expense_head,
                expense_field=expense_field,
                month=month,
                year=year,
                cost=cost,
                updated_by=request.user
            )
            return redirect('view_costing', expense_head_id=expense_head.id)
    else:
        # For GET request, initialize an empty form with dynamic fields
        department_id = request.GET.get('department')  # Get the department id from query parameters (optional)
        form = CostingForm(department_id=department_id)

        # Dynamically populate expense fields and heads based on department
        if department_id:
            expense_fields = ExpenseField.objects.filter(department__id=department_id)
            expense_heads = ExpenseHead.objects.filter(expensefield__department__id=department_id).distinct()

        # Debugging: Check if expense_fields and expense_heads are being correctly populated
        # print("Expense Heads:", expense_heads)
        # print("Expense Fields:", expense_fields)
        

    return render(request, 'tig_costing/add_costing.html', {
        'form': form,
        'departments': departments,
        'expense_heads': expense_heads,
        'expense_fields': expense_fields
    })



# def view_costing(request, expense_head_id):
#     try:
#         expense_head = ExpenseHead.objects.get(id=expense_head_id)
#     except ExpenseHead.DoesNotExist:
#         return render(request, 'tig_costing/error.html', {'message': 'Expense Head not found'})

#     costings = Costing.objects.filter(expense_head=expense_head)

#     return render(request, 'tig_costing/view_costing.html', {
#         'expense_head': expense_head,
#         'costings': costings,
#     })

#=============== FOR KEY VALUE PAIR ====================

from collections import defaultdict

from collections import defaultdict
from django.shortcuts import render
from .models import ExpenseHead, Department, ExpenseField, Costing
from django.contrib.auth.decorators import login_required

@login_required
def view_costing(request, expense_head_id):
    try:
        # Try to fetch the expense head using the passed ID
        expense_head = ExpenseHead.objects.get(id=expense_head_id)
    except ExpenseHead.DoesNotExist:
        # If the expense head does not exist, return an error page
        return render(request, 'tig_costing/error.html', {'message': 'Expense Head not found'})

    # Fetch all costings related to the expense head
    costings = Costing.objects.filter(expense_head=expense_head)

    # Initialize expenses dictionary to store monthly and total costs per department
    expenses = defaultdict(
        lambda: {
            "Departments": defaultdict(
                lambda: {
                    "Jan'25": 0, "Feb'25": 0, "Mar'25": 0, "Apr'25": 0,
                    "May'25": 0, "Jun'25": 0, "Jul'25": 0, "Aug'25": 0,
                    "Sept'25": 0, "Oct'25": 0, "Nov'25": 0, "Dec'25": 0,
                    "Total": 0
                }
            )
        }
    )

    # Populate the expenses dictionary with cost data
    for costing in costings:
        month_key = costing.month[:3] + "'25"  # Get the short version of the month with year suffix
        department = costing.department.name    # Get the department name
        expenses[costing.expense_head.name]["Departments"][department][month_key] += float(costing.cost)
        expenses[costing.expense_head.name]["Departments"][department]["Total"] += float(costing.cost)

    # Fetch all departments and expense fields related to the expense head
    departments = Department.objects.all()
    expense_fields = ExpenseField.objects.filter(expense_head=expense_head)

    print("Expenses:", dict(expenses))
    # Prepare context to be passed to the template
    context = {
        'expense_head': expense_head,            # Expense head for which we are displaying costing details
        'expenses': dict(expenses),               # Converted expenses defaultdict to regular dictionary for JSON-safe structure
        'departments': departments,               # List of all departments (for dropdowns or selection)
        'expense_fields': expense_fields,         # List of expense fields (for dropdowns or selection)
    }

    print(context)
    # Return the rendered view with the context
    return render(request, 'tig_costing/view_costing.html', context)












@user_passes_test(lambda user: user.is_superuser)
def create_dynamic_field(request):
    """Allow superusers to dynamically create departments or expense fields."""
    if request.method == "POST":
        department_name = request.POST.get("department_name")
        expense_field_name = request.POST.get("expense_field_name")
        expense_head_id = request.POST.get("expense_head_id")

        # Create department if provided
        if department_name:
            department, _ = Department.objects.get_or_create(name=department_name, is_dynamic=True)

        # Create expense field if provided
        if expense_field_name and expense_head_id:
            expense_head = get_object_or_404(ExpenseHead, id=expense_head_id)
            department = get_object_or_404(Department, name=department_name)
            ExpenseField.objects.create(
                name=expense_field_name,
                expense_head=expense_head,
                department=department,
            )
        return JsonResponse({"status": "success"})

    return JsonResponse({"error": "Invalid request"}, status=400)

def test_view(request):
    # Fetch all expense heads and their related fields and departments
    data = []
    expense_heads = ExpenseHead.objects.prefetch_related('fields')

    for expense_head in expense_heads:
        for field in expense_head.fields.all():
            data.append({
                'expense_head': expense_head.name,
                'department': field.department.name,
                'field_name': field.name,
                'months': [0] * 12,  # Placeholder for monthly costing (Jan to Dec)
                'total': 0,         # Placeholder for total
            })
            print(data)

    # Pass the data to the template
    return render(request, 'tig_costing/test.html', {'expense_data': data})


