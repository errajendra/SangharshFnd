from dataclasses import fields
import unicodedata
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import BloodDonate, CustomUser, Activity, District, FoundationAccountSetting
from django.forms.fields import DateField
from django.forms import widgets

from django.contrib.auth import get_user_model


# Create your forms here.


UserModel = get_user_model()

class emailField(forms.EmailField):
    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "email",
        }


# update user form through admin
class UpdateUserFormAdmin(UserChangeForm):

    valid_up_to =  DateField(widget=widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ("name", "valid_up_to", "blood_group", "father_name", "mobile_nomber", "role", "address1", "address2", "district", "profile", "staff", "admin")


# update user form through staff
class UpdateUserFormStaff(UserChangeForm):

    valid_up_to =  DateField(widget=widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CustomUser
        fields = ("name", "valid_up_to", "blood_group", "father_name", "mobile_nomber", "alternet_mobile_nomber", "role", "district", "profile", "staff")



# # update user form through member
class UpdateProfileForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ("name", "blood_group", "father_name", "mobile_nomber", "alternet_mobile_nomber", "profile", 'address1', 'address2')


# new user create form
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ("email", "name", "blood_group", "father_name", "mobile_nomber", "alternet_mobile_nomber", "district", "profile", "valid_up_to", "password1", "password2")

 
# new user create form from out sourse
class NewUserFormOut(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ("email", "name", "blood_group", "father_name", "district", "mobile_nomber", "alternet_mobile_nomber", "profile", "password1", "password2")

 
class BloodDonateForm(forms.ModelForm):
    
    date = DateField(widget=widgets.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = BloodDonate
        fields = ("donator", "patient_name", "patient_blood_group", "patient_mobile","patient_address", "receiver_name","receiver_mobile","receiver_address","date","message")
        
        
        
class ActivityForm(forms.ModelForm):
    
    class Meta:
        model = Activity
        exclude = ('added_by',)
        # fields = '__all__'
        
          
        
class DistrictForm(forms.ModelForm):
    
    class Meta:
        model = District
        fields = '__all__'
        
             
        
class AccountSettingForm(forms.ModelForm):
    
    class Meta:
        model = FoundationAccountSetting
        fields = '__all__'
        
        
        
        
                
