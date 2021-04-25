from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext, gettext_lazy as _
from .models import Account

class RegisterationForm(UserCreationForm):

    email = forms.EmailField(
        label=_('電子信箱'),
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        error_messages={
                         'invalid': '請輸入有效電子信箱',
                         'required':'尚未輸入電子信箱',
                        }
    )

    password1 = forms.CharField(
        label=_('密碼'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        error_messages={'required':'尚未輸入密碼'},
    )

    password2 = forms.CharField(
        label=_('確認密碼'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        error_messages={'required':'尚未輸入確認密碼'},
    )


    error_messages = {
        'password_mismatch': ('兩次密碼輸入不同'),
    }

    class Meta:

        model = Account
        fields = ('email', 'password1', 'password2')

    def clean_email(self):

        email = self.cleaned_data['email']
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'{email} 已被註冊')


class LogInForm(forms.ModelForm):

    email = forms.EmailField(error_messages={'required':'請輸入電子信箱'})
    password = forms.CharField(error_messages={'required':'請輸入密碼'})

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("登入失敗，請確認電子信箱和密碼")


class ResetPasswordForm(SetPasswordForm):

    error_messages = {
        'password_mismatch': _('兩次密碼輸入不同'),
    }
    new_password1 = forms.CharField(
        label=_("新密碼"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        error_messages={'required':'尚未輸入密碼'},
    )
    new_password2 = forms.CharField(
        label=_("確認新密碼"),
        strip=False,
        error_messages={'required':'尚未輸入密碼'},
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super().__init__(*args, **kwargs)

    # def clean_new_password2(self):
    #     password1 = self.cleaned_data.get('new_password1')
    #     password2 = self.cleaned_data.get('new_password2')
    #     if password1 and password2:
    #         if password1 != password2:
    #             raise ValidationError(
    #                 self.error_messages['password_mismatch'],
    #                 code='password_mismatch',
    #             )
    #     password_validation.validate_password(password2, self.user)
    #     return password2

    # def save(self, commit=True):
    #     password = self.cleaned_data["new_password1"]
    #     self.user.set_password(password)
    #     if commit:
    #         self.user.save()
    #     return self.user