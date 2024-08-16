# Generated by Django 5.1 on 2024-08-16 14:34

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_userexpensegroup'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('reason', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('split_type', models.CharField(choices=[('EQUAL', 'Equal'), ('EXACT', 'Exact'), ('PERCENT', 'Percent')], max_length=10)),
                ('shares', models.JSONField(default=dict)),
                ('expense_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='dashboard.expensegroup')),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses_paid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
