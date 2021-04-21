from django.http import request
from authapp.models import User, UserAddress
from django.db import models
from .utils import (
    product_image_directory_path,
    product_thumbnail_directory_path,
    product_unique_slug_generator_using_name,
    product_category_name_unique_slug_generator_using_name,
    product_company_name_unique_slug_generator_using_name
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):

    slug = models.SlugField(
        max_length=255, 
        blank=True,
        null=True, 
        db_index=True,
        help_text=_(
            'This will be automatically generated using Category Name.'
        ),
    )
    category_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = product_category_name_unique_slug_generator_using_name(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"


class Company(models.Model):

    slug = models.SlugField(
        max_length=255, 
        blank=True,
        null=True, 
        db_index=True,
        help_text=_(
            'This will be automatically generated using Company Name.'
        ),
    )
    company_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = product_company_name_unique_slug_generator_using_name(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Product Company"
        verbose_name_plural = "Product Companies"


class Product(models.Model):

    slug = models.SlugField(
        max_length=255, 
        blank=True,
        null=True, 
        db_index=True,
        help_text=_(
            'This will be automatically generated using Product Name.'
        ),
    )
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        to = Category,
        on_delete = models.CASCADE,
    )
    description = models.CharField(max_length=2000)
    thumbnail = models.ImageField(
        upload_to=product_thumbnail_directory_path,
        blank=True
    )
    price = models.PositiveIntegerField(default=0)
    company = models.ForeignKey(
        to = Company,
        on_delete = models.CASCADE,
    )
    is_draft = models.BooleanField(
        default = False,
        help_text=_(
            'Checking this box will not show this product on main page.'
            'Select this instead of deleting product.'
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = product_unique_slug_generator_using_name(self)
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

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE
    )
    images = models.FileField(upload_to = product_image_directory_path)

    def __str__(self):
        return self.product.name


class Order(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, blank=True, null=True)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_cart_total(self):
        orderitems = OrderItem.objects.filter(order=self)
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = OrderItem.objects.filter(order=self)
        total = int(sum([item.quantity for item in orderitems]))
        return total

    def __str__(self):
        return self.user.username + " - " + str(self. date_created)


class OrderItem(models.Model):
    
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product.name + " - " + str(self.order.id)

    