from django.db import models
from .utils import (
    product_image_directory_path,
    product_thumbnail_directory_path,
    unique_slug_generator_using_name
)
from django.urls import reverse

class Product(models.Model):

    slug = models.SlugField(max_length=255, blank=True,null=True, db_index=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    thumbnail = models.ImageField(upload_to=product_thumbnail_directory_path,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator_using_name(self)
        super().save(*args, **kwargs)
    
    @property
    def get_all_images(self):
        return ProductImage.objects.filter(product=self)
    
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={
            "slug": self.slug
        })
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):

    product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    images = models.FileField(upload_to = product_image_directory_path)

    def __str__(self):
        return self.product.name
