from django.contrib import admin
from .models import Product_Details,Index_Page
from .models import Employee, Country, State, City, District, Manager, OrderUpdate

# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_name', 'country_code']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['state_name', 'state_code']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city_name', 'city_code']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['district_name', 'district_code']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_firstname','employee_middlename','employee_lastname','employee_address',
                    'employee_experience','employee_designation','employee_id','employee_monthsalary',
                    'employee_per_annum_salary', 'employee_pf', 'employee_telephone','employee_mobile',
                    'employee_email','employee_tax','employee_country','employee_state','employee_city',
                    'employee_district','employee_dob']

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['manager_firstname','manager_middlename','manager_lastname','manager_address',
                    'manager_experience','manager_designation','manager_monthlysalary','manager_id',
                    'manager_per_annum_salary','manager_pf','manager_telephone','manager_mobile','manager_email',
                    'manager_tax','manager_dob','manager_country','manager_state',
                    'manager_city','manager_district']

class Product_Details_Admin(admin.ModelAdmin):
    list_display = ['id','name','product_category','image','product_description',
                    'product_original_price','price','product_upload_date']

@admin.register(Index_Page)
class Index_Page_Admin(admin.ModelAdmin):
    list_display = ['index_image']


"""Integrate with admin module."""
from django.contrib import admin
from .models import CustomUser,Orders

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'first_name', 'last_name', 'is_staff', 'phone', 'address', 'file',]

from .models import User_Model_Email_Verification
admin.register(User_Model_Email_Verification)
list_display = ['user','token','verify']


@admin.register(Product_Details)
class home(admin.ModelAdmin):
    list_display = ['id','name','image']

@admin.register(Orders)
class Orders_Details(admin.ModelAdmin):
    list_display = ['order_id','items_json','amount','name','email','address','city','state','zip_code','phone']

admin.site.register(OrderUpdate)