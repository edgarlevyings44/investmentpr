from django.contrib import admin
from .models import InvestmentAccount, Transaction, UserInvestmentAccount

admin.site.register(InvestmentAccount)
admin.site.register(Transaction)
admin.site.register(UserInvestmentAccount)