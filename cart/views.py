from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View
from .models import Cart
from products.models import Product
from system.constant import *
from system.function import decode

class CartView(View):
    template_name = 'cart.html'
    
    def get(self, req):
        carts = Cart.get_carts(user_obj= req.user)
        try:
            msg = req.session['create_order_success']
        except Exception:
            msg = None
        if msg:
            del req.session['create_order_success']
        return render(req, self.template_name, {
                'carts': carts,
                'msg':msg
            }
        )
    
    def post(self, req):
        if 'add-to-cart' in req.path:
            post = req.POST
            product_id = str(decode(post.get('product_id')))
            quantity = post.get('amount')
            buynow = int(post.get('buynow'))
            if buynow == 1:
                pr_q = f'{product_id}:{quantity}'
                pr_q_exists = Cart.get_buynow_cart(req.user)
                buynow_cart = get_object_or_404(Cart, user=req.user, status = STATUS_INACTIVE)
                buynow_cart.products_id_and_quantity = pr_q
                buynow_cart.save()
            else:
                pr_q = Cart.get_pr_q(req.user)
                data = ''
                exists = False
                if len(pr_q) > 0:
                    pr_q = pr_q.split(';')
                    for dt in pr_q:
                        if product_id in dt.split(':')[0]:
                            data+=f'{product_id}:{int(quantity)+int(dt.split(":")[1])}'
                            exists = True
                        else:
                            data+=dt
                        if not dt == pr_q[len(pr_q)-1]:
                            data+=';'
                    if not exists:
                        data+=f';{product_id}:{quantity}'
                else:
                    data+=f'{product_id}:{quantity}'
                cart = get_object_or_404(Cart, user = req.user, status = STATUS_ACTIVE)
                cart.products_id_and_quantity = data
                cart.save()
            get_pr_q = Cart.get_pr_q(req.user)
            result = {
                'status': STATUS_ACTIVE,
                'amount_cart': len(get_pr_q.split(';')) if len(get_pr_q)>0 else len(get_pr_q)
            }
            return JsonResponse(result)
    
        elif 'update-cart' in req.path:
            post = req.POST
            product_id = str(decode(post.get('product_id')))
            quantity = post.get('amount')
            pr_q = Cart.get_pr_q(req.user).split(';')
            data = ''
            for dt in pr_q:
                if product_id in dt.split(':')[0]:
                    data+=f'{product_id}:{quantity}'
                else:
                    data+=dt
                if not dt == pr_q[len(pr_q)-1]:
                    data+=';'
            cart = get_object_or_404(Cart, user = req.user, status = STATUS_ACTIVE)
            cart.products_id_and_quantity = data
            cart.save()
            result = {
                'status': STATUS_ACTIVE
            }
            return JsonResponse(result)

        elif 'delete-cart' in req.path:
            post = req.POST
            product_id = str(decode(post.get('product_id')))
            pr_q = Cart.get_pr_q(req.user).split(';')
            data = ''
            for dt in pr_q:
                if product_id in dt.split(':')[0]:
                    continue
                else:
                    data+=dt
                if not dt == pr_q[len(pr_q)-1]:
                    data+=';'
            cart = get_object_or_404(Cart, user = req.user, status = STATUS_ACTIVE)
            cart.products_id_and_quantity = data
            cart.save()
            result = {
                'status': STATUS_ACTIVE,
                'amount_cart': len(data.split(';')) if len(data)>0 else len(data)
            }
            return JsonResponse(result)

        # If none of the conditions are met, return an error response
        error_result = {
            'error': 'Invalid request'
        }
        return JsonResponse(error_result)
