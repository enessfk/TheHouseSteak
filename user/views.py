from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
#from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from home.models import UserProfile, Setting
from home.views import setTotal
from order.models import ShopCart, Order, OrderProduct
from product.models import CommentForm, Comment, Category
from user.forms import UserUpdateForm, ProfileUpdateForm, PasswordChangeForm

@login_required(login_url='/login')
def index(request):
    category=Category.objects.all()
    current_user=request.user
    profiles=UserProfile.objects.filter(user_id=current_user.id)
    profileImage=UserProfile.objects.get(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get()
    setTotal(request)
    context={
        'category':category,
        'profiles':profiles,
        'shopcart':shopcart,
        'profile':profileImage,
        'setting':setting
    }
    return render(request,'user_profile.html',context)

def user_update(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your acoount has been updated')
            return redirect('/user')
    else:
        category=Category.objects.all()
        current_user=request.user
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.userprofile)
        profiles = UserProfile.objects.filter(user_id=current_user.id)
        profileImage = UserProfile.objects.get(user_id=current_user.id)
        setting=Setting.objects.all()
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        context={
            'category':category,
            'user_form': user_form,
            'profile_form': profile_form,
            'profiles':profiles,
            'profile':profileImage,
            'shopcart':shopcart,
            'setting':setting
        }
        return render(request,'user_update.html',context)

def change_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Your password has been changed succesfuly')
            return redirect('/user')
        else:
            messages.error(request,'Please correct the error below. <br>'+str(form.errors))
            return redirect('/user/password')
    else:
        current_user=request.user
        category=Category.objects.all()
        form=PasswordChangeForm(request.user)
        profile = UserProfile.objects.get(user_id=current_user.id)
        setting=Setting.objects.all()
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        context={
            'category':category,
            'form':form,
            'profile':profile,
            'shopcart':shopcart,
            'setting':setting
        }
        return render(request, 'change_password.html',context)

@login_required(login_url='/login')
def orders(request):
    current_user = request.user
    category=Category.objects.all()
    orders=Order.objects.filter(user_id=current_user)
    profile = UserProfile.objects.get(user_id=current_user.id)
    setting = Setting.objects.get()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    context={
        'category':category,
        'orders':orders,
        'profile':profile,
        'shopcart':shopcart,
        'setting':setting
    }
    return render(request,'user_orders.html',context)

@login_required(login_url='/login')
def orderdetail(request,id):
    current_user = request.user
    category = Category.objects.all()
    order = Order.objects.get(user_id=current_user,id=id)
    orderitems=OrderProduct.objects.filter(order_id=id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    setting = Setting.objects.get()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'orderitems':orderitems,
        'profile': profile,
        'shopcart': shopcart,
        'setting':setting
    }
    return render(request, 'user_order_detail.html', context)


def comments(request):
    current_user = request.user
    category = Category.objects.all()
    comments = Comment.objects.filter(user_id=current_user)
    profile = UserProfile.objects.get(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get()
    context = {
        'category': category,
        'comments': comments,
        'profile': profile,
        'shopcart': shopcart,
        'setting':setting
    }
    return render(request,'user_comments.html',context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user=request.user
    Comment.objects.filter(id=id,user_id=current_user.id).delete()
    messages.error(request,'Comment has been deleted.')
    return HttpResponseRedirect('/user/comments')