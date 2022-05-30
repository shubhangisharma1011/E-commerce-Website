from django.conf import settings
from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Online_App import views
from django.contrib.auth import views as auth_views
from Online_App.views import account_verify


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Online_App/', include('django.contrib.auth.urls')),
    path('employee/', views.EmployeeView.as_view(), name="employee"),
    path('emptable/', views.EmployeeTableView.as_view(), name="emptable"),
    path('manager/', views.ManagerView.as_view(), name="manager"),
    path('managertable/', views.ManagerTableView.as_view(), name="managertable"),
    path('',views.Index_Viewset.as_view(), name="Index"),
    path('Login_View/',views.Login_View.as_view(), name="Login_View"),
    path('Registration_View/',views.Registration_View.as_view(), name="Registration_View"),
    path('Home_View/',views.Home_View.as_view(), name="Home_View"),
    path('Logout_View/',views.Logout_View.as_view(), name="Logout_View"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
    path('account-verify/<slug:token>', account_verify, name="account_verify"),
    path('accounts/', include('allauth.urls')),
    path('Change_Password/', views.Change_Password.as_view(), name='Change_Password'),
    ###Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    # for payment details
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),

    # for Read More
    path('Read_More/<int:id>', views.read_more, name='Read_More'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)