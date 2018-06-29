from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import MyUser
from .forms import UserCreationForm,UserChangeForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','gender','class_name','father_name','father_occupation','mother_name','mother_occupation','date_of_birth','date_of_joining','subjects_opted','mobile','address','city','comments','profile_pic',)}),
        #         fields=('first_name','last_name','gender','father_name','class_name',,'mobile','address','city')

        ('Permissions', {'fields': ('is_admin','is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'fields': ('username','email', 'password1', 'password2')}
            'fields': ('username','email','password1','password2','first_name','last_name','gender','class_name','father_name','father_occupation','mother_name','mother_occupation','date_of_birth','date_of_joining','subjects_opted','mobile','address','city','comments','profile_pic',)}

        ),
    )
    search_fields = ('username','email',)
    ordering = ('username','email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
