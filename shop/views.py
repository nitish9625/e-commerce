from django.http import response
from django.shortcuts import render, HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.
def index(request):
    # products= Product.objects.all()
    # n= len(products)
    # nSlides= n//4 + ceil((n/4) + (n//4))
    # allprod = [[products, range(1, nSlides), nSlides],[products, range(1, nSlides), nSlides]]
    # params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'product': products}
    allprod = []
    catprods= Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n= len(prod)
        nSlides= n//4 + ceil((n/4) + (n//4))
        allprod.append([prod,range(1, nSlides,), nSlides])
    params = {
        'allprod':allprod
    }
    return render(request,"shop/index.html", params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method=='POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        textarea = request.POST.get('textarea', '')
        contact = Contact(name=name, email=email, phone=phone, textarea=textarea)
        contact.save()
        thank = True
    return render(request,'shop/contact.html', {'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')


def productview(request, id):
    # fetch the product using the id
    product = Product.objects.filter(id=id)
    return render(request, 'shop/productview.html', {'product': product[0]})

def checkout(request):
    if request.method=='POST':
        items_json = request.POST.get('itemsjson', '')
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname','')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json,fname=fname, lname = lname, email=email, phone=phone, address=address, city=city, state=state, zip_code=zip_code,)
        print(fname, lname, email, address, city, state, zip_code, phone)
        order.save()
        update = OrderUpdate(order_id = order.order_id, update_desc = "The order has been palced")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html')


