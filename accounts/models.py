from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class InvestmentAccount(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    users = models.ManyToManyField(User, through='UserInvestmentAccount')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'deposit':
            self.account.balance += self.amount
        elif self.transaction_type == 'withdrawal' and self.account.balance >= self.amount:
            self.account.balance -= self.amount
        
        self.account.save()
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.username}"


class UserInvestmentAccount(models.Model):
    ROLE_CHOICES = [
        ('view', 'View Only'),
        ('crud', 'Full CRUD'),
        ('post', 'Post Only'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'account')

    def __str__(self):
        return f"{self.user.username} - {self.role} on {self.account.name}"