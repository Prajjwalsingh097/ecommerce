from django.shortcuts import *

from .models import *
from seller.models import *
from buyer.models import *

from django.db import connection
from django.db import *
from django.contrib.auth.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required



def log_in(request):
    cat=Category.objects.all()
    products=Product.objects.all()
    
    
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

        

        nm = request.POST['name']
        pswd=request.POST['password']

        user = authenticate(username=nm, password=pswd)
        print(user)

        if user:
            login(request,user)
            print("Authenticated")
            profileObject=userProfile.objects.get(username=user)
            print("Data odf ProfileObject : ",profileObject.userType)

            # Redirecting using CRUD in Django
            
            if profileObject.userType=='seller':
                return redirect('/seller/home/')
                #return render(request,'index.html',{'user':profileObject.userType})
            elif profileObject.userType=='buyer' :
                return redirect('/buyer/home/')
                #return render(request,"index.html",{'user':profileObject.userType})
  
            '''
            Redirecting using Queries 


            myCursor = connection.cursor()
            myCursor.execute("select * from ecommerce_userprofile where username='{}'".format(nm))
            usr=myCursor.fetchone()
            print(usr)
            if usr[1]=='seller':
                return render(request,'index.html',{'user':usr[1]})
            elif usr[1]=='buyer' :
                return render(request,"index.html",{'user':usr[1]})
            '''

        
    
        
    # Not Passing due to over data on Page 
    # Just past it into the returns dict after {'cat':cat}
    # ,'products':products
    return render(request,"login.html",{'cat':cat})

@login_required
def log_out(request):
	logout(request)
	return render(request,"login.html")


def signup(request):

    cat=Category.objects.all()
    products=Product.objects.all()
    '''    
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
    ''' 

    if request.method=="POST":
        fn=request.POST['fname']
        ln=request.POST['Lname']
        un=request.POST['usname']
        pswd=request.POST['password']
        email=request.POST['email']
        mobile=request.POST['mobile']
        address=request.POST['address']
        usertype=request.POST['usertype']

        if usertype=="seller":
            uobj=User(first_name=fn,last_name=ln,username=un, password=make_password(pswd),is_superuser=1,email=email)
            uobj.save()

            u_obj=userProfile(user=uobj, userType=usertype,address=address,mobile=mobile,username=un)
            u_obj.save()

            return redirect("/login/")
        elif usertype=="buyer":
            uobj=User(first_name=fn,last_name=ln,username=un, password=make_password(pswd),is_superuser=1,email=email)
            uobj.save()

            u_obj=userProfile(user=uobj, userType=usertype,address=address,mobile=mobile,username=un)
            u_obj.save()

            return redirect("/login/")
    
    # Not Passing due to over data on Page 
    # Just past it into the returns dict after {'cat':cat}
    # ,'products':products
    return render(request,"signup.html",{'cat':cat})


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
    
    
    return render(request, 'index.html',{'cat':cat,'products':products})
