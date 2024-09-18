from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'user', 'transaction_type', 'amount', 'date']
        read_only_fields = ['user', 'date']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The transaction amount must be greater than zero")
        return value
    
    def validate(self, data):
        account = data['account']
        transaction_type = data['transaction_type']
        amount = data['amount']

        if transaction_type == 'withdrawal' and account.balance < amount:
            raise serializers.ValidationError("Insufficient funds in the account for this withdrawal.")
        
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)