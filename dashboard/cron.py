from django.core.mail import send_mail
from django.conf import settings
from .models import Expense
from django.contrib.auth.models import User


def send_weekly_summary_email():
    users = User.objects.all()

    for user in users:
        expenses_owed_by_user = Expense.objects.filter(paid_by=user)
        if expenses_owed_by_user.exists():
            message = "You owe the following amounts:\n\n"
            for expense in expenses_owed_by_user:
                message += f"To {expense.paid_for.username}: {expense.amount} for {expense.reason} in group {expense.expense_group.name}\n"

            send_mail(
                'Weekly Expense Summary',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
