from django.shortcuts import get_object_or_404
from rest_framework import serializers

from vendor.models import Vendor
from vendor.serializers import VendorSerializer

from .models import Product, Image, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name","slug")

        extra_kwargs = {
            "slug": {'validators': []},
            "closed": {"slug": True},
        }




    

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ("image",)

    def to_native(self, value):
        return f'{value.image.url}'
    

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    images = ImageSerializer(many=True, read_only=True)

    
    class Meta:
        model = Product
        fields = ("name", "categories", "slug", "price", "quantity_available","description","images")

       


        






