from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegistrationForm
from django.utils.translation import gettext, gettext_lazy as _

from .models import Account


class AccountAdmin(UserAdmin):

    list_display = ('email', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    ordering = ('email',)  # solution for E033

    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_admin', 'is_staff', 'is_superuser',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    add_form = RegistrationForm


admin.site.register(Account, AccountAdmin)
