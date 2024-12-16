import calendar
from django import forms
from .models import Costing, Department, ExpenseField , ExpenseHead
from tig_costing.models import ExpenseHead, ExpenseField



# class CostingForm(forms.Form):
#     department = forms.ModelChoiceField(queryset=Department.objects.all(), label="Select Department")
#     expense_head = forms.ModelChoiceField(queryset=ExpenseHead.objects.all(), label="Select Expense Head")
#     expense_field = forms.ModelChoiceField(queryset=ExpenseField.objects.all(), label="Select Expense Field")
#     month = forms.ChoiceField(choices=[(m, m) for m in [
#         'January', 'February', 'March', 'April', 'May', 'June', 'July',
#         'August', 'September', 'October', 'November', 'December'
#     ]], label="Select Month")
#     year = forms.IntegerField(label="Enter Year")
#     cost = forms.DecimalField(max_digits=12, decimal_places=2, label="Enter Cost")

#     def __init__(self, *args, **kwargs):
#         department_id = kwargs.get('initial', {}).get('department_id')
#         if department_id:
#             kwargs['initial']['expense_field'] = ExpenseField.objects.filter(department_id=department_id)
#         super().__init__(*args, **kwargs)

# --------------------------testing using forms ---------------------




class CostingForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    expense_head = forms.ModelChoiceField(queryset=ExpenseHead.objects.none(), required=True)
    expense_field = forms.ModelChoiceField(queryset=ExpenseField.objects.none(), required=True)
    MONTH_CHOICES = [
    ('Jan', 'January'),
    ('Feb', 'February'),
    ('Mar', 'March'),
    ('Apr', 'April'),
    ('May', 'May'),
    ('Jun', 'June'),
    ('Jul', 'July'),
    ('Aug', 'August'),
    ('Sep', 'September'),
    ('Oct', 'October'),
    ('Nov', 'November'),
    ('Dec', 'December'),
]
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=True)
    year = forms.IntegerField()
    cost = forms.DecimalField(max_digits=12, decimal_places=2)

    def __init__(self, *args, **kwargs):
        department_id = kwargs.pop('department_id', None)
        super().__init__(*args, **kwargs)

        print(self.fields['month'])

        if department_id:
            # Filter expense heads by department
            self.fields['expense_head'].queryset = ExpenseHead.objects.filter(
                expensefield__department__id=department_id
            ).distinct()

            # Filter expense fields by department
            self.fields['expense_field'].queryset = ExpenseField.objects.filter(
                department__id=department_id
            )
