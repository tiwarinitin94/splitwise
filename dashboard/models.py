from django.db import models


from django.contrib.auth.models import User

from userdetails.models import BaseModel



class ExpenseGroup(BaseModel):
    created_by=  models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_expense_user')
    name=  models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name


class UserExpenseGroup(BaseModel):
    expense_group= models.ForeignKey(ExpenseGroup, on_delete=models.CASCADE, related_name='group_expense_user_group')
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_expense_user_user')
    
    def __str__(self) -> str:
        return self.expense_group.name+" /"+self.user.username


from django.conf import settings
from django.utils import timezone


class Expense(models.Model):
    SPLIT_TYPE_CHOICES = [
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENT', 'Percent')
    ]

    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses_paid'
    )
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses_added'
    )
    paid_for = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses_owed'
    )
    expense_group = models.ForeignKey(
        'ExpenseGroup',
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    split_type = models.CharField(max_length=10, choices=SPLIT_TYPE_CHOICES)
    shares = models.JSONField(default=dict)  # For storing percentages or exact amounts

    
    

   

    def __str__(self):
        return f"{self.paid_by} paid {self.amount} for {self.reason} in group {self.expense_group}"