from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home1)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['shop']=uname
                return redirect(shop_home1)
            else:
                login(req,data)
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req,"Invalid username or password")
            return redirect(shop_login)
    else:
        return render(req,'login.html')
    

# def shop_login(req):
#     if 'shop' in req.session:
#         return redirect(shop_home1)
#     else:

#         if req.method=='POST':
#             uname=req.POST['uname']
#             password=req.POST['password']
#             data=authenticate(username=uname,password=password)
#             if data:
#                 login(req,data)
#                 req.session['shop']=uname
#                 return redirect(shop_home1)
#         return render(req,'login.html')

def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)

# .....................................admin.............................

    
def shop_home1(req):
    if 'shop' in req.session:
        product=Product.objects.all()
        return render(req,'shop/shop_home.html',{'products':product})
    else:
        return redirect(shop_login)


def add_product(req):
    if req.method=='POST':
        id=req.POST['pro_id']
        name=req.POST['name']
        discription=req.POST['discription']
        price=req.POST['price']
        offer_price=req.POST['o_price']
        file=req.FILES['img']
        data=Product.objects.create(product_id=id,product_name=name,price=price,offer_price=offer_price,img=file,dis=discription)
        data.save()
        return redirect(shop_home1)
    return render(req,'shop/add_product.html')


def edit_product(req,id):
    pro=Product.objects.get(pk=id)
    if req.method=='POST':
        e_id=req.POST['pro_id']
        name=req.POST['name']
        discription=req.POST['discription']
        price=req.POST['price']
        offer_price=req.POST['o_price']
        file=req.FILES.get('img')
        if file:
            Product.objects.filter(pk=id).update(product_id=e_id,product_name=name,price=price,offer_price=offer_price,img=file,dis=discription)
        else:
            Product.objects.filter(pk=id).update(product_id=e_id,product_name=name,price=price,offer_price=offer_price,dis=discription)
        return redirect(shop_home1)
    return render(req,'shop/edit_product.html',{'data':pro})

def delete_product(req,id):
    data=Product.objects.get(pk=id)
    url=data.img.url
    url=url.split('/')[-1]
    os.remove('media/'+url)
    data.delete()
    return redirect(shop_home1)



# ................................user......................................

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"Email Exists")
            return redirect(register)
    else:
        return render(req,'user/register.html')

def user_home(req):
    # if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/user_home.html',{'data':data})
    # else:
        # return redirect(shop_login)

def view_product(req,pid):
    data=Product.objects.get(pk=pid)
    return render(req,'user/view_product.html',{'data':data})


# def add_to_cart(req,pid):
#     product=Product.objects.get(pk=pid)
#     user=User.objects.get(username=req.session['user'])
#     data=Cart.objects.create(user=user,product=product)
#     data.save()
#     return redirect(view_cart)

def add_to_cart(req,pid):
    product = Product.objects.get(pk=pid)
    user = User.objects.get(username=req.session['user'])
    data = Cart.objects.create(user=user,product=product)
    data.save()
    return redirect(view_cart)

# def add_to_cart(req,id):
#     Product=produ.objects.get(pk=id)
#      print(Product)
#      user=User.objects.get(username=req.session['user'])
#      print(user)
#      data=Cart.objects.create(user=user,cake=Product)
#      data.save()
#      return redirect(cart_display)



def view_cart(req):
    return render(req,'user/cart_display.html')

