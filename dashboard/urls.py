from django.urls import path
from dashboard.views import *





urlpatterns = [
    path('expense-group', ListOfExpenseGroup.as_view(), name='expensegroups'),      
    path('expense-group/create/', ExpenseGroupCreateAPIView.as_view(), name='expense-group-create'),
    path('expense-group/<int:pk>/', ExpenseGroupDetailAPIView.as_view(), name='api-expense-group-detail'),
    path('user-expense-group/create/', UserExpenseGroupCreateView.as_view(), name='api-user-expense-group-create'),
    path('expenses/', ExpenseCreateAPIView.as_view(), name='api-expense-create'),
    path('owes-to-user/<int:group_id>/', OwesToUserInGroupAPIView.as_view(), name='owes-to-user'),
    path('owes-by-user/<int:group_id>/', OwesByUserInGroupAPIView.as_view(), name='owes-by-user'),
]
