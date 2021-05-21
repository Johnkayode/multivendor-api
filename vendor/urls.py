from django.urls import path

from .views import VendorList, VendorDetail, ConfirmAccount, VendorLogin, VendorProfile


urlpatterns = [
    path('', VendorList.as_view(), name='all_vendors'),
    path('<int:uid>/', VendorDetail.as_view(), name='vendor_detail'),
    path('confirm-account/', ConfirmAccount.as_view(), name='confirm_account'),
    path('signin/', VendorLogin.as_view(), name='sign_in'), 
    path('dashboard/', VendorProfile.as_view(), name='vendor_dashboard')
]