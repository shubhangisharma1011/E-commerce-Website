from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Country(models.Model):
    country_name = models.CharField(max_length=50)
    country_code = models.IntegerField()

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = 'country_details'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


##model for state employee and manager
class State(models.Model):
    state_name = models.CharField(max_length=50)
    state_code = models.IntegerField()

    def __str__(self):
        return self.state_name

    class Meta:
        db_table = 'state_details'
        verbose_name = 'State'
        verbose_name_plural = 'States'


class City(models.Model):
    city_name = models.CharField(max_length=50)
    city_code = models.IntegerField()

    def __str__(self):
        return self.city_name

    class Meta:
        db_table = 'city_details'
        verbose_name = 'City'
        verbose_name_plural = 'Citys'


class District(models.Model):
    district_name = models.CharField(max_length=30)
    district_code = models.IntegerField()

    def __str__(self):
        return self.district_name

    class Meta:
        db_table = 'district_details'
        verbose_name = 'District'
        verbose_name_plural = 'Districts'


#Employee Model
class Employee(models.Model):
    employee_firstname = models.CharField(max_length=50,)
    employee_middlename = models.CharField(max_length=50, null=True, blank=True)
    employee_lastname = models.CharField(max_length=50, null=True, blank=True)
    employee_address = models.CharField(max_length=100)
    employee_experience = models.IntegerField()
    employee_designation = models.CharField(max_length=50)
    employee_id = models.IntegerField(unique=True)
    employee_monthsalary = models.IntegerField()
    employee_per_annum_salary = models.IntegerField()
    employee_pf = models.IntegerField()
    employee_telephone = models.IntegerField()
    employee_mobile = models.IntegerField()
    employee_email = models.EmailField(max_length=25)
    '''for giving the range to the dob need to mention into forms.py'''
    employee_dob = models.DateField(null=True, blank=True)
    employee_tax = models.IntegerField(null=True, blank=True)
    '''apply foregin key and fetch the country,state,city and district model fields'''
    employee_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='Employee_Country')
    employee_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='Employee_State')
    employee_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='Employee_City')
    employee_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='Employee_District')

    def __str__(self):
        return self.employee_firstname

    class Meta:
        db_table = 'employee_details'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'


class Manager(models.Model):
    Employee = models.ManyToManyField(Employee)
    manager_firstname = models.CharField(max_length=50, null=False, blank=False)
    manager_middlename = models.CharField(max_length=50, null=True, blank=True)
    manager_lastname = models.CharField(max_length=50, null=True, blank=True)
    manager_address = models.CharField(max_length=100)
    manager_experience = models.IntegerField()
    manager_designation = models.CharField(max_length=50)
    manager_monthlysalary = models.IntegerField()
    manager_id = models.IntegerField(unique=True)
    manager_per_annum_salary = models.IntegerField(null=True, blank=True)
    manager_pf = models.IntegerField()
    manager_telephone = models.IntegerField()
    manager_mobile = models.IntegerField()
    manager_email = models.EmailField(max_length=25)
    manager_tax = models.IntegerField(null=True, blank=True)
    '''DOB field with range and also mention into forms.py'''
    manager_dob = models.DateField(null=True, blank=True)
    '''apply foregin key and fetch the country,state,city and district model field'''
    manager_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='Manager_Country')
    manager_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='Manager_State')
    manager_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='Manager_City')
    manager_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='Manager_District')

    def __str__(self):
        return self.manager_firstname

    class Meta:
        db_table = 'managers_details'
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'



class Product_Details(models.Model):
    name = models.CharField(max_length=80)
    product_category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Product_Images')
    product_description = RichTextField(blank=True)
    product_original_price = models.IntegerField()
    price = models.IntegerField()
    product_upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "product_details"
        verbose_name = "product"
        verbose_name_plural = "products"


import uuid

class Orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    amount=models.CharField(max_length=1000000 ,default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    phone=models.CharField(max_length=10, validators=[MinLengthValidator(10)])

    def __str__(self):
        return self.name

    class Meta():
        db_table = "placed_order"
        verbose_name = "order"
        verbose_name_plural = "orders"

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add = True)



class Index_Page(models.Model):
    index_image = models.FileField(upload_to='index_images')

    class Meta():
        db_table = "index_page"
        verbose_name = "index"
        verbose_name_plural = "index"


#User Model Login with email + use for login registration (Default Model)
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.utils.translation import ugettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class Profile(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    file = models.FileField(upload_to="Update_Profile", default='images.png')

#create the model for display the fields into update profile
#for update the profile picture and also mention into views,models,forms
class CustomUser(AbstractUser):
    """User model."""
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True, null=True, blank=True)
    file = models.FileField(upload_to="User_Images", default='images.png')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

#a new models for email verification by link
class User_Model_Email_Verification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
    token = models.CharField(max_length=150)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.token

