from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from system.function import to_slug
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator,MinValueValidator, MaxValueValidator
from system.constant import *
from django.db.models import F

class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField('ProductCategory', related_name='types', blank=True)
    status = models.IntegerField(default = STATUS_ACTIVE, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_all_product_type(cls):
        return cls.objects.filter(status = STATUS_ACTIVE).values()

# Suit, Vest, Ví, Túi, Giày, Dây lưng,
class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    products = models.OneToOneField('Product', related_name='categories_products',on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(default = STATUS_ACTIVE, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    # cost_price = models.DecimalField(max_digits=10, decimal_places=0)
    regular_price = models.DecimalField(max_digits=10, decimal_places=0)
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        default=0
    )
    sale_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL, null=True, related_name='products_category')
    quantity = models.IntegerField(null= False, default= 0)
    image = models.ImageField(upload_to='product/', blank=True)
    related_images = models.CharField(max_length=3000, blank=True)
    # is_feature = models.IntegerField(default = STATUS_ACTIVE, choices=FEATURE_CHOICES)
    sold = models.IntegerField(default = 0)
    fake_sold = models.IntegerField(null= True,blank=True)
    viewed = models.IntegerField(null= True,blank=True)
    status = models.IntegerField(default = STATUS_ACTIVE, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.sale_price is None and self.regular_price is not None and self.discount is not None:
            self.selling_price = (100 - self.discount) / 100 * self.regular_price
        elif self.discount is None and self.regular_price is not None and self.sale_price is not None:
            self.selling_price = self.sale_price
        elif self.discount is None and self.regular_price is not None and self.sale_price is None:
            self.selling_price = self.regular_price
        elif self.discount is None and self.regular_price < self.sale_price:
            self.selling_price = self.regular_price
            self.sale_price = self.selling_price
        elif self.discount is not None and self.regular_price is not None and self.sale_price is not None:
            self.selling_price = (100 - self.discount) / 100 * self.regular_price
            self.sale_price = self.selling_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_best_selling_related_product_by_cate_slug(cls, slug):
        # Get object of ProductCate by slug to query Product by category objetcs
        # and sorted DESC by sold with '-sold' and get last 5 records 
        # -> top 5 record with the highest sold
        try:
            get_cate = get_object_or_404(ProductCategory, slug = slug)
            return cls.objects.filter(category=get_cate, status = STATUS_ACTIVE).order_by('-sold').order_by('?').values()[:5]
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_promotion_related_product_by_cate_slug(cls, slug):
        # __gt: greater than: >
        # __get: greater than or equal >=
        # __lt: less than: <
        # __lte: less than or equal <= 
        try:
            get_cate = get_object_or_404(ProductCategory, slug = slug)
            return cls.objects.filter(category=get_cate, status=STATUS_ACTIVE).exclude(regular_price=F('selling_price')).order_by('?').values()[:5]
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_product_by_slug(cls, slug):
        try:
            return cls.objects.get(slug=slug, status = STATUS_ACTIVE)
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def get_product_by_id(cls, id):
        try:
            return cls.objects.get(id=id, status = STATUS_ACTIVE)
        except cls.DoesNotExist:
            return None
@receiver(pre_save, sender=ProductType)
@receiver(pre_save, sender=ProductCategory)
@receiver(pre_save, sender=Product)
def custom_update(sender, instance, **kwargs):
    if instance.pk is None or instance.name != sender.objects.get(pk=instance.pk).name:
        instance.slug = to_slug(instance.name)
