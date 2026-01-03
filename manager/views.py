from django.shortcuts import render,get_object_or_404,redirect
from .models import*
from django.contrib import messages
from user.models import*

# Create your views here.
def adminhome(request):
     return render(request,'admin/adminhome.html')

def adminviews(request):
    numb = request.GET.get('type')
    orders = None  # default: nothing to show

    if numb == '1':
        orders = ordertb.objects.filter(orderstatus='inprocess')
    elif numb == '2':
        orders = ordertb.objects.filter(orderstatus='pending')
    elif numb == '3':
        orders = ordertb.objects.filter(orderstatus='completed')
    elif numb == '4':
        orders = ordertb.objects.filter(orderstatus='Rejected')
    elif numb == '5':
        orders = ordertb.objects.all()

    context = {'orders': orders}
    return render(request, 'admin/adminview.html', context)


def productadd(request):
     if request.method =='POST':
         name=request.POST['name']
         size=request.POST['size']
         fabric=request.POST['fabric']
         description=request.POST['description']
         listprice=request.POST['listprice']
         price=request.POST['price']
         price50=request.POST['price50']
         price100=request.POST['price100']
         categoryid=request.POST['categoryid']
         if len(request.FILES)>0:
              imge=request.FILES['image']
         else:
              imge='no image'    
         n=product.objects.create(name=name,size=size,description=description,listprice=listprice,price=price,price50=price50,price100=price100,categoryid_id=categoryid,fabric=fabric,image=imge)
         n.save()
         messages.info(request,'product added')
     cate=category.objects.all()
     return render(request,'admin/addproduct.html',{'ca':cate})   



def viewproduct(request):
      n=product.objects.all()
      p={'n':n}
      return render(request,'admin/productshow.html',p) 


def productedit(request,id):
     r=get_object_or_404(product,id=id)
     if request.method == 'POST':
         name=request.POST['name']
         size=request.POST['size']
         description=request.POST['description']
         listprice=request.POST['listprice']
         price=request.POST['price']
         price50=request.POST['price50']
         price100=request.POST['price100']
         categoryid=request.POST['categoryid']
         fabric=request.POST['fabric']
         if 'image' in request.FILES:
            r.image = request.FILES['image']
          
         r.name=name
         r.size=size
         r.fabric=fabric
         r.description=description
         r.listprice=listprice
         r.price=price
         r.price50=price50
         r.price100=price100
         r.categoryid_id=categoryid
     #     r.image=image
         r.save()
         messages.info(request,'updated')
         return redirect('viewproduct')
     cate=category.objects.all()
     n=product.objects.filter(id=id)
     return render(request,'admin/editproduct.html',{'ca':cate,'s':n})

def deleteproduct(request,id):
     product.objects.filter(id=id).delete()
     return redirect('viewproduct')

def adminview(request):
      n=ordertb.objects.all()
      p={'n':n}
      return render(request,'admin/managerview.html',p) 


def deatilesshow(request,id):
    m=ordertb.objects.filter(id=id)
    n=orderitems.objects.filter(order_id=id)
    p={'m':m,'n':n}
    return render(request,'admin/showdetails.html',p) 


def cancel(request,id):
     a=ordertb.objects.filter(id=id).update(orderstatus='Rejected')
     b={'a':a}
     return redirect('adminview')


def shipordr(request):
    if request.method == 'POST':
         carrier=request.POST['carrier']
         tracking=request.POST['tracking']
         shippingdate=request.POST['shippingdate']
         id=request.POST['orderid']
         ordrtb=ordertb.objects.filter(id=id)
         ordrtb.update(carrier=carrier,tracking=tracking,shippingdate=shippingdate,orderstatus='completed')
    return redirect('adminview')

def ordersts(request,id): 
     a=ordertb.objects.filter(id=id).update(orderstatus='inprocess')
     b={'a':a}
     return redirect('adminview')

