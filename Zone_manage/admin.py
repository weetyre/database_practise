from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username = forms.CharField(label='username', max_length=20, min_length=6,
                               widget=forms.TextInput(attrs={'class': 'form-input'}),
                               error_messages={'required': 'username already taken.',})
    password = forms.CharField(label='Password', max_length=18, min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password_confirmation = forms.CharField(label='Password confirmation', max_length=18, min_length=6,
                                            widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', max_length=50, widget=forms.EmailInput(attrs={'class': 'from-input'})
                             ,error_messages={'required': 'email already taken.',})

    class Meta:
        model = MyUser
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("passwords don't match")
        return password_confirmation

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # here set current time to created_date
        user.set_created_date()
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'created_at', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'created_at', 'type', 'is_admin')
    list_filter = ('is_admin', 'type')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('created_at',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Type', {'fields': ('type',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'created_at', 'type', 'password', 'password_confirmation','is_admin')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
