from django.db import models
from accounts.models import User
from system.constant import *
# Create your models here.
class GeoLocation(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    parent = models.IntegerField()
    status = models.IntegerField(default=STATUS_ACTIVE, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_location_by_parent_id(cls, id):
        return cls.objects.filter(parent=id, status=STATUS_ACTIVE).order_by('name').values()
    
    @classmethod
    def get_name_location_by_id(cls, id):
        return cls.objects.get(pk = id).name
    
class Contact(models.Model):
    name = models.CharField(max_length=255,null=False)
    email = models.EmailField(null=False)
    tel = models.IntegerField(null=False)
    content = models.TextField(null=False)
    status = models.IntegerField(default=STATUS_ACTIVE, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class TermsAndServices(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(null=False)
    status = models.IntegerField(default=STATUS_ACTIVE, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

