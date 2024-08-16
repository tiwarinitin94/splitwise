from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import generics
from django.db.models import Sum
from rest_framework import status
import math

class ExpenseGroupCreateAPIView(generics.CreateAPIView):
    queryset = ExpenseGroup.objects.all()
    serializer_class = ExpenseGroupSerializer
    permission_classes = [IsAuthenticated]
    
class ListOfExpenseGroup(generics.ListAPIView):
    queryset = ExpenseGroup.objects.all()
    serializer_class = ExpenseGroupSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this API

    def get_queryset(self):
        # Filter queryset to include only those created by the authenticated user
        user = self.request.user
        return ExpenseGroup.objects.filter(created_by=user)

class UserExpenseGroupCreateView(generics.CreateAPIView):
    queryset = UserExpenseGroup.objects.all()
    serializer_class = UserExpenseGroupSerializer
    permission_classes = [IsAuthenticated]

class ExpenseGroupDetailAPIView(generics.RetrieveAPIView):
    queryset = ExpenseGroup.objects.all()
    serializer_class = ExpenseGroupDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the expense group ID from the URL parameters
        expense_group_id = self.kwargs.get('pk')
        # Return the specific expense group object
        return ExpenseGroup.objects.get(id=expense_group_id)


class ExpenseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        paid_by = request.user
        expense_group_id = data.get('expense_group')
        amount = data.get('amount')
        reason = data.get('reason')
        split_type = data.get('split_type')
        shares = data.get('shares')  # Expected to be a dictionary {user_id: share_value}

        try:
            expense_group = ExpenseGroup.objects.get(id=expense_group_id)
        except ExpenseGroup.DoesNotExist:
            return Response({'error': 'ExpenseGroup not found'}, status=status.HTTP_404_NOT_FOUND)

        if split_type == 'PERCENT':
            total_percentage = sum(shares.values())
            if not math.isclose(total_percentage, 100.0, abs_tol=0.01):
                return Response({'error': 'Total percentage must be exactly 100.'}, status=status.HTTP_400_BAD_REQUEST)

            for user_id, percentage in shares.items():
                if user_id == str(paid_by.id):  # Skip the record if user_id is the same as paid_by
                    continue
                share_amount = round((percentage / 100) * float(amount), 2)
                
                print(user_id,share_amount)
                Expense.objects.create(
                    paid_by=paid_by,
                    paid_for_id=user_id,
                    added_by=request.user,
                    expense_group=expense_group,
                    amount=share_amount,
                    reason=reason,
                    split_type=split_type
                )
                
        elif split_type == 'EXACT':
            total_amount = sum(shares.values())
            if not math.isclose(total_amount, float(amount), abs_tol=0.01):
                return Response({'error': 'Total exact shares must equal the total amount.'}, status=status.HTTP_400_BAD_REQUEST)

            for user_id, exact_amount in shares.items():
                if user_id == str(paid_by.id):  # Skip the record if user_id is the same as paid_by
                    continue
                Expense.objects.create(
                    paid_by=paid_by,
                    added_by=request.user,
                    paid_for_id=user_id,
                    expense_group=expense_group,
                    amount=exact_amount,
                    reason=reason,
                    split_type=split_type
                )
                
        elif split_type == 'EQUAL':
            # Get all members of the expense group
            members = UserExpenseGroup.objects.filter(expense_group=expense_group)
            total_members = members.count()
            print(total_members)
            for member in members:
                if member.id!=paid_by.id:
                    # Exclude the user who paid
                    equal_share = amount / total_members
                    Expense.objects.create(
                        paid_by=paid_by,
                        paid_for_id=member.id,
                        added_by=request.user,
                        expense_group=expense_group,
                        amount=equal_share,
                        reason=reason,
                        split_type=split_type,
                    )

        return Response({'success': 'Expense created successfully'}, status=status.HTTP_201_CREATED)
    

# class ExpenseCreateAPIView(generics.CreateAPIView):
#     serializer_class = ExpenseSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(paid_by_id=self.request.user)


class OwesToUserInGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        logged_in_user = request.user
        expenses = Expense.objects.filter(
            paid_by=logged_in_user,
            expense_group_id=group_id
        ).exclude(paid_for=logged_in_user)

        total_owed = {}
        for expense in expenses:
            if expense.paid_for.id not in total_owed:
                total_owed[expense.paid_for.id] = 0
            total_owed[expense.paid_for.id] += float(expense.amount)

        result = [
            {
                "user": {
                    "id": uid,
                    "username": User.objects.get(id=uid).username
                },
                "amount": round(amount, 2)
            }
            for uid, amount in total_owed.items()
            if amount > 0
        ]

        if not result:
            return Response({"detail": "No one owes you in this group."}, status=status.HTTP_204_NO_CONTENT)

        return Response(result)

class OwesByUserInGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        logged_in_user = request.user
        expenses = Expense.objects.filter(
            paid_for=logged_in_user,
            expense_group_id=group_id
        ).exclude(paid_by=logged_in_user)

        total_owed = {}
        for expense in expenses:
            if expense.paid_by.id not in total_owed:
                total_owed[expense.paid_by.id] = 0
            total_owed[expense.paid_by.id] += float(expense.amount)

        result = [
            {
                "user": {
                    "id": uid,
                    "username": User.objects.get(id=uid).username
                },
                "amount": round(amount, 2)
            }
            for uid, amount in total_owed.items()
            if amount > 0
        ]

        if not result:
            return Response({"detail": "You don't owe anyone in this group."}, status=status.HTTP_204_NO_CONTENT)

        return Response(result)
