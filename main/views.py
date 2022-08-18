from audioop import reverse
from ctypes import create_unicode_buffer
import email
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db.models import Sum
from .models import pub,produit,cart_product,category,wishlist,command,pack,comments,comments_pack,command_packs
def index(request):
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    category_formation=category.objects.get(category_name='formation')
    category_service=category.objects.get(category_name='service')
    context={
        'pubs':pub.objects.all(),
        'produits':produit.objects.all(),
        'categories':category.objects.all(),
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count(),
        'packs':pack.objects.all(),
        'formations':produit.objects.filter(category_name=category_formation),
        'services':produit.objects.filter(category_name=category_service)
    }
    return render(request,'index.html',context)
def product(request,id):
    current_product=produit.objects.get(id=id)
    all_product=produit.objects.all()
    other_product=[]
    
    for i in all_product:
        if(i.id !=current_product.id):
            other_product.append(i)
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    context={
        'cart':cart_product.objects.filter(user=request.user),
        'product':current_product,
        'other_product':other_product,
        'minicart':prix,
        'categories':category.objects.all(),
        'number_shopping':cart_product.objects.filter(user=request.user).count(),
        'comments':comments.objects.filter(produit=current_product),
        'variable':0
    }
    return render(request,'single-product-tab-style-left.html',context)
def signin(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        login_user=auth.authenticate(request,username=username,password=password)
        if login_user is not None:
            auth.login(request,login_user)
            return redirect('/home/')
        else :
            messages.info(request,"le nom ou le mot de pass est faux ! resseyer")
            return redirect('/signin/')
        
    return render(request,'login-register.html')
def signup(request):
    if request.method == 'POST':
        username=request.POST.get('first')
        lastname=request.POST.get('last')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password2=request.POST.get('confirme')
        if User.objects.filter(email=email).exists():
            messages.info(request,'cette boite mail est deja utilisé !')
            return redirect('/')
        elif(password != password2):
            messages.info(request,'vous devez confimer votre mot de pass correctement')
            return redirect('/')
        else:
            new_user=User.objects.create(email=email,password=password,username=username)
            new_user.is_active = True
            new_user.set_password(password)
            new_user.save()
            return redirect('/')
    return render(request,'login-register.html')
def add_to_wishlist(request,id):
    existing_product=wishlist.objects.filter(id=id,user=request.user).first()
    if wishlist.objects.filter(id=id,user=request.user).exists() :
        return redirect(request.META['HTTP_REFERER'])
    else:
        add_produit=produit.objects.get(id=id)
        new_wishlist=wishlist.objects.create(user=request.user,produit=add_produit)
        new_wishlist.save()
    context={
       'wishlist':wishlist.objects.filter(user=request.user)
    }
    return render(request,'wishlist.html',context)
def shopping_cart(request):
    
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity 
    context={
        'categories':category.objects.all(),
        'total':prix,
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count()
    }
    return render(request,'shopping-cart.html',context)
def search(request,id):
    category_needed=category.objects.get(id=id)
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    context={
        'categories':category.objects.all(),
        'product_incategory':produit.objects.filter(category_name=category_needed),
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count()
    }
    return render(request,'search.html',context)
def logout(request):
    auth.logout(request)
    return redirect('/signup/')
def add_to_cart(request,id):
    product=produit.objects.get(id=id)
    find_product=cart_product.objects.filter(produit=product,user=request.user).first()
    if  request.method=="POST":
        quantity=request.POST.get('quantity')
        if find_product is not None:
            find_product.quantity=find_product.quantity + int(quantity)
            find_product.save()
            return redirect(request.META['HTTP_REFERER'])
        else :
            new_product_in_cart=cart_product.objects.create(produit=product,user=request.user,quantity=quantity)
            new_product_in_cart.save()
            return redirect(request.META['HTTP_REFERER'])
    if find_product is not None:
        find_product.quantity=find_product.quantity + 1
        find_product.save()
        return redirect(request.META['HTTP_REFERER'])
    else :
        new_product_in_cart=cart_product.objects.create(produit=product,user=request.user)
        new_product_in_cart.save()
        return redirect(request.META['HTTP_REFERER'])
def remove_wishlist_item(request,id):
    remove_product=wishlist.objects.get(id=id)
    remove_product.delete()
    return redirect('/wishliste/')
def remove_shoppingcart_item(request,id):
    remove_product=cart_product.objects.get(id=id)
    remove_product.delete()
    return redirect(request.META['HTTP_REFERER'])
def wishliste(request):
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    context={
        'categories':category.objects.all(),
        'wishlist':wishlist.objects.filter(user=request.user),
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count()
    }
    return render(request,'wishlist.html',context)
def search_product(request):
    if request.method=='POST':
        searching=request.POST.get('searching')
        cate=request.POST.get('selected')
        product_incategory=[]
        
        prix=0
        for i in cart_product.objects.all():
            if(i.user == request.user):
                prix+=i.produit.prix*i.quantity
        if bool(searching) != False :
            product_same_name=produit.objects.filter(nom_produit=searching)
            if cate =='0':
                product_incategory.extend(product_same_name)
            else :
                for i in product_same_name:
                    if i.category_name.category_name == cate:
                        product_incategory.append(i)
        else :
            if cate =='0':
               for i in produit.objects.all():
                    if i.category_name :
                        product_incategory.append(i)
            else :
                for i in produit.objects.all():
                    if i.category_name == cate :
                        product_incategory.append(i)
        context={
            'categories':category.objects.all(),
            'product_incategory':product_incategory,
            'cart':cart_product.objects.filter(user=request.user),
            'minicart':prix,
            'number_shopping':cart_product.objects.filter(user=request.user).count()
        }
        return render(request,'search.html',context)
def confirme(request):
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    if request.method == 'POST':
        fullname=request.POST.get('customerName')
        email =request.POST.get('customerEmail')
        phone_number=request.POST.get('customerNumber')
        address=request.POST.get('customerAddress')
        Subject=request.POST.get('contactSubject')
        cart=cart_product.objects.filter(user=request.user).first()
        new_order=command.objects.create(user=request.user,cart=cart,full_name=fullname,email=email,phone_number=phone_number,address=address)
        
        new_order.save()
    context={
        'categories':category.objects.all(),
        'wishlist':wishlist.objects.filter(user=request.user),
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count()
    }
    return render(request,'confirme.html',context)
def packs(request,id):
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    pack_searched=pack.objects.get(id=id)
    other_pack=[]
    for y in pack.objects.all():
        if y.nom_pack!=pack_searched.nom_pack:
            other_pack.append(y)
    context={
        'categories':category.objects.all(),
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count(),
        'current':pack_searched,
        'comments':comments_pack.objects.filter(pack=id),
        'other_pack':other_pack
    }
    return render(request,'pack.html',context)  
def formations(request):
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    formation_category=category.objects.get(category_name='formation')
    context={
        'categories':category.objects.all(),
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count(),
        'all_formation':produit.objects.filter(category_name=formation_category),
    }
    return render(request,'formation.html',context)
def services(request):
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    services_category=category.objects.get(category_name='service')
    context={
        'categories':category.objects.all(),
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count(),
        'all_services':produit.objects.filter(category_name=services_category),
    }
    return render(request,'services.html',context)
def add_comment_pack(request,id):
    current_pack=pack.objects.get(id=id)
    comment=request.GET.get('comment')
    rating=request.GET.get('selected')
    
    new_comment=comments_pack.objects.create(pack=current_pack,username=request.user.username,comment_text=comment,stars=rating)
    new_comment.save()
    return redirect(request.META['HTTP_REFERER'])
def add_comment(request,id):
    current_product=produit.objects.get(id=id)
    comment=request.GET.get('comment')
    rating=request.GET.get('selected')
    new_comment=comments.objects.create(produit=current_product,username=request.user.username,comment_text=comment,stars=rating)
    new_comment.save()
    return redirect(request.META['HTTP_REFERER'])
def handel_not_found(request,exception):
    return render(request,'404.html')
def confirme_packs(request,id):
    prix=0
    for i in cart_product.objects.all():
        if(i.user == request.user):
            prix+=i.produit.prix*i.quantity
    if request.method == 'POST':
        fullname=request.POST.get('customerName')
        email =request.POST.get('customerEmail')
        phone_number=request.POST.get('customerNumber')
        address=request.POST.get('customerAddress')
        Subject=request.POST.get('contactSubject')
        packs=pack.objects.get(id=id)
        new_order=command_packs.objects.create(user=request.user,pack=packs,full_name=fullname,email=email,phone_number=phone_number,address=address)
        new_order.save()
    context={
        'categories':category.objects.all(),
        'wishlist':wishlist.objects.filter(user=request.user),
        'cart':cart_product.objects.filter(user=request.user),
        'minicart':prix,
        'number_shopping':cart_product.objects.filter(user=request.user).count(),
        'id':id
    }
    return render(request,'confirme_pack.html',context)