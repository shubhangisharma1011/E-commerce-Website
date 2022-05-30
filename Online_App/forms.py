from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms import ModelForm
from django import forms
from .models import Employee, Manager, Orders

#create your models here

class EmployeeForm(ModelForm):
    YEARS = [x for x in range(1940, 2021)]
    employee_dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = Employee
        fields = '__all__'


class ManagerForm(ModelForm):
    YEARS = [x for x in range(1940, 2021)]
    manager_dob = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = Manager
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','address','phone','file']

from .models import Profile,Product_Details
from django import forms

class UpdatedProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','address','phone','file']
####################################################################33
class Product_DetailsForm(forms.ModelForm):
    class Meta:
        model = Product_Details
        fields = ['name','product_category','image','product_description','product_original_price','price']

class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'