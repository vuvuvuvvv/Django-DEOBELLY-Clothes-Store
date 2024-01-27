from django.contrib import admin
from .models import *
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from system.constant import *
from .forms import *
import os
from PIL import Image
from django.conf import settings
import random
# Register your models here.

class MultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_categories_display', 'status', 'created_at', 'updated_at')
    fields = ('name', 'categories', 'status')
    list_filter = ('status', 'categories')
    
    def get_categories_display(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])
    get_categories_display.short_description = 'Categories'
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["widget"] = admin.widgets.FilteredSelectMultiple(("Categories"), False)
            kwargs["queryset"] = ProductCategory.objects.all()
            kwargs["form_class"] = MultipleChoiceField
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(ProductType, ProductTypeAdmin)

# Product Category
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status', 'created_at','updated_at')
    fields = ('name', 'products','status')
    def get_products_display(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])
    get_products_display.short_description = 'Product'
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["widget"] = admin.widgets.FilteredSelectMultiple(("Product"), False)
            kwargs["queryset"] = Product.objects.all()
            kwargs["form_class"] = MultipleChoiceField
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(ProductCategory, ProductCategoryAdmin)

# Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['display_image', 'name', 'regular_price', 'selling_price', 'get_category_display', 'sold', 'status']
    form = ProductAdminForm

    def get_category_display(self, obj):
        return obj.category.name
    get_category_display.short_description = 'Category'

    def display_image(self, obj):
        # Create a function to display the image as a thumbnail in the admin list view
        if obj.image:
            return format_html('<img src="{}" style="object-fit:contain;aspect-ratio:2 /3" width="80"  />', str(obj.image.url))
        return ''
    display_image.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        uploaded_images = form.cleaned_data.get('upload_image')
        if uploaded_images:
            if not obj.related_images:
                obj.related_images = ''
            for uploaded_image in uploaded_images:
                # Check if the uploaded file is an image
                if uploaded_image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Save the image to the media folder
                    file_folder = os.path.join('product', uploaded_image.name)
                    image_path = os.path.join(settings.MEDIA_ROOT, file_folder)
                    with open(image_path, 'wb+') as destination:
                        for chunk in uploaded_image.chunks():
                            destination.write(chunk)

                    image = Image.open(image_path)
                    # Resizing to 800x600 pixels
                    image.thumbnail((800, 600))
                    image.save(image_path)
                    obj.related_images += f'{file_folder};' 
        obj.fake_sold = random.randint(200, 66666)
        obj.view = obj.fake_sold + random.randint(100, 99999)
        obj.save()
        super().save_model(request, obj, form, change)
admin.site.register(Product, ProductAdmin)