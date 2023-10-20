from django.shortcuts import render
from core.models import TermsAndServices, GeoLocation
from core.forms import ContactForm
from system.constant import *
from django.views import View
from django.http import JsonResponse

def index(req):
    return render(req,'index.html',{})

def terms(req):
    terms = TermsAndServices.objects.filter(status = STATUS_ACTIVE).all().values()
    return render(req, 'terms_and_services.html',{
        'terms':terms
    })

def our_stories(req):
    return render(req, 'introduction.html',{
    })

class ContactView(View):
    template_name = 'contact.html'

    def get(self, req):
        form = ContactForm() 
        return render(req, self.template_name, {'form': form})

    def post(self, req):
        form = ContactForm(req.POST) 
        if form.is_valid():
            if req.user.is_authenticated:
                user = req.user
                contact_instance = form.save(commit=False) 
                contact_instance.user = user 
                contact_instance.save()
            else: 
                form.save()
            
            return render(req, self.template_name, {
                'form': form,
                'success': True
            })
        else:
            return render(req, self.template_name, {'form': form})
        
def get_geolocation(req):
    if req.method == 'POST':
        parent_id = req.POST.get('parent_id')
        location = GeoLocation.get_location_by_parent_id(parent_id)
        result = {
            'status': STATUS_ACTIVE,
            'location': list(location)
        }
        return JsonResponse(result)