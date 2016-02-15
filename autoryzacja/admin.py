from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from autoryzacja.models import PipesUser

# Register your models here.
class PipesUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = PipesUser
        fields = ('email', 'first_name', 'last_name', 'is_admin')

    def clean_password2(self):
        password_first = self.cleaned_data.get("password1")
        password_second = self.cleaned_data.get("password2")

        if not password_first or not password_second or password_first != password_second:
            raise forms.ValidationError("Hasła nie są takie same")
        validate_password(password_second)

        return password_second

    def save(self, commit=True):
        user = super(PipesUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PipesUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = PipesUser
        fields = ('email', 'password', 'first_name', 'last_name', 'is_admin')

    def clean_password(self):
        return "dupa"


class PipesUserAdmin(UserAdmin):
    #fields = ('email', 'first_name', 'last_name', 'is_admin')
    add_form = PipesUserCreationForm
    form = PipesUserChangeForm

    list_display = ('email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Email', {
            'fields': ('email',),
        }),
        ('Imię i nazwisko', {
            'fields': (('first_name', 'last_name')),
        }),
        ('Hasło', {
            'fields': ('password',)
        }),
        ('Administrator', {
            'fields': ('is_admin',),
            'description': ('Zaznacz jeżeli konto ma być kontem administratora'),
        }),
    )

    add_fieldsets = (
        ('Email', {
            'fields': ('email',),
        }),
        ('Imię i nazwisko', {
            'fields': (('first_name', 'last_name')),
        }),
        ('Hasłp',{
            'fields': ('password1', 'password2')
        }
        ),
        ('Administrator', {
            'fields': ('is_admin',),
            'description': ('Zaznacz jeżeli konto ma być kontem administratora'),
        }),
    )

    search_fields = ('email', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(PipesUser, PipesUserAdmin)
admin.site.unregister(Group)