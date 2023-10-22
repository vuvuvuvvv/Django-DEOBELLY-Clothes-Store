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
            categories = data.get('cate')
            cursor = data.get('cursor')
            product_type = data.get('type')
            sort = data.get('sort')
            # print(categories)
            keyword = data.get('search')

            sort_types = {
                '1':'selling_price',
                '2':'-selling_price',
                '3':'-created_at'
            }
            
            # Tạo query set sản phẩm:
            products = Product.objects
            
            if keyword:
                # Query theo kyword
                # Khởi tạo một Q object trống
                word_conditions = Q()

                # Bẻ nhỏ keyword tạo dsach các điều kiện so sánh
                for w in keyword.split(" "):
                    # word_conditions |= Q(name__icontains=str(w))
                    word_conditions &= Q(name__icontains=str(w))
                # Kiểm tra điều kiện lọc
                products = products.filter(word_conditions).filter(status = STATUS_ACTIVE)

            # Check theo loại sản phẩm
            if product_type:
                #Lấy ra danh mục theo loại sản phẩm
                get_all_categories = ProductType.objects.get(slug = product_type).categories.all()
                if get_all_categories:
                    cate_conditions = Q()
                    for cate in get_all_categories:
                        if cate:
                            cate_conditions |= Q(category=cate)
                    # Kiểm tra điều kiện lọc
                    products = products.filter(cate_conditions)
                else:
                    products = None
            if categories:
                cate_conditions = Q()
                for cate in categories:
                    if cate:
                        cate_conditions |= Q(category=ProductCategory.get_category_by_slug(cate))
                    # Kiểm tra điều kiện lọc
                products = products.filter(cate_conditions)
            if products:
                # Check kèm danh mục sản phẩm
                if sort:
                    products = products.order_by(sort_types[str(sort)])
                # Return list
                products = list(products.values())
                if not cursor:
                    cursor = 0
                start = cursor*PRODUCT_PER_PAGE
                amount = len(products)
                end = (cursor+1)*PRODUCT_PER_PAGE if amount > (cursor+1)*PRODUCT_PER_PAGE else amount

                #Pagination
                products = products[start:end]
                result = {
                    'status': STATUS_ACTIVE,
                    'products': products,
                    'amount':amount
                }
            else:
                result = {
                    'status': STATUS_INACTIVE
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


