from django.urls import path

from .views import ConfirmAccount, CustomerLogin

from .views import CreateCustomer, CustomerProfile


urlpatterns = [
    path('', CreateCustomer.as_view(), name='all_vendors'),
    path('dashboard/', CustomerProfile.as_view(), name='customer_dashboard'),
    path('confirm-account/', ConfirmAccount.as_view(), name='confirm_account'),
    path('signin/', CustomerLogin.as_view(), name='sign_in')
]