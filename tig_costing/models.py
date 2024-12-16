from django.db import models
from django.db import models
from django.contrib.auth.models import User



class Department(models.Model):
    name = models.CharField(max_length=100)
    is_dynamic = models.BooleanField(default=False)
    print("test")

    def __str__(self):
        return f"{self.id} {self.name}"

class ExpenseHead(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} {self.name}"

class ExpenseField(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    expense_head = models.ForeignKey(ExpenseHead, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.name}"

class Costing(models.Model):
    department = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="costings",
          
    )
    expense_head = models.ForeignKey(ExpenseHead, on_delete=models.CASCADE)
    expense_field = models.ForeignKey(ExpenseField, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Ensure this field exists
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.department} - {self.expense_field} - {self.cost} - {self.id}"





# Audit Trail Model
class AuditTrail(models.Model):
    costing = models.ForeignKey(Costing, on_delete=models.CASCADE, related_name="audit_trail")
    change_type = models.CharField(max_length=50)  # E.g., 'Create', 'Update', 'Delete'
    old_data = models.TextField()  # Store old values
    new_data = models.TextField()  # Store new values
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Who made the change
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit for {self.costing.expense_field.name} on {self.timestamp}"

