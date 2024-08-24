from django.db import models


from django.contrib.auth.models import User

from userdetails.models import BaseModel
from django.core.mail import send_mail


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

    def _send_expense_email(self):
        subject = f'New Expense Added: {self.reason}'
        message = f'You have been added to an expense.\n\nDetails:\nAmount: {self.amount}\nReason: {self.reason}\nDate: {self.date.strftime("%Y-%m-%d %H:%M:%S")}\n\nYou owe: {self.amount}'

        # Get participants excluding the one who paid
        participants = Expense.objects.filter(expense_group=self.expense_group).exclude(paid_by=self.paid_by)
        
        for participant in participants:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [participant.paid_for.email],
                fail_silently=False,
            )