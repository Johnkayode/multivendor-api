from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-dashboard/', admin.site.urls),
    path('vendors/', include('vendor.urls')),
    path('customers/', include('customer.urls')),
    path('administrators/', include('administrator.urls')),
    path('products/', include('product.urls')),

]

'''
    path('products', include('product.urls')),
    path('orders/', include('order.urls')),
    path('wallet/', include('wallet.urls'))
    '''