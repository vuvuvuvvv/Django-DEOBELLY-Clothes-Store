from django.shortcuts import redirect, render
from cart.models import Cart
from products.models import Product
from order.forms import OrderForm
from core.models import GeoLocation
# Create your views here.
from django.views import View

class CheckoutView(View):
    template_name = 'checkout.html'

    def get(self, req):
        cart = Cart.get_carts(user_obj= req.user)

        return render(req, self.template_name, {
                'form': OrderForm(),
                'cart': cart
            }
        )
    
    def post(self, req):
        form = OrderForm(req.POST) 
        if form.is_valid():
            data = req.POST
            get_pr_q = Cart.get_pr_q(req.user)
            total_payment = 0
            for val in get_pr_q.split(';'):
                product = Product.get_product_by_id(int(val.split(':')[0]))
                total_price = product.selling_price*int(val.split(':')[1])
                total_payment += total_price
            user = req.user
            order_instance = form.save(commit=False) 
            order_instance.user = user 
            order_instance.address = f"{data['specific_address']}, {GeoLocation.get_name_location_by_id(data['wards'])}, {GeoLocation.get_name_location_by_id(data['district'])}, {GeoLocation.get_name_location_by_id(data['provinve'])}"
            order_instance.total_price = total_payment
            order_instance.products_id_and_quantity = get_pr_q
            order_instance.save()
            cart = Cart.objects.get(user = req.user)
            cart.delete()
            return redirect('cart')
        else:
            return render(req, self.template_name, {'form': form})