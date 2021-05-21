from django.contrib.auth import login
from django.shortcuts import redirect, render, resolve_url

from seller.models import Product,Category
from ecommerce.models import *
from datetime import date,datetime

from .models import *
import pymysql

from django.db import connection

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def Order_by_id(request,id):
    uobj=userProfile.objects.get(user__username=request.user)
    
    oid=orders.objects.get(id=id)
    ProductOrders=OrderProduct.objects.filter(order_id=id)
    Products=[]
    for x in ProductOrders:
        Products.append(Product.objects.get(id=x.product_id))

    address=AddressDetails.objects.get(id=oid.Address_id)
    return render(request,"invoice.html",{'order_id':oid.order_id,'products':Products,'address':address,'grandTotal':oid.total_amt,'uobj':uobj})

@login_required
def orderDetails(request):
    uobj=userProfile.objects.get(user__username=request.user)
    order=orders.objects.filter(placed_by=uobj.id)

    print(order)

    return render(request,"order.html",{'order':order})

@login_required
def checkout(request):
    pqty=request.POST.getlist('pqty')
    price=request.POST.getlist('price')
    pid=request.POST.getlist('pid')
    

    address_id=request.POST['address_id']

    print("Address Id :",address_id)
    print("Product Qty : ",pqty)
    print("Product Price :",price)
    print("Product Id ",pid)

    addressObj=AddressDetails.objects.get(id=address_id)
    Products=[]
    for x in pid:    
        Products.append(Product.objects.get(id=x))

    print(Products)
    total=[]
    grandTotal=0

    for x in range(len(price)):
        grandTotal+=float(pqty[x])*float(price[x])

    print(grandTotal)

    
    myCursor = connection.cursor()
    myCursor.execute('SELECT * FROM buyer_orders ORDER BY ID DESC LIMIT 1')
    orderData=list(myCursor.fetchone())
    
    print(orderData)
    
    uobj=userProfile.objects.get(user__username=request.user)


    # OID_DATE(DDMMYYYY)_RandomNumber
    oid="OID_"+str(date.today())+"_"+str(orderData[0]+1)

    order=orders(order_id=oid,total_amt=grandTotal,amt_status=0,placed_by=uobj,Address=addressObj)
    order.save()

    for x in range(len(pqty)):
        Order_Product=OrderProduct(order=order,product=Product.objects.get(id=pid[x]),qty=pqty[x],status=0)
        Order_Product.save()
    
    for x in range(len(pqty)):
        total.append(float(pqty[x])*float(price[x]))
        
        # Deleting the Data from stock Update 
        product=Product.objects.filter(id=pid[x])
        newQty=product[0].qty-int(pqty[x])
        product.update(qty=newQty)

    # Cart clear
    cartObj=Cart.objects.filter(user_id=uobj.id)
    cartObj.delete()
    
    return render(request,"invoice.html",{'order_id':oid,'products':Products,'address':addressObj,'pqty':pqty,'total':total,'grandTotal':grandTotal,'uobj':uobj})

    #return render(request,"Invoice.html",{'products':Products,'pqty':pqty,'total':total,'grandTotal':grandTotal,'uobj':uobj})

@login_required
def orderCreation(amt, userObj, product_qty, product_id):


    pass    


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
   
@login_required
def cartdel(request,id):
    uobj=userProfile.objects.get(user__username=request.user)
    pobj=Product.objects.get(id=id)

    c=Cart.objects.get(user=uobj,product=pobj)
    c.delete()

    return redirect('/buyer/cartDetails/')

@login_required
def cartDetails(request):
    uobj=userProfile.objects.get(user__username=request.user)
    products=[]


    address=AddressDetails.objects.filter(user_id=uobj.id)

    cartObj=Cart.objects.filter(user_id=uobj.id)
    amt=0
    
    cartCount=Cart.objects.filter(user_id=uobj.id).count()


    for i in cartObj:
        products.append(Product.objects.get(id=i.product_id))

    print(products)


    for x in products:
        amt+=int(x.price)
    
    cartCount=Cart.objects.filter(user_id=uobj.id).count()
    return render(request,"CartDetails.html",{'products':products,'count':cartCount,'address':address,'uobj':uobj,'amount':amt})

@login_required
def cart(request,id):
    
    pobj=Product.objects.get(id=id)
    uobj=userProfile.objects.get(user__username=request.user)

    try:
        c=Cart(product=pobj,user=uobj)
        c.save()
        messages.success(request,"Product Addedd")
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


@login_required
def updateAddress(request):

    if request.method=='POST':
        add1=request.POST['add1']
        add2=request.POST['add2']
        pincode=request.POST['pincode']
        city=request.POST['city']
        landmark=request.POST['landmark']
        state=request.POST['state']
        mobile=request.POST['mobile']
        uobj=userProfile.objects.get(user__username=request.user)

        
        Address=AddressDetails(Address_line1=add1,Address_line2=add2,pincode=pincode,city=city,landmark=landmark,state=state,mobile=mobile,user=uobj)
        Address.save()


        uobj=userProfile.objects.get(user__username=request.user)

    
        addressObj=AddressDetails.objects.filter(user_id=uobj.id)
        print(" Is that Exist : ",addressObj)
        return render(request,"profile.html", {'userdata':uobj,'Address':addressObj })






    return render(request, "updateAddress.html")


@login_required
def updateUserDetails(request):
    pass


# User profile update n all
@login_required
def profile(request):
    uobj=userProfile.objects.get(user__username=request.user)

    
    addressObj=AddressDetails.objects.filter(user_id=uobj.id)
    print(" Is that Exist : ",addressObj)
    return render(request,"profile.html", {'userdata':uobj,'Address':addressObj })



    


