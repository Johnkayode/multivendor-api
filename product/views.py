from django.shortcuts import render, get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from vendor.models import Vendor
from vendor.permissions import IsVendor

from .models import Image, Product, Category, Image
from .serializers import ImageSerializer, ProductSerializer, CategorySerializer



class CategoryView(generics.ListCreateAPIView):
    permission_classes = ()
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    


class CreateListProduct(generics.ListCreateAPIView):
    permission_classes = ()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def get(self, request, vendor_id=None):

        if vendor_id:
            vendor = get_object_or_404(Vendor, id=vendor_id)
            products = Product.objects.filter(vendor=vendor)
        else:
            products = Product.objects.all()

        data = ProductSerializer(products, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor = get_object_or_404(Vendor, user=request.user)
        product = Product.objects.create(vendor=vendor,
        name=serializer.data['name'],
        slug=serializer.data['slug'],
        price=serializer.data['price'],
        quantity_available=serializer.data['quantity_available'],
        description=serializer.data['description'])

        slugs = [dict(x)['slug'] for x in serializer.data['categories']]

        categories = Category.objects.filter(slug__in=slugs)
        product.categories.set(categories)

        return Response(
            {"detail": "Product successfully created!"}, status=status.HTTP_201_CREATED
        )




class ImageUploadView(generics.CreateAPIView):
    permission_classes = (IsVendor,)
    queryset =  Image.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, product_slug):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, slug=product_slug)
    
        if request.user == product.vendor.user:
            serializer.save(product=product)
            return Response(
                {"detail": f"{product.name}'s image successfully added!"}, status=status.HTTP_201_CREATED
            )
        
        return Response(
            {"detail": "You don't have necessary permission(s) for this action"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


        


