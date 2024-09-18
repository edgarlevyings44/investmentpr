from django.urls import path
from .views import TransactionViewSet
from .views import AdminUserTransactionsView

transaction_list = TransactionViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

transaction_detail = TransactionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('api/accounts/<int:account_id>/transactions/', transaction_list, name='transaction-list'),
    path('api/accounts/<int:account_id>/transactions/<int:pk>/', transaction_detail, name='transaction-detail'),
    path('api/admin/users/<int:user_id>/transactions/', AdminUserTransactionsView.as_view(), name='admin-user-transactions'),
]