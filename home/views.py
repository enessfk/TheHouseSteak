import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.core import serializers
from django.db.models import Q, Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactForm, UserProfile, FAQ
from order.models import ShopCart
from product.models import Product, Category, Images, Comment


def index(request):
    setting=Setting.objects.get()
    sliderdata=Product.objects.all().order_by('-price')[:5]
    specialOffersFastFood=Product.objects.filter(Q(category__title='Burgers') | Q(category__title='Pizzas')).order_by('?')[:1]
    specialOffersChicken=Product.objects.filter(Q(category__title='Chicken')).order_by('?')[:1]
    specialOffersDessert=Product.objects.filter(Q(category__title='Desserts')).order_by('?')[:2]
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    if request.user.id != None:
        profile=UserProfile.objects.get(user_id=current_user.id)
    else:
        profile=None
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    setTotal(request)
    category=Category.objects.all()
    context={'setting':setting,
             'page':'home',
             'category':category,
             'profile':profile,
             'specialOffersFastFood':specialOffersFastFood,
             'specialOffersChicken': specialOffersChicken,
             'specialOffersDessert': specialOffersDessert,
             'sliderdata':sliderdata,
             'shopcart':shopcart
             }
    return render(request,'index.html',context)

def setTotal(request):
    current_user=request.user
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    totalcal = 0
    for rs in shopcart:
        totalcal += rs.product.price * rs.quantity
    ordertotal = round(totalcal, 2)
    if ordertotal > 50 or request.session['cart_items'] == 0:
        delivery = 0
    else:
        delivery = 3.99
    total = round((ordertotal + delivery), 2)
    request.session['total'] = total
    request.session['ordertotal'] = ordertotal
    request.session['delivery'] = delivery
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()


def aboutus(request):
    setting=Setting.objects.get()
    current_user=request.user
    if request.user.id != None:
        profile=UserProfile.objects.get(user_id=current_user.id)
    else:
        profile=None
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    context={'setting':setting, 'page':'aboutus','profile':profile, 'shopcart':shopcart}
    return render(request,'aboutus.html',context)

def references(request):
    setting=Setting.objects.get()
    current_user=request.user
    if request.user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    context={'setting':setting, 'page':'references','profile':profile, 'shopcart':shopcart}
    return render(request,'references.html',context)

def contact(request):
    if request.method =='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,'Your message has been sent.Thank you for your attention.')
            return HttpResponseRedirect('/contact')

    setting=Setting.objects.get()
    current_user=request.user
    if request.user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    form=ContactForm()
    context={'setting':setting,'form':form ,'page':'contact','profile':profile, 'shopcart':shopcart}
    return render(request,'contact.html',context)

def menu(request):
    setting = Setting.objects.get()
    current_user=request.user
    if request.user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    setTotal(request)
    products=Product.objects.all()
    category=Category.objects.all()
    context={'products':products,
             'setting':setting,
             'category':category,
             'page':'menu',
             'profile':profile,
             'shopcart':shopcart}
    return render(request,'menu.html',context)

def product_detail(request,id,slug):
    setting=Setting.objects.get()
    current_user=request.user
    if request.user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    products=Product.objects.get(pk=id)
    images=Images.objects.filter(product_id=id)
    comments=Comment.objects.filter(product_id=id,status="True")
    setTotal(request)
    stars=Comment.objects.filter(product_id=id).aggregate(Avg('rate'))
    context={'product':products,
             'setting':setting,
             'images':images,
             'comments':comments,
             'stars':stars,
             'profile': profile,
             'shopcart': shopcart
            }
    return render(request,'product_detail.html',context)


def product_search(request):
    if request.method =='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            category=Category.objects.all()
            current_user = request.user
            if request.user.id != None:
                profile = UserProfile.objects.get(user_id=current_user.id)
            else:
                profile = None
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            setTotal(request)
            query=form.cleaned_data['query']
            products=Product.objects.filter(title__icontains=query)
            setting=Setting.objects.get()
            context={
                'products':products,
                'category':category,
                'profile': profile,
                'shopcart': shopcart,
                'setting':setting
            }
            return render(request,'product_search.html',context)

    return HttpResponseRedirect('/')

def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    setting=Setting.objects.get()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Login Error! | Username or password is not correct.")
            return HttpResponseRedirect('/login')

    category=Category.objects.all()
    current_user=request.user
    if request.user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    context={
        'category':category,
        'profile': profile,
        'shopcart': shopcart,
        'setting':setting,
    }
    return render(request,'login.html',context)

def signup_view(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/Users/user.png"
            data.save()
            return HttpResponseRedirect('/')

    form=SignUpForm()
    category = Category.objects.all()
    current_user=request.user
    if request.user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
        shopcart=ShopCart.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'form':form,
        'profile': profile,
        'shopcart': shopcart
    }
    return render(request, 'signup.html', context)


def faq(request):
    current_user=request.user
    category=Category.objects.all()
    faq=FAQ.objects.all().order_by('ordernumber')
    setting=Setting.objects.get()
    if request.user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context={
        'faq':faq,
        'category':category,
        'profile':profile,
        'setting':setting
    }
    return render(request,'faq.html',context)