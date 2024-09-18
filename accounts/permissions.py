from rest_framework import permissions
from .models import UserInvestmentAccount

class IsViewOnly(permissions.BasePermission):
    """
    Custom permission to allow view-only access.
    """
    def has_permission(self, request, view):
        account_id = view.kwargs.get('account_id')
        if account_id:
            try:
                user_role = UserInvestmentAccount.objects.get(user=request.user, account__id=account_id).role
                if user_role == 'view' and request.method in permissions.SAFE_METHODS:
                    return True 
            except UserInvestmentAccount.DoesNotExist:
                return False
        return False


class IsFullCRUD(permissions.BasePermission):
    """
    Custom permission to allow full CRUD (Create, Read, Update, Delete) access.
    """
    def has_permission(self, request, view):
        account_id = view.kwargs.get('account_id')
        if account_id:
            try:
                user_role = UserInvestmentAccount.objects.get(user=request.user, account__id=account_id).role
                if user_role == 'crud':
                    return True 
            except UserInvestmentAccount.DoesNotExist:
                return False
        return False


class IsPostOnly(permissions.BasePermission):
    """
    Custom permission to allow only POST access (create transactions).
    """
    def has_permission(self, request, view):
        account_id = view.kwargs.get('account_id')
        if account_id:
            try:
                user_role = UserInvestmentAccount.objects.get(user=request.user, account__id=account_id).role
                if user_role == 'post' and request.method == 'POST':
                    return True 
            except UserInvestmentAccount.DoesNotExist:
                return False
        return False