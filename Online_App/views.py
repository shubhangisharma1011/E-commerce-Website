from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from razorpay.resources import order

from .models import User_Model_Email_Verification, OrderUpdate
from .forms import CreateUserForm
from django.core.mail import send_mail
from django.conf import settings
import uuid
from .models import Product_Details,Index_Page
# for change the password use inbuilt form
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EmployeeForm, ManagerForm, OrderForm
from .models import Employee, Manager, Orders
#for ADD CART:(PYPI)
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
#for paytm payment
MERCHANT_KEY = "zbUhg2xUXemqwgMH"
from .PayTm import Checksum
# Create your views here.

class EmployeeTableView(View):
    def get(self, request):
        employee_form = Employee.objects.all()
        context = {'empform': employee_form}
        return render(request, 'table.html', context)


class EmployeeView(View):
    def get(self, request):
        form = EmployeeForm()
        '''get the employee form on web page'''
        return render(request,'employee.html',{'form': form})

    def post(self, request):
        form1 = EmployeeForm()
        form1 = EmployeeForm(request.POST)
        if form1.is_valid():
            '''if post data is valid then save the data '''
            form1.save()

            '''in case data is not valid then show error'''
        else:
            return HttpResponse("not Submitted !!")
        '''in case form is valid then redirect on emptable page'''
        return redirect('emptable')

'''def manager table and show the data into table on web page'''

class ManagerTableView(View):
    def get(self, request):
        manager_form = Manager.objects.all()
        context = {'form': manager_form}
        return render(request, 'managertable.html', context)


#Manager Form get and post through class view

class ManagerView(View):
    def get(self, request):
        forms = ManagerForm()
        '''get the manager form on web page'''
        return render(request, 'manager.html', {'forms': forms})

    def post(self, request):
        forms1= ManagerForm()
        forms1 = ManagerForm(request.POST)
        if forms1.is_valid():
            '''if post data is valid then save the data 
            and redirect on managertable'''
            forms1.save()
        else:
            return HttpResponse("Data Not Submitted")
        return redirect('managertable')


class Index_Viewset(View):
    def get(self, request):
        table = Index_Page.objects.all()
        return render(request,'Index.html', {'table':table})

#for email verification
def send_email_after_registration(email,token):
    subject = "Verify Email"
    message = f"Hi click on the link to verify your account http://127.0.0.1:8000/account-verify/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)


class Registration_View(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request,'Registration_2.html',{'form':form})
    def post(self, request):
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            uid = uuid.uuid4()
            em_obj = User_Model_Email_Verification(user=new_user, token=uid)
            em_obj.save()
            send_email_after_registration(new_user.email, uid)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, 'verification link send to your email' + first_name+ last_name)
        else:
            print(form.errors)  # for display the error via form
            context = {'form': form}
            return render(request, 'Registration_2.html', context)
        return redirect('Login_View')

def account_verify(request, token):
    account_activate = User_Model_Email_Verification(token=token)
    account_activate.verify = True
    account_activate.save()
    return redirect('Login_View')

class Login_View(View):
    def get(self,request):
        form = CreateUserForm()
        context = {'form':form}
        return render(request, 'Login.html',context)
    def post(self, request):
        form = CreateUserForm(request.POST)
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
        else:
            messages.error(request, 'Please fill the correct details')
            return redirect('Login_View')
        messages.success(request,"Welcome! "+email)
        return redirect('Home_View')


class Logout_View(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Successfully logout")
        return redirect('/')

from .forms import UpdatedProfileForm,Product_DetailsForm
@method_decorator(login_required, name='dispatch')
class Home_View(View):
    def get(self, request):
        ProductTable = Product_Details.objects.all()
        form = CreateUserForm()
        return render(request, 'shopping_website.html', {'form': form, 'ProductTable': ProductTable})
    def post(self, request):
        form = UpdatedProfileForm(request.POST, request.FILES, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Update')
            return redirect('Home_View')
        else:
            messages.error(request, "do not update")
            return redirect('Update_Profile')

@method_decorator(login_required, name='dispatch')
class Change_Password(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})
    def post(self, request):
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('Home_View')
            else:
                messages.error(request, 'Please correct the error below.')
            return HttpResponse("Please Correct the Error")

#Read more
def read_more(request, id):
    ProductTable = Product_Details.objects.get(id=id)
    context = {'ProductTable':ProductTable}
    return render(request, 'read_more.html', context)

#Add Cart
@login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product_Details.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product_Details.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product_Details.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product_Details.objects.get(id=id)
    cart.remove(product=product)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'cart_detail.html')


##for payment
class Checkout(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'checkout.html',{'form':form})
    def post(self, request):
        form = OrderForm(request.POST)
        items_json = request.POST['items_json']
        amount = request.POST['amount']
        name = request.POST['name']
        email = request.POST['email']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        phone = request.POST['phone']
        order = Orders(name=name, email=email,city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount, items_json=items_json)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        param_dict = {

            'MID': 'ePlvKF59582708748321',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING', #webstaging is use for testing purpose
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})
#@csrf_exempt to the top of your view, then basically telling the view that it doesn't need the token.
#This is a security exemption that you should take seriously.
@csrf_exempt
def handlerequest(request):
    #paytm will send post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]  = form[i]
        if i == "CHECKSUMHASH":
            checksum=form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("order success")
        else:
            print("order not success because" + response_dict['RESPMG'])
    return render(request, 'paymentstatus.html', {'response':response_dict})

