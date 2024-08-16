
from rest_framework import serializers
from .models import *


# serializers.py
from rest_framework import serializers
from .models import User, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class OwesToUserSerializer(serializers.Serializer):
    user = UserSerializer()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class OwesByUserSerializer(serializers.Serializer):
    user = UserSerializer()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    
class UserExpenseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExpenseGroup
        fields = ['id','expense_group', 'user']
        
        
class ExpenseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseGroup
        fields = ['id','created_by', 'name']
        
class ExpenseGroupDetailSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseGroup
        fields = ['id', 'created_by', 'name', 'member_count']

    def get_member_count(self, obj):
        # Count the number of UserExpenseGroup entries for this expense group
        return UserExpenseGroup.objects.filter(expense_group=obj).count()
    

from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'paid_by', 'expense_group', 'amount', 'reason', 'date', 'split_type', 'shares']

    def validate(self, data):
        if data['split_type'] == 'PERCENT':
            total_percentage = sum(data['shares'].values())
            if not math.isclose(total_percentage, 100.0, abs_tol=0.01):
                raise serializers.ValidationError("Total percentage must be exactly 100.")
        elif data['split_type'] == 'EXACT':
            total_amount = sum(data['shares'].values())
            if not math.isclose(total_amount, data['amount'], abs_tol=0.01):
                raise serializers.ValidationError("Total exact shares must equal the total amount.")
        return data