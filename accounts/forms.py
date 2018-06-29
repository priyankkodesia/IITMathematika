from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.admin import widgets
from datetime import date
from events.models import EventModel

MyUser=get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username','email','password1','password2','first_name','last_name','gender','class_name','father_name','father_occupation','mother_name','mother_occupation','date_of_birth','date_of_joining','subjects_opted','mobile','address','city','comments','profile_pic',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
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
        # fields = ('username','email', 'password','is_staff', 'is_active', 'is_admin')
        fields = ('username','email','password','first_name','last_name','gender','class_name','father_name','father_occupation','mother_name','mother_occupation','date_of_birth','date_of_joining','subjects_opted','mobile','address','city','comments','profile_pic','is_staff', 'is_active', 'is_admin')


    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserEditForm(forms.ModelForm):

    class Meta:
        model = MyUser
        # fields = ('username','email', 'password','is_staff', 'is_active', 'is_admin')
        fields = ('username','email','first_name','last_name','gender','class_name','father_name','father_occupation','mother_name','mother_occupation','date_of_birth','date_of_joining','subjects_opted','mobile','address','city','comments','profile_pic',)
        widgets = {
            'date_of_birth': DateInput(),
            'date_of_joining': DateInput()
                }

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserLoginForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= MyUser
        fields=('username','password',)


class StudentFetchForm(forms.ModelForm):
    class Meta:
        model=MyUser
        fields=('class_name','username')
        
        
class EventAddForm(forms.ModelForm):
    content = forms.CharField()
    class Meta:
        model=EventModel
        fields=['occur_date','content']