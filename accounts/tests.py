from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import InvestmentAccount, Transaction, UserInvestmentAccount
from django.utils import timezone
from datetime import timedelta

class InvestmentAccountTestCase(APITestCase):
    def setUp(self):

        self.user_view_only = User.objects.create_user(username='view_user', password='password')
        self.user_full_crud = User.objects.create_user(username='crud_user', password='password')
        self.user_post_only = User.objects.create_user(username='post_user', password='password')
        self.admin_user = User.objects.create_superuser(username='admin', password='password')

        self.account1 = InvestmentAccount.objects.create(name='Account 1', balance=100.00)
        self.account2 = InvestmentAccount.objects.create(name='Account 2', balance=200.00)
        self.account3 = InvestmentAccount.objects.create(name='Account 3', balance=300.00)

        UserInvestmentAccount.objects.create(user=self.user_view_only, account=self.account1, role='view')
        UserInvestmentAccount.objects.create(user=self.user_full_crud, account=self.account2, role='crud')
        UserInvestmentAccount.objects.create(user=self.user_post_only, account=self.account3, role='post')

        self.client.force_authenticate(user=self.user_full_crud)

    def test_view_only_user_cannot_create_transaction(self):
        self.client.force_authenticate(user=self.user_view_only)
        url = reverse('transaction-list', kwargs={'account_id': self.account1.id})
        data = {
            'transaction_type': 'deposit', 
            'amount': 50.00
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_crud_user_can_create_transaction(self):
        self.client.force_authenticate(user=self.user_full_crud)
        url = reverse('transaction-list', kwargs={'account_id': self.account2.id})
        data = {
            'transaction_type': 'deposit', 
            'amount': 100.00,
            'account': self.account2.id
        }
        response = self.client.post(url, data, format='json')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.account2.refresh_from_db()
        self.assertEqual(self.account2.balance, 300.00)

    def test_post_only_user_can_post_but_not_view_transactions(self):
        self.client.force_authenticate(user=self.user_post_only)
        url = reverse('transaction-list', kwargs={'account_id': self.account3.id})
        data = {
            'transaction_type': 'deposit', 
            'amount': 50.00,
            'account': self.account3.id
        }

        post_response = self.client.post(url, data, format='json')

        print(post_response.data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_transactions_with_date_filter(self):
        Transaction.objects.create(account=self.account1, user=self.user_view_only, transaction_type='deposit', amount=50.00, date=timezone.now() - timedelta(days=3))
        Transaction.objects.create(account=self.account2, user=self.user_full_crud, transaction_type='withdrawal', amount=20.00, date=timezone.now() - timedelta(days=1))

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-user-transactions', kwargs={'user_id': self.user_view_only.id})

        start_date = (timezone.now() - timedelta(days=4)).date()
        end_date = (timezone.now() - timedelta(days=2)).date()
        response = self.client.get(url, {'start_date': start_date, 'end_date': end_date})

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['transactions']), 1)
        self.assertEqual(response.data['total_balance'], 50.00)


    def test_deposit_negative_amount(self):
        url = reverse('transaction-list', kwargs={'account_id': self.account1.id})
        data = {
            'transaction_type': 'deposit',
            'amount': -50.00  
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('The transaction amount must be greater than zero', response.data['amount'])