from django.contrib import admin
from .models import *

class UserExpenseGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'expense_group', 'user')
    list_filter = ('expense_group', 'user')
    search_fields = ('user__username', 'expense_group__name')

class ExpenseGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'name')
    list_filter = ('created_by',)
    search_fields = ('name', 'created_by__username')

admin.site.register(UserExpenseGroup, UserExpenseGroupAdmin)
admin.site.register(ExpenseGroup, ExpenseGroupAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'paid_by','paid_for','added_by', 'expense_group', 'amount', 'reason', 'date', 'split_type')
    list_filter = ('split_type', 'date', 'expense_group')
    search_fields = ('reason', 'paid_by__username', 'expense_group__name')
    readonly_fields = ('date',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Optionally, filter based on user permissions or other logic
        return qs

admin.site.register(Expense, ExpenseAdmin)