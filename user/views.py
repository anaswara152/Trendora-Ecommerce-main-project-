from django.shortcuts import render,redirect,get_object_or_404
from .models import*
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,get_user_model
from manager.models import *
import stripe
import datetime
from django.views.generic import TemplateView
from django.conf import settings
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'common/home.html')


def registration(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        # phone=request.POST['phone']
        email=request.POST['email']
        address=request.POST['address']
        city=request.POST['city']
        postalcode=request.POST['postalcode']
        state=request.POST['state']
        password=request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.info(request,'email existing')
            return render(request,'user/register.html')
        elif User.objects.filter(username=email).exists():
             messages.info(request,'email not existing')
             return render(request,'user/register.html')
        else:
            user=User.objects.create_user(username=username, first_name= first_name,last_name=last_name,email=email,password=password)
            user.save()
            customer=reg(user=user,address=address,city=city,state=state,postalcode=postalcode)
            customer.save()
            customer_obj,created=Group.objects.get_or_create(name="CUSTOMER")
            customer_obj.user_set.add(user)
            return render(request,'common/login.html')

    return render(request,'user/register.html')


def userhome(request):
    products = product.objects.all()

    if request.user.is_authenticated:
        # Use request.user directly (User instance)
        wishlist_items = whislist.objects.filter(customerid=request.user).values_list('productid_id', flat=True)
        cart_items=cart.objects.filter(customerid_id=request.user.id).values_list('productid_id',flat=True)
    else:
        wishlist_items = []

    return render(request, 'user/userhome.html', {'p': {'m': products}, 'wishlist_items': wishlist_items,'c':cart_items})

def login_user(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="CUSTOMER").exists():
            return redirect('userhome')
        else:
            return redirect('adminhome')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate using username (if you want email, need custom backend)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name="CUSTOMER").exists():
                return redirect('userhome')
            else:
                return redirect('adminhome')
        else:
            messages.error(request, 'User credentials are not correct')

    return render(request, 'common/login.html')
def logoutuser(request):
     if request.user.is_authenticated:
           request.session.flush()
     return redirect('home')


def deatiles(request,id):
    m=product.objects.filter(id=id)
    p={'m':m}
    return render(request,'user/showdetails.html',p) 



def addcart(request):
    if request.user.is_authenticated:
        id=request.POST['productid']
        productid=product.objects.get(id=id)
        print(productid.id)
        customerid=request.user.id
        print(customerid)
        count=int(request.POST['count'])
        print(count)
        if count<50:
            price=productid.price
            print(price)
        elif count<100:
            price=productid.price50
            print(price)
        else:
            price=productid.price100
            print(price)
     
        n=cart(customerid_id=customerid,productid_id=productid.id,count=count,price=price)
        n.save()
    return redirect('userhome')


def viewcart(request):
    id=request.user.id
    cart_obj=cart.objects.filter(customerid_id=id)
    grand=0
    for c in cart_obj:
        total=(c.count)*(c.price)
        grand=grand+total
    p={'n':cart_obj,'gr':grand}
    return render(request,'user/viewcart.html',p)

def trash(request,id):
    productid=cart.objects.filter(id=id)
    customerid=request.user.id
    number=productid[0].count
    if number==0:
        messages.info('blank')
        return redirect('viewcart')
    else:
        quantity=number-1
        p=productid.update(count=quantity)
        return redirect('viewcart')
    
def addproduct(request,id):
    productid=cart.objects.filter(id=id)
    customerid=request.user.id
    num=productid[0].count
    if num==0:
        messages.info(request,'blank')
        return redirect('viewcart')
    else:
        qunt=num+1
        k=productid.update(count=qunt)
        return redirect('viewcart')
    
def deletecart(request,id): 
    m=cart.objects.filter(id=id).delete()
    return redirect('viewcart')    



def summary(request):
    id=request.user.id
    carttb=cart.objects.filter(customerid_id=id)
    cid=carttb[0].customerid
    v=reg.objects.filter(user_id=cid)
    grand=0
    for c in carttb:
        total=(c.count)*(c.price)
        grand=grand+total
    p={'v':v ,'n':carttb,'gr':grand}
    return render(request,'user/summary.html',p)


def viewprofile(request):
    if not request.user.is_authenticated:
        # redirect to login if user is not logged in
        return redirect('login')

    # Get the profile for the logged-in user
    s = get_object_or_404(reg, user=request.user)
    return render(request,'user/viewprofile.html',{'s':s})



def edit_profile(request, id):
    profile = get_object_or_404(reg, id=id)  # Get the user's profile
    user = profile.user  # Associated User object

    if request.method == 'POST':
        # Get data from form
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postalcode = request.POST.get('postalcode')

        # Update User object
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Update reg profile object
        profile.address = address
        profile.city = city
        profile.state = state
        profile.postalcode = postalcode
        profile.save()

        return redirect('viewprofile')  # Redirect back to view profile page

    return render(request, 'user/editprofile.html', {'profile': profile})



def addwhis(request, id):
    if not request.user.is_authenticated:
        return redirect('loginuser')

    # Get the product instance
    product_instance = get_object_or_404(product, id=id)

    # Check if already exists in wishlist
    exists = whislist.objects.filter(productid=product_instance, customerid=request.user).exists()

    if not exists:
        whislist.objects.create(productid=product_instance, customerid=request.user)
        messages.success(request, "Item added to your wishlist ❤️")
    else:
        messages.info(request, "This item is already in your wishlist 💖")

    return redirect('userhome')


def toggle_wishlist(request, id):
    # Get product
    product_instance = get_object_or_404(product, id=id)

    # Get logged-in user
    user = request.user

    # Check if already in wishlist
    wishlist_item = whislist.objects.filter(productid=product_instance, customerid=user)

    if wishlist_item.exists():
        # Remove from wishlist
        wishlist_item.delete()
    else:
        # Add to wishlist
        whislist.objects.create(productid=product_instance, customerid=user)

    return redirect('userhome')



def viewwish(request):
    id=request.user.id
    wish_obj=whislist.objects.filter(customerid_id=id)
 
    return render(request,'user/viewish.html',{'w':wish_obj})


def checkout(request):
    if request.method == "POST":
        name=request.POST.get('name')
        phone=request.POST['phone']
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state') 
        email=request.POST.get('email')
        orderdate=datetime.datetime.now()
        id=request.user.id
        ordertotal=request.POST.get('grandtotal')  
        ordr=ordertb.objects.create(name=name,phone=phone,address=address,city=city,state=state,email=email,orderdate=orderdate,ordertotal=ordertotal,customerid_id=id)
        ordr.save() 
        cid=request.user.id
        cartta=cart.objects.filter(customerid_id=cid)
        for k in cartta:
            total=k.price
            count=k.count
            productid=k.productid.id
            order=ordr.id      
            item=orderitems(total=total,count=count,productid_id=productid,order_id=order)
            item.save()
            messages.info(request,'order confirmed')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        else:
            domain = request.build_absolute_uri('/')  # For production

        user_id = request.user.id
        products = cart.objects.filter(customerid_id=user_id)

        if not products.exists():
            return render(request, 'user/empty_cart.html')  # Handle empty cart case

        line_items = []
        for item in products:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.productid.name,
                        'description': item.productid.description,
                    },
                    'unit_amount': int(item.productid.price * 100),  # Convert dollars to cents
                },
                'quantity': item.count,
            })

        # Create the Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=domain + '/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain + '/cancel/',
            metadata={'orderid':ordr.id}

        )
        cartta.delete()
        return redirect(checkout_session.url, code=303)

  

class SuccessView(TemplateView):
    template_name = "user/sucess.html"
    def get(self,request,*args,**kwargs):
        session_id=request.GET.get('session_id')
        if not session_id:
            return HttpResponse('session id is missing',status=400)
        try:
             session=stripe.checkout.Session.retrieve(session_id)
             print(session)
             if session.payment_status =="paid":
                 order_id=session.metadata.get('orderid')
                 order=get_object_or_404(ordertb,id=order_id)
                 order.paymentstatus="paid"
                 order.transactionid=session_id
                 order.paymentdate=datetime.datetime.now()
                 order.save()
        except stripe.error.StripeError as e:
           return HttpResponse(f"Stripe error: {str(e)}", status=500)         
        return super().get(request,*args,**kwargs)


class CancelView(TemplateView):
   template_name="user/cancel.html"








def search(request):
     prodct=request.GET.get('name')
     if prodct:
          n=product.objects.filter(title__icontains=prodct)
     else:
          n=product.objects.all()
     books=product.objects.all()     
     return render(request,'user/userhome.html',{'n':n},{'books':books}) 

