from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import *
from system.constant import *
import json
from django.http import JsonResponse
# Create your views here.
class Shop(View):
    template_name = 'shop.html'

    def get(self, req):
        return render(req, self.template_name, {
            'product_types':ProductType.get_all_product_type()
        })
    
class ProductDetail(View):
    template_name = 'detail.html'

    def get(self, req):
        slug = req.GET['slug']
        product = Product.get_product_by_slug(slug)
        best_selling_product = Product.get_best_selling_related_product_by_cate_slug(product.category.slug)
        promotion_product = Product.get_promotion_related_product_by_cate_slug(product.category.slug)
        related_product = {
            'bán chạy nhất':best_selling_product,
            'Đang khuyến mại':promotion_product
        }
        
        return render(req, self.template_name, {
            'product': product,
            'related_product' : related_product
        })


def product_filter_ajax(req):
    if req.method == 'POST':
        result = {
            'status': STATUS_ACTIVE,
            'products': list(Product.objects.all().values())
        }
        return JsonResponse(result)
    
