import calendar
from django import forms
from .models import Costing, Department, ExpenseField , ExpenseHead
from tig_costing.models import ExpenseHead, ExpenseField






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



