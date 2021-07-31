from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import Setting, UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from product.models import Category, Product


def index(request):
    return HttpResponse("Order")

@login_required(login_url='/login')
def addtocart(request,id):
    url=request.META.get('HTTP_REFERER')
    current_user = request.user
    checkproduct=ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control=1
    else:
        control=0

    if request.method=='POST':
        form=ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
            request.session['cart_items']=ShopCart.objects.filter(user_id=current_user.id).count()
            return HttpResponseRedirect(url)
    else:
        if control==1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items']=ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, 'Product has been added successfully')
        return HttpResponseRedirect(url)

    messages.warning(request,'Product has not been added. An error occured! ')
    return  HttpResponseRedirect(url)


@login_required(login_url='/login')
def deletefromcart(request,id):
    current_user=request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    ShopCart.objects.filter(id=id).delete()
    messages.success(request,'Product has deleted from cart')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login')
def orderproduct(request):
    category=Category.objects.all()
    setting=Setting.objects.get()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)

    totalcal = 0
    for rs in shopcart:
        totalcal += rs.product.price * rs.quantity
    ordertotal = round(totalcal, 2)
    if ordertotal > 50:
        delivery = 0
    else:
        delivery = 3.99
    total = round((ordertotal + delivery), 2)
    request.session['total'] = total
    request.session['ordertotal'] = ordertotal
    request.session['delivery'] = delivery
    if  request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.tableno = form.cleaned_data['tableno']
            data.phone=form.cleaned_data['phone']
            data.user_id=current_user.id
            data.total=total
            data.deliverytime=form.cleaned_data['deliverytime']
            deliverytime=data.deliverytime
            data.ip=request.META.get('REMOTE_ADDR')
            ordercode=get_random_string(5).upper
            data.code=ordercode
            data.save()

            shopcart=ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail=OrderProduct()
                detail.order_id=data.id
                detail.product_id=rs.product_id
                detail.user_id=current_user.id
                detail.quantity=rs.quantity
                product=Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
                detail.price=rs.product.price
                detail.amount=rs.amount
                detail.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items']=0
            request.session['total'] = 0
            request.session['ordertotal'] = 0
            request.session['delivery'] = 0
            messages.success(request,'Your order has been completed.Thank you!')
            return render(request,'completed_checkout.html',{'ordercode':ordercode,'deliverytime':deliverytime,'category':category})
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect("/checkout")
    form=OrderForm()
    profile=UserProfile.objects.get(user_id=current_user.id)
    tablenumber=range(11,21)
    context={
        'profile':profile,
        'shopcart':shopcart,
        'category':category,
        'total':total,
        'ordertotal': ordertotal,
        'setting': setting,
        'delivery': delivery,
        'form':form,
        'tableno': tablenumber
    }
    return render(request,'checkout.html',context)




