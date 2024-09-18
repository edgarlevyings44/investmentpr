from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Transaction, InvestmentAccount, UserInvestmentAccount
from .serializers import TransactionSerializer
from .permissions import IsViewOnly, IsFullCRUD, IsPostOnly
from rest_framework.permissions import IsAdminUser
from django.utils.dateparse import parse_date


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated] 

    def get_permissions(self):
        """
        Dynamically assign permissions based on the user role in the investment account.
        """
        account_id = self.kwargs.get('account_id')


        if account_id:

            try:
                user_role = UserInvestmentAccount.objects.get(user=self.request.user, account_id=account_id).role
                if user_role == 'view':
                    return [IsViewOnly()]
                elif user_role == 'crud':
                    return [IsFullCRUD()]
                elif user_role == 'post':
                    return [IsPostOnly()]
            except UserInvestmentAccount.DoesNotExist:
                return [IsAuthenticated()] 
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Filter transactions by the investment account.
        """
        account_id = self.kwargs.get('account_id')

        if self.request.user.is_staff:
            return Transaction.objects.filter(account_id=account_id)
        
        return Transaction.objects.filter(account_id=account_id, user=self.request.user)

def perform_create(self, serializer):
        """
        Ensure that the user making the transaction is automatically set.
        """
        serializer.save(user=self.request.user)
        
class AdminUserTransactionsView(APIView):
    """
    Admin-only view that returns all transactions of a user,
    along with the total balance across all accounts.
    Supports date range filtering.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        transactions = Transaction.objects.filter(user__id=user_id)

        if start_date:
            transactions = transactions.filter(date__gte=parse_date(start_date))
        if end_date:
            transactions = transactions.filter(date__lte=parse_date(end_date))

        transaction_data = []
        total_balance = 0

        for transaction in transactions:
            transaction_data.append({
                'id': transaction.id,
                'account': transaction.account.name,
                'transaction_type': transaction.transaction_type,
                'amount': transaction.amount,
                'date': transaction.date,
            })

            if transaction.transaction_type == 'deposit':
                total_balance += transaction.amount
            elif transaction.transaction_type == 'withdrawal':
                total_balance -= transaction.amount

        response_data = {
            'user_id': user_id,
            'total_balance': total_balance,
            'transactions': transaction_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)