from django.shortcuts import *
from .models import *
from ecommerce.views import *
from ecommerce.models import *


from django.db import connection
from django.db import *
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .forms import *
import pymysql
'''
from .models import userProfile
from django.db import connection
from django.db import *
from django.contrib.auth.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
'''

@login_required
def category(request,id):

    uobj=userProfile.objects.get(username=request.user)
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

        return render(request, "welcomeseller.html",{'uobj':uobj,'cat':cat,'products':products})
    except:
        cat=Category.objects.all()
        products=Product.objects.all()

        return render(request, "welcomeseller.html",{'uobj':uobj,'cat':cat,'products':products})


@login_required

# User profile update n all
@login_required
def profile(request):
    uobj=userProfile.objects.get(user__username=request.user)

    
    addressObj=AddressDetails.objects.filter(user_id=uobj.id)
    print(" Is that Exist : ",addressObj)
    return render(request,"profile.html", {'uobj':uobj,'Address':addressObj })



@login_required
def home(request):
    uobj=userProfile.objects.get(username=request.user)
   
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



    return render(request, "welcomeseller.html",{'uobj':uobj,'cat':cat,'products':products})
       


    return render(request,"welcomeseller.html",{'cat':cat,'products':products})

@login_required
def add_product(request):
    categories = Category.objects.all()
    # JUST RETRIVING DATA
    for x in categories:
        print(x.catname)

    if request.method=="POST":
        try:
            key=request.POST['search']
            myCursor = connection.cursor()
            myCursor.execute("SELECT * FROM seller_product WHERE seller_product.desc like '%{}%'".format(key))
            searchData=list(myCursor.fetchall())
            p=[]
            for x in searchData:
                p.append(Product.objects.get(name=x[1]))
            
            print(p)

            
            return render(request,"searchResult.html",{'cat':cat,'products':p})
        except:
            pass


   
        name = request.POST["name"]
        desc = request.POST["desc"]
        price = request.POST["price"]
        qty = request.POST["qty"]
        catname = request.POST["cat"]
        img = request.FILES['img']
        dated = datetime.now()
        cobj = Category.objects.get(catname=catname)
        uobj = userProfile.objects.get(user__username=request.user)
        product=Product(name=name,desc=desc,price=price,qty=qty,pro_img=img,category=cobj,addedd_by=uobj)
        product.save()

        return redirect("/seller/product_addedd")


    cat=Category.objects.all()
    products=Product.objects.all()

        

    return render(request,"add_product.html",{'cat':cat,'products':products})


    #return render(request,"add_product.html",{'categories':categories})

# Create your views here.
    '''
    if request.method=="POST":
        form=addProductForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            print("Data Validated ")
            form.save()
            return render(request,"<h1> Submitted </h1>")
        
    '''

@login_required
def product_addedd(request):
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
    

    return render(request,"product_addedd.html",{'cat':cat,'products':products})
