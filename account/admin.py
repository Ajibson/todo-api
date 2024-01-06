from django.contrib import admin

from .models import Account, Token


admin.site.register(Account)
admin.site.register(Token)
