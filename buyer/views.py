from django.contrib.auth import login
from django.shortcuts import redirect, render, resolve_url

from seller.models import Product,Category
from ecommerce.models import *


from .models import *
import pymysql

from django.db import connection

from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def category(request,id):

    print(id)
    try:
        cat=Category.objects.all()
        print(id)

        myCursor = connection.cursor()
        myCursor.execute("SELECT * FROM seller_product WHERE seller_product.category_id = '{}'".format(id))
        product=list(myCursor.fetchall())
        
        
        print(product)
        products=[]
        for x in product:
            products.append(Product.objects.get(id=x[0]))
        
        print(products)

        return render(request, "welcomebuyer.html",{'cat':cat,'products':products})
        '''
        

        myCursor.execute("SELECT * FROM seller_product WHERE seller_product.category_id = '{}'".format(id))
        searchData=list(myCursor.fetchall())
            
        #products=[]
        #products.append(Product.objects.get(category_id=id))

        return render(request,"category.html",{'cat':cat,'products':searchData})
        '''
    except:
        cat=Category.objects.all()
        products=Product.objects.all()

        return render(request, "welcomebuyer.html",{'cat':cat,'products':products})
   



def cartDetails(request):
    uobj=userProfile.objects.get(user__username=request.user)
    products=[]

    cartObj=Cart.objects.filter(user_id=uobj.id)
    cartCount=Cart.objects.filter(user_id=uobj.id).count()


    for i in cartObj:
        products.append(Product.objects.get(id=i.product_id))

    print(products)
    

    return render(request,"CartDetails.html",{'products':products,'count':cartCount})

@login_required
def cart(request,id):
    
    pobj=Product.objects.get(id=id)
    uobj=userProfile.objects.get(user__username=request.user)

    try:
        c=Cart(product=pobj,user=uobj)
        c.save()
        messages.success(request,"Product Addedd Successfully")
        return redirect('/buyer/home/')
    except:
        messages.error(request,"Product Already In the Cart")
        return redirect('/buyer/home/')
 

    

@login_required
def home(request):
    cat=Category.objects.all()
    products=Product.objects.all()
    if request.method=='POST':
        
        key=request.POST['search']
        myCursor = connection.cursor()
        myCursor.execute("SELECT * FROM seller_product WHERE seller_product.desc like '%{}%'".format(key))
        searchData=list(myCursor.fetchall())
        p=[]
        for x in searchData:
            p.append(Product.objects.get(name=x[1]))
        
        print(p)



        return render(request,"searchResult.html",{'cat':cat,'products':p})

    uobj=userProfile.objects.get(user__username=request.user)

    cartCount=Cart.objects.filter(user_id=uobj.id).count()

    
    
    return render(request, "welcomebuyer.html",{'cat':cat,'products':products,'count':cartCount})

