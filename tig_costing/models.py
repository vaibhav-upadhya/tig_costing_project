from calendar import month
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.forms import JSONField

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    is_dynamic = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class ExpenseHead(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class ExpenseField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    expense_head = models.ForeignKey(ExpenseHead, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class ExpenseType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense_field = models.ForeignKey(ExpenseField, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.expense_name} - {self.expense_field}"

# Signal to auto-create costing records for 12 months when a new ExpenseType is created
@receiver(post_save, sender=ExpenseType)
def create_costing_for_expense_type(sender, instance, created, **kwargs):
    """
    Signal to create costing records for all months when a new ExpenseType is created.
    """
    if created:
        user = User.objects.filter(is_superuser=True).first()  # Assign a default superuser
        if not user:
            raise Exception("Ensure at least one superuser exists for assigning updated_by.")

        months = [
            "Jan", "Feb", "Mar", "Apr", "May",
            "Jun", "Jul", "Aug", "Sept",
            "Oct", "Nov", "Dec"
        ]
        year = datetime.now().year

        for month in months:
            Costing.objects.create(
                expense_type=instance,
                month=month,
                year=year,
                cost=0.00,  # Initial cost set to 0
                updated_by=user
            )
    
    


# ================================================================WORKING==========================================================================
class Costing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    month = models.CharField(max_length=20)  # Store month names like "Jan'25"
    expense_type = models.ForeignKey('ExpenseType', on_delete=models.CASCADE)  # Ensure ExpenseType model exists
    year = models.IntegerField()  # Stores the year
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Ensure User model exists
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.expense_type} - {self.month} - {self.year} - {self.cost}"



class AuditTrail(models.Model):
    CHANGE_TYPES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    )

    costing = models.ForeignKey(Costing, on_delete=models.CASCADE, related_name="audit_trails")
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField(null=True, blank=True)  # Optional: Details of changes

    def __str__(self):
        return f"{self.change_type} on {self.costing} by {self.changed_by}"
