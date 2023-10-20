from django.shortcuts import render, redirect

from django.http import JsonResponse

def test(req):
    return render(req,'test.html',{})

# Create your views here.
def test_api_ajax(req):
    if req.method == "POST":
        return JsonResponse({
            'message': 'oke'
        })
    else:
        return redirect('home')