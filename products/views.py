from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import *
from system.constant import *
import json
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
class Shop(View):
    template_name = 'shop.html'

    def get(self, req):
        return render(req, self.template_name, {
            'product_types':ProductType.get_all_product_type()
        })

    def post(self, req):
        if 'api_product_filter' in req.path:
            data = json.loads(req.body)
            category = data.get('cate')
            cursor = data.get('cursor')
            product_type = data.get('type')
            sort = data.get('sort')

            keyword = data.get('search')

            sort_types = {
                '1':'selling_price',
                '2':'-selling_price',
                '3':'-created_at'
            }
            print(keyword)

            if keyword:
                print(keyword)
                # Khởi tạo một Q object trống
                word_conditions = Q()

                # Bẻ nhỏ keyword tạo dsach các điều kiện so sánh ư
                for w in keyword.split(" "):
                    # word_conditions |= Q(name__icontains=str(w))
                    word_conditions &= Q(name__icontains=str(w))
                # Kiểm tra điều kiện lọc
                if sort:
                    products = Product.objects.filter(word_conditions).order_by(sort_types[str(sort)])
                else:
                    products = Product.objects.filter(word_conditions)
            else:
                if sort:
                    products = Product.objects.all().order_by(sort_types[str(sort)])
                else:
                    products = Product.objects.all()

            # if sort:
            #     products.order_by(sort_types[str(sort)])
    
            # for prd in products.values():
            #     print(prd['selling_price'])

            result = {
                'status': STATUS_ACTIVE,
                'products': list(products.values())
            }
            return JsonResponse(result)
        else:
            query = req.POST.get('query')
            return render(req, self.template_name, {
                'product_types':ProductType.get_all_product_type(),
                'query': query
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


