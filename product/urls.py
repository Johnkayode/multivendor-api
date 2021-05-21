from django.urls import path

from .views import CreateListProduct, ImageUploadView, CategoryView


urlpatterns = [
    path('', CreateListProduct.as_view(), name='create_list_products'),
    path('<int:id>/', CreateListProduct.as_view(), name='get_vendor_products'),
    path('<slug:product_slug>/image/', ImageUploadView.as_view(), name='upload_image'),
    path('categories/', CategoryView.as_view(), name='categories')

]