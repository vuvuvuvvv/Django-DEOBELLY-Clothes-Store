"""clothes_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import accounts.views as acc_views
from system.constant import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib.auth import views as auth_views
from core import views as core_views
from products import views as pr_views
from test import views as test_views
from cart import views as cart_views
from order import views as order_views

urlpatterns = [
    #
    path('favicon.ico/',RedirectView.as_view(url='/static/images/favicon.ico')),
    #
    path("admin/", admin.site.urls),
    # core
    path("", core_views.index, name="home"),
    path('terms-and-services/',core_views.terms, name='terms'),
    path('our-stories/',core_views.our_stories, name='our_stories'),
    path('contact/',core_views.ContactView.as_view(), name='contact'),

    #auth
    path("signup/", acc_views.signup, name="signup"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/", auth_views.LogoutView.as_view(), name="logout"
    ),    
    path(
        "validate_infor_user/",
        acc_views.validate_infor_user,
        name="validate_infor_user",
    ),
    # reset pass
    path(
        "reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            html_email_template_name="password_reset_email.html",
            subject_template_name="password_reset_subject.txt",
            extra_email_context = {
                'PHONE_CONTACT':PHONE_CONTACT,
                'ADMIN_MAIL':ADMIN_MAIL,
                'COMPANY_ADDRESS':COMPANY_ADDRESS,
                'SENDER_NAME':SENDER_NAME
            }
        ),
        name="password_reset",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),

    # url login with google
    path("", include("allauth.urls")),
    path("", include("allauth.socialaccount.urls")),
    path('', include('social_django.urls', namespace='social')),

    #api
    path('api_check_user_validated/', acc_views.check_user_validated, name='api_check_user_validated'),
    path('api_product_filter/',pr_views.Shop.as_view(), name='product_filter_api'),
    path('api_geolocation_get_address/',core_views.get_geolocation, name='geolocation_filter_api'),
    path('cart/add-to-cart/',cart_views.CartView.as_view(), name='add_cart'),
    path('cart/update-cart/',cart_views.CartView.as_view(), name='update_cart'),
    path('cart/delete-cart/',cart_views.CartView.as_view(), name='delete_cart'),

    #product
    path('shop/', pr_views.Shop.as_view(), name='shop'),
    path('shop/detail/', pr_views.ProductDetail.as_view(), name='detail'),
    path('cart/',cart_views.CartView.as_view(), name='cart'),
    path('checkout/',order_views.CheckoutView.as_view(), name='checkout'),
    
    # todo
    path('',core_views.index, name='search_product'),
    path('',core_views.index, name='ajax_create_contact'),
]

#important to show images!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)