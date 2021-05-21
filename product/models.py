from django.db import models

from vendor.models import Vendor


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    '''
    def get_absolute_url(self):
        return reverse('shop_by_category', args=[self.slug])
    '''

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    categories = models.ManyToManyField(Category, related_name='categories')
    slug = models.SlugField(max_length=200,db_index=True)
    quantity_available = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor')

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(unique=True)

    def __str__(self):
        return f"{self.image.url}"

    


