from django.shortcuts import render,HttpResponse,redirect
from app.models import Register,shopregister,product,review,Wishlist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.urls import reverse
import random
from django.contrib.auth.decorators import login_required
import requests
import json
url = "https://pricer.p.rapidapi.com/str"

# Create your views here.
# def index(request):
#     # Fetch all shops with their related products using prefetch_related
#     shops = shopregister.objects.all()
#     for shop in shops:
#         # Prefetch related products for each shop
#         shop.products = shop.product_set.all()
#     return render(request, 'index.html', {'products': shops})


def shophome(request):
    return render(request,'shophome.html')


from django.shortcuts import render
from .models import product, shopregister  # Import the shopregister model

def index(request):
    products = product.objects.all()  # Fetch all products
    shops = shopregister.objects.all()  # Fetch all shops
    return render(request, 'main-index.html', {'products': products, 'shops': shops})


def home(request):
    return render(request,'home.html')

def adhome(request):
    return render(request,'adhome.html')

def adminproduct(request):
    return render(request,'adminproduct.html')

def register(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        age=request.POST.get('age')
        image=request.FILES.get('image')
        gender=request.POST.get('gender')
        if Register.objects.filter(email=email).exists():
            alert="<script>alert('email already exist');window.location.href='/register';</script>"
            return HttpResponse(alert)
        obj=Register(name=name,email=email,phone=phone,password=password,age=age,image=image,gender=gender)
        obj.save()
        return redirect('index')
    return render(request,'register.html')

def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            us=Register.objects.get(email=email,password=password)
            semail=us.email
            request.session['email']=semail
            return redirect('product_list')
        except:
            msg="invalid username or password" 
        return render(request,'login.html',{"msg":msg})
    return render(request,'login.html')  
     
def viewprofile(request):
    try:
        email=request.session['email']
        user=Register.objects.get(email=email)
        if user:
            return render(request,'viewprofile.html',{'usr':user})
        else:
            return redirect('login')
    except:
        return redirect('login') 

def editprofile(request):
    email=request.session['email']
    user=Register.objects.get(email=email)
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        age=request.POST.get('age')
        image=request.FILES.get('image')
        gender=request.POST.get('gender')

        user.name=name
        user.email=email
        user.phone=phone
        user.password=password
        user.age=age
        if image:
            user.image=image
        user.gender=gender
        user.save()
        return redirect('viewprofile')
    return render(request,'editprofile.html',{'usr':user})

def delprofile(request,id):
    user=Register.objects.get(id=id)
    user.delete()
    return redirect('index')


def shopindex(request):
    return render(request,'shopindex.html')

def shopreg(request):
    if request.method == "POST":
        shopname = request.POST.get('shopname')
        shopownername = request.POST.get('shopownername')
        storeid = request.POST.get('storeid')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        location = request.POST.get('location')

        if shopregister.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exists');window.location.href='/shopregister';</script>")

        obj = shopregister(
            shopname=shopname, shopownername=shopownername, email=email,
            phone=phone, password=password, image=image, location=location,
            storeid=storeid, status="pending"
        )
        obj.save()
        return redirect('shoplogin')

    return render(request, 'shopregister.html')


def shoplogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            us = shopregister.objects.get(email=email, password=password)

            if us.status == "approved": 
                request.session['semail'] = us.email
                return redirect('seller_list')
            else:
                msg = "Your shop is awaiting admin approval."
        except shopregister.DoesNotExist:
            msg = "Invalid username or password."

        return render(request, 'shoplogin.html', {"msg": msg})

    return render(request, 'shoplogin.html')

from django.shortcuts import render, redirect
from app.models import shopregister

def admin_shops(request):
    shops = shopregister.objects.all()
    return render(request, 'admin_shops.html', {'shops': shops})

def approve_shop(request, shop_id):
    shop = shopregister.objects.get(id=shop_id)
    shop.status = "approved"
    shop.save()
    return redirect('admin_shops')


     
def shopviewprofile(request):
    try:
        email=request.session['semail']
        shop=shopregister.objects.get(email=email)
        if shop:
            return render(request,'shopviewprofile.html',{'shop':shop})
        else:
            return redirect('shoplogin')
    except Exception as e:
        print (e)
        return redirect('shoplogin')  

def shopeditprofile(request):
    email=request.session['semail']
    try:

        shop=shopregister.objects.get(email=email)
    except  :
        return redirect('shoplogin')
    if request.method=="POST":
        shopname=request.POST.get('shopname')
        shopownername=request.POST.get('shopownername')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        storeid=request.POST.get('storeid')
        image=request.FILES.get('image')
        location=request.POST.get('location')

        shop.shopname=shopname
        shop.shopownername=shopownername
        shop.email=email
        shop.phone=phone
        shop.password=password
        shop.storeid=storeid
        shop.location=location
        if image:
            shop.image=image
        shop.save()
        return redirect('shopviewprofile')
    return render(request,'shopeditprofile.html',{'shop':shop})

def shopdelprofile(request,id):
    shop=shopregister.objects.get(id=id)
    shop.delete()
    return redirect('shopindex')

def addproduct(request):
    email=request.session['semail']
    try:
        shop=shopregister.objects.get(email=email)
    except  :
        return redirect('shoplogin')
    if request.method=='POST':
        productname=request.POST.get('productname')
        productimage=request.FILES.get('productimage')
        productprice=request.POST.get('productprice')
        offerprice=request.POST.get('offerprice')
        discountvalue=request.POST.get('discountvalue')
        stock=request.POST.get('stock')
        obj=product(productname=productname,productimage=productimage,productprice=productprice,offerprice=offerprice,discountvalue=discountvalue,stock=stock,shopname=shop)
        obj.save()
        return redirect('seller_list')
    return render(request,'addproduct.html')
                
# def product_list(request):
#     # Retrieve all the products from the database
#     products = product.objects.all()
#     return render(request, 'productlist.html', {'products': products})

# from django.db.models import Q
# def product_list(request):
#     query = request.GET.get('search', '')  # Get the search query from the user
#     products = product.objects.filter(
#         Q(productname__icontains=query) | Q(shopname__shopname__icontains=query)
#     ).order_by(
#         'offerprice' if query else 'productprice'
#     )

#     return render(request, 'productlist.html', {'products': products, 'query': query})


from django.shortcuts import render
from .models import product,NotifyModel
from django.db.models import Q


def notify_me(request, product_id):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user=Register.objects.get(email = email)        
            Product = get_object_or_404(product, id=product_id)  
            notify_model , created = NotifyModel.objects.get_or_create(user=user,product = Product , seen = False )
            print("p",Product.productname)
            if not created:
                 return JsonResponse({'message': f'You already  notified. So when {Product.productname} is back in stock you will be notified'})
            
            else:
                return JsonResponse({'message': f'You will be notified when {Product.productname} is back in stock!'})
        except:
            return redirect('product_list')
    else:
        return redirect('login')




from django.shortcuts import render
from .models import product, ShopPoster
from django.utils import timezone
def product_list(request):
    query = request.GET.get('search', '')  # Get the search query from the user

    # Delete expired posters
    today = timezone.now().date()
    ShopPoster.objects.filter(expire_date__lt=today).delete()

    # If no search query, show all products
    if query == '':
        products = product.objects.all().order_by('offerprice' if query else 'productprice')
    else:
        # Filter for products matching the search query
        products = product.objects.filter(
            Q(productname__icontains=query) | Q(shopname__shopname__icontains=query)
        ).order_by('offerprice' if query else 'productprice')

    # Fetch only non-expired posters
    posters = ShopPoster.objects.filter(expire_date__gte=today)

    return render(request, 'productlist.html', {
        'products': products,
        'query': query,
        'posters': posters,  # Pass non-expired posters to the template
    })

def re_product(request,cid):
    data=product.objects.get(id=cid)
    pro=review.objects.filter(product=data)
    return render(request, 'shopreview.html',{'product':data,'reviews':pro})
# def product_list(request):
#     query = request.GET.get('search', '')  # Get the search query from the user

#     # If no search query, show all products
#     if query == '':
#         products = product.objects.all().order_by('offerprice' if query else 'productprice')
#     else:
#         # Filter for all products that contain the search query or are either SAMSUNG or iPhone
#         products = product.objects.filter(
#             Q(productname__icontains=query) | Q(shopname__shopname__icontains=query)
#         ).order_by('offerprice' if query else 'productprice')

#     # For Samsung or iPhone-specific filtering
#     samsung_products = product.objects.filter(
#         Q(productname__icontains="SAMSUNG") & 
#         (Q(productname__icontains=query) | Q(shopname__shopname__icontains=query)
#         )
#     ).order_by('offerprice' if query else 'productprice')

#     iphone_products = product.objects.filter(
#         Q(productname__icontains="iPhone") & 
#         (Q(productname__icontains=query) | Q(shopname__shopname__icontains=query)
#         )
#     ).order_by('offerprice' if query else 'productprice')

#     return render(request, 'productlist.html', {
#         'products': products, 
#         'samsung_products': samsung_products,
#         'iphone_products': iphone_products,
#         'query': query
#     })

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .models import product


def get_shop_coordinates(location_name):
    """Convert shop location name to coordinates"""
    try:
        geolocator = Nominatim(user_agent="my_store_app")
        location = geolocator.geocode(location_name)
        if location:
            return (location.latitude, location.longitude)
    except Exception:
        return None
    return None

def nearby_products(request):
    """View for nearby products page"""
    return render(request, 'nearby_products.html')

def get_nearby_products_data(request):
    """AJAX endpoint for getting nearby products"""
    if request.method == 'POST':
        try:
            # Check if we're getting coordinates directly
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            print('lat', latitude )
            print('lng', longitude, )
            
            if latitude and longitude:
                user_lat = float(latitude)
                user_lng = float(longitude)
            else:
                # Handle location search case
                location_search = request.POST.get('location_search')
                if not location_search:
                    return JsonResponse({
                        'success': False,
                        'error': 'No location data provided'
                    })
                
                user_coords = get_shop_coordinates(location_search)
                if not user_coords:
                    return JsonResponse({
                        'success': False,
                        'error': 'Unable to find the specified location'
                    })
                user_lat, user_lng = user_coords
            
            user_location = (user_lat, user_lng)
            all_products = product.objects.all()
            nearby_products = []
            
            for prod in all_products:
                shop_coords = get_shop_coordinates(prod.shopname.location)
                if shop_coords:
                    distance = geodesic(user_location, shop_coords).kilometers
                    if distance <= 10:  # 10km radius
                        nearby_products.append({
                            'id': prod.id,
                            'name': prod.productname,
                            'price': str(prod.offerprice if prod.offerprice else prod.productprice),
                            'original_price': str(prod.productprice),
                            'discount': prod.discountvalue,
                            'stock': prod.stock,
                            'image': prod.productimage.url if prod.productimage else '',
                            'shop': prod.shopname.shopname,
                            'location': prod.shopname.location,
                            'distance': round(distance, 2)
                        })
            
            nearby_products.sort(key=lambda x: x['distance'])
            
            return JsonResponse({
                'success': True,
                'products': nearby_products
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
# views.py


# def shop_list(request):
#     shops = shopregister.objects.all()
#     return render(request, 'productlist.html', {'shops': shops})


def seller_list(request):
    email = request.session.get('semail')  # Get the seller's email from session
    try:
        shop = shopregister.objects.get(email=email)
    except shopregister.DoesNotExist:
        return redirect('shoplogin')  
    products = product.objects.filter(shopname=shop)
    return render(request, 'sellerlist.html', {'products': products})
from django.core.mail import send_mail
from django.utils import timezone
from .models import NotifyModel
from .import models
from django.conf import settings

def send_stock_notifications():
    # Find products with stock > 0
    products_in_stock = models.product.objects.filter(stock__gt=0)

    for produc in products_in_stock:
        notifications = NotifyModel.objects.filter(product=produc, seen=False)
        
        for notification in notifications:
            send_mail(
                subject=f"Product {produc.productname} is now available!",
                message=f"The product {produc.productname} is now back in stock.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[notification.user.email]
            )
            # Mark the user as notified
            notification.notified = True
            notification.save()


def edit_product(request, product_id):
    email = request.session.get('semail')  
    if not email:
        return redirect('shoplogin')

    shop = shopregister.objects.get(email=email) 
    product_obj = get_object_or_404(product, id=product_id, shopname=shop) 

    if request.method == 'POST':
        product_obj.productname = request.POST.get('productname')
        product_obj.productprice = request.POST.get('productprice')
        product_obj.offerprice = request.POST.get('offerprice')
        product_obj.discountvalue = request.POST.get('discountvalue')
        product_obj.stock = int(request.POST.get('stock'))

        if 'productimage' in request.FILES:
            product_obj.productimage = request.FILES['productimage']
        
        product_obj.save() 
        if product_obj.stock > 0:
            send_stock_notifications()  
        return redirect('seller_list') 

    return render(request, 'edit_product.html', {'product': product_obj})


def delete_product(request,product_id):
    email = request.session.get('semail')
    if not email:
        return redirect('shoplogin')
    shop = shopregister.objects.get(email=email)
    product_obj = get_object_or_404(product,id=product_id,shopname=shop)

    product_obj.delete()
    return redirect('seller_list')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        admail = 'admin@gmail.com'
        adpass = '123'
        if email == admail:
            if password == adpass:
                return redirect('adhome')
    return render (request,'adminlogin.html')

def aduser(request):
    users = Register.objects.all()
    return render(request, 'aduser.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(Register, id=user_id)
    user.delete()
    return redirect('aduser')

def delete_shop(request, shop_id):
    shop = get_object_or_404(shopregister, id=shop_id)
    shop.delete()
    return redirect('adshop')

def adshop(request):
    # Fetch all shops from the shopregister model
    shops = shopregister.objects.all()
    return render(request, 'adshop.html', {'shops': shops})

# def adseller_list(request):
#     email = request.session.get('semail')  
#     try:
#         shop = shopregister.objects.get(email=email)
#     except shopregister.DoesNotExist:
#         return redirect('shoplogin')  
#     products = product.objects.filter(shopname=shop)
#     return render(request, 'sellerlist.html', {'products': products})

def adseller_list(request, shop_id):
    try:
        shop = shopregister.objects.get(id=shop_id)
    except shopregister.DoesNotExist:
        return redirect('adminhome') 
    products = product.objects.filter(shopname=shop)

    return render(request, 'adminproduct.html', {'products': products, 'shop': shop})

def addelete_product(request, p_id):
    ap = get_object_or_404(product, id=p_id)
    ap.delete()
    return redirect('adhome')



# def review(request):
#     if request.method == 'POST':
#         productdes = request.POST.get('productdes')
#         rating = request.POST.get('rating')

#         # Create and save the review object
#         review_instance = review(productdes=productdes, rating=rating)
#         review_instance.save()

#         return redirect('success')  # Redirect to a success page

#     return render(request, 'review.html')


def review_view(request, product_id):
    product_instance = get_object_or_404(product, id=product_id)
    
    if request.method == 'POST':
        productdes = request.POST.get('productdes')
        rating = request.POST.get('rating')

        # Create and save the review object for the specific product
        review_instance = review(product=product_instance, productdes=productdes, rating=rating)
        review_instance.save()

        return redirect('product_list')  # Redirect to a success page

    return render(request, 'review.html', {'product': product_instance})


# def view_reviews(request, product_id):
#     try:
#         product_obj = product.objects.get(id=product_id)
#         reviews = review.objects.filter(product=product_obj)
#         return render(request, 'view_reviews.html', {'product': product_obj, 'reviews': reviews})
    
#     except product.DoesNotExist:
#         return render(request, '404.html') 


from django.db.models import Avg

def view_reviews(request, product_id):
    try:
        # Get the product object
        product_obj = product.objects.get(id=product_id)
        
        # Get all reviews related to this product
        reviews = review.objects.filter(product=product_obj)
        
        # Calculate the average rating for this product
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        
        if not average_rating:
            average_rating = 0
        

        return render(request, 'view_reviews.html', {
            'product': product_obj,
            'reviews': reviews,
            'average_rating': average_rating
        })
    
    except product.DoesNotExist:
        return render(request, '404.html') 

def add_to_wishlist(request, product_id):
    if 'email' in request.session:
        email = request.session.get('email')
        user = Register.objects.get(email=email)
        product_obj = product.objects.get(id=product_id)

        # Check if the product is already in the wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, products=product_obj)  # Use 'products' instead of 'product'

        if not created:
            # If the item already exists in the wishlist, you might want to notify the user
            return redirect('wishlist')  # Redirect to wishlist page or show a message

        return redirect('wishlist')  # Redirect to wishlist page
    else:
        return redirect('login')

    

def view_wishlist(request):
    if 'email' in request.session:
        email = request.session.get('email')
        user = Register.objects.get(email=email)

        # Get all products in the user's wishlist
        wishlist_items = Wishlist.objects.filter(user=user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login') 

def remove_from_wishlist(request, item_id):
    if 'email' in request.session:
        email = request.session.get('email')
        user = Register.objects.get(email=email)

        # Get the wishlist item and delete it
        wishlist_item = get_object_or_404(Wishlist, id=item_id, user=user)
        wishlist_item.delete()
        return redirect('wishlist')
    else:
        return redirect('login')


import pandas as pd
from django.shortcuts import render
from .models import product, review

from django.db.models import Count, Avg
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend_products(user_id):
    """
    Generate product recommendations for a user using collaborative filtering,
    inferred indirectly from review data.
    """
    # Fetch all reviews
    reviews = review.objects.all()

    if not reviews.exists():
        return []

    # Simulate user IDs for collaborative filtering
    # Assuming `request.user` has a unique identifier
    user_ratings = {}
    for idx, rev in enumerate(reviews):
        user_ratings.setdefault(idx % 10, []).append({"product_id": rev.product.id, "rating": rev.rating})

    # Create a DataFrame for user-product ratings
    data = {
        "user_id": [],
        "product_id": [],
        "rating": [],
    }

    for user_id, ratings in user_ratings.items():
        for r in ratings:
            data["user_id"].append(user_id)
            data["product_id"].append(r["product_id"])
            data["rating"].append(r["rating"])

    df = pd.DataFrame(data)

    # Create a pivot table (users as rows, products as columns, ratings as values)
    pivot_table = df.pivot_table(index="user_id", columns="product_id", values="rating", fill_value=0)

    # Calculate the similarity matrix using cosine similarity
    similarity_matrix = cosine_similarity(pivot_table)
    user_similarities = pd.DataFrame(similarity_matrix, index=pivot_table.index, columns=pivot_table.index)

    # Find the most similar users to the given user (simulated user IDs)
    user_index = user_id % 10  # Map the user ID to a simulated user
    if user_index not in user_similarities.index:
        return []

    similar_users = user_similarities[user_index].sort_values(ascending=False).index[1:]  # Exclude the user itself

    # Get product recommendations based on similar users' preferences
    recommendations = []
    for similar_user in similar_users:
        user_ratings = pivot_table.loc[similar_user]
        recommended_products = user_ratings[user_ratings > 0].index.tolist()
        recommendations.extend(recommended_products)

    # Remove duplicates and return as a list of product IDs
    return list(set(recommendations))
from django.db.models import Count

from django.db.models import Count
from .models import product, review
import random

def display_random_products(request):
    user = request.user  # Assuming the user is authenticated

    # Get recommended product IDs
    recommended_product_ids = recommend_products(user.id) if user.is_authenticated else []

    if recommended_product_ids:
        # Fetch the recommended product objects randomly
        recommended_products = product.objects.filter(id__in=recommended_product_ids).order_by('?')[:6]  # Limit to 6 random products
    else:
        # Fall back to listing products randomly based on reviews (popularity)
        reviewed_products = (
            review.objects.values("product")
            .annotate(review_count=Count("product"))
            .order_by("-review_count")
        )
        product_ids = [item["product"] for item in reviewed_products]
        recommended_products = product.objects.filter(id__in=product_ids).order_by('?')[:6]  # Limit to 6 random products

    return render(request, 'random_products.html', {'products': recommended_products})





def adminedit_product(request, product_id):
    # Get the product by ID
    product_obj = get_object_or_404(product, id=product_id)
    
    # If the request is POST, process the form data
    if request.method == 'POST':
        product_obj.productname = request.POST.get('productname')
        product_obj.productprice = request.POST.get('productprice')
        product_obj.offerprice = request.POST.get('offerprice')
        product_obj.discountvalue = request.POST.get('discountvalue')
        product_obj.stock = request.POST.get('stock')

        # If there's an uploaded file (product image), update the product image
        if 'productimage' in request.FILES:
            product_obj.productimage = request.FILES['productimage']
        
        product_obj.save()  # Save the product with updated data
        
        # Redirect to the product list page for the same shop
        return redirect('adseller_list', shop_id=product_obj.shopname.id)
    
    return render(request, 'admin_edit_product.html', {'product': product_obj})


#product compare
# def productt(request):
#    if request.method=='POST':
#       sr=request.POST.get('cs')
#       querystring = {"q":sr}
      

#       headers = {
#          "X-RapidAPI-Key": "8228a841camsh2b4989400084094p16dbd0jsn95bc8590ae4e",
#          "X-RapidAPI-Host": "pricer.p.rapidapi.com"
#       }

#       response = requests.get(url, headers=headers, params=querystring)

#       print(response.json())   

#       result=response.json()
#       # print(result)

#       li=[]

#       for i in range(1,12):
#         dic = {
#            "image":result[i]['img'],
#             'title':result[i]['title'],
#             'price':result[i]['price'],
#             'shop':result[i]['shop']
#          }
#         li.append(dic) 
#       request.session['prod']=li
#       print('title 2 is ',result[1]['title'])
#       print('price 2 is ',result[1]['price'])
#       return render(request,'listpricecom.html',{'lis':li})
#    else:
#       return render(request,'productcom.html')



import requests

def productt(request):
    if request.method == 'POST':
        sr = request.POST.get('cs')
        querystring = {"q": sr}

        headers = {
            "X-RapidAPI-Key": "8228a841camsh2b4989400084094p16dbd0jsn95bc8590ae4e",
            "X-RapidAPI-Host": "pricer.p.rapidapi.com"
        }

        # Fetch data from API
        url = "https://pricer.p.rapidapi.com/str"  # Replace with the actual API endpoint
        response = requests.get(url, headers=headers, params=querystring)
        result = response.json()

        # USD to INR conversion rate
        USD_TO_INR = 82.0  # Replace this with the current conversion rate if needed

        api_products = []
        for i in range(1, min(12, len(result))):  # Handle cases where result has fewer items
            try:
                price_inr = float(result[i]['price'].replace("$", "").replace(",", "")) * USD_TO_INR
                dic = {
                    "image": result[i]['img'],
                    "title": result[i]['title'],
                    "price": price_inr,  # Converted price in INR
                    "shop": result[i]['shop'],
                    "link": result[i]['link'],
                }
                api_products.append(dic)
            except (KeyError, ValueError):
                continue  # Skip items with missing or invalid data

        # Fetch local products from the database
        local_products = product.objects.filter(productname__icontains=sr)

        # Find the best products based on price
        best_api_product = None
        if api_products:
            best_api_product = min(api_products, key=lambda x: x['price'])

        best_local_product = None
        if local_products.exists():
            best_local_product = min(local_products, key=lambda x: (x.productprice if x.productprice is not None else float('inf')))


        return render(
            request, 
            'listpricecom.html', 
            {
                'api_products': api_products,
                'local_products': local_products,
                'best_api_product': best_api_product,
                'best_local_product': best_local_product
            }
        )
    else:
        return render(request, 'productcom.html')



from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)  # This will log the user out
    request.session.flush()  # This clears the session
    return redirect('index')  # Redirect to any URL after logout

import os
from django.shortcuts import render
from django.http import JsonResponse
from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO

import os
from django.shortcuts import render
from django.http import JsonResponse
from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO

# Initialize Hugging Face Client
HUGGING_FACE_TOKEN = "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"
client = InferenceClient(model="stabilityai/stable-diffusion-3-medium-diffusers", token=HUGGING_FACE_TOKEN)

# View for generating image
def generate_image(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        if not prompt:
            return JsonResponse({"error": "Prompt cannot be empty."}, status=400)

        try:
            # Generate the image from the prompt
            image = client.text_to_image(prompt=prompt)

            # Convert JpegImageFile to bytes-like object
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Save the image to the media directory
            output_path = os.path.join("media", "generated_image.png")
            os.makedirs("media", exist_ok=True)

            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())

            return JsonResponse({"message": "Image generated successfully!", "image_url": f"/{output_path}"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return render(request, "poster.html")

def camera_view(request):
    return render(request, 'camera.html')
# import imagehash
# from PIL import Image
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# from django.views.decorators.csrf import csrf_exempt
# from .models import UploadedImage, product  # Now using 'product'

# @csrf_exempt
# def detect_object(request):
#     if request.method == "GET":
#         return render(request, "camera.html")

#     if request.method == "POST" and request.FILES.get("image"):
#         image_file = request.FILES["image"]

#         # Save the uploaded image in the model
#         uploaded_image = UploadedImage.objects.create(image=image_file)

#         # Convert uploaded image to hash
#         uploaded_img_path = uploaded_image.image.path
#         uploaded_img = Image.open(uploaded_img_path)
#         uploaded_hash = imagehash.average_hash(uploaded_img)

#         # Compare with stored product images
#         matched_products = []
#         for prod in product.objects.all():  # Using 'product' model
#             product_img = Image.open(prod.productimage.path)
#             product_hash = imagehash.average_hash(product_img)

#             if uploaded_hash - product_hash < 10:  # Adjust threshold if needed
#                 matched_products.append({
#                     "name": prod.productname,
#                     "image": prod.productimage.url,
#                     "price": prod.productprice,
#                     "offer": prod.offerprice
#                 })

#         return JsonResponse({"products": matched_products})

#     return JsonResponse({"error": "No image received"}, status=400)
import requests
import imagehash
from PIL import Image
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import product, UploadedImage

# Import for BLIP image captioning
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Load BLIP model and processor (this may take a few seconds on the first run)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Your RapidAPI key and host for searching products (new API)
RAPIDAPI_KEY = "5659871bb9msh0c1d0cf56ee7423p198b9ajsnac7cd20ccaa4"
RAPIDAPI_HOST = "image-search19.p.rapidapi.com"

# @csrf_exempt
# def detect_object(request):
#     if request.method == "GET":
#         return render(request, "camera.html")

#     if request.method == "POST" and request.FILES.get("image"):
#         image_file = request.FILES["image"]

#         # Save the image in UploadedImage model
#         uploaded_image = UploadedImage.objects.create(image=image_file)
#         file_path = uploaded_image.image.path  # Get the file path

#         # Open the uploaded image using Pillow
#         uploaded_img = Image.open(file_path)

#         # First, attempt to compare with stored product images using image hashing.
#         matched_products = compare_image_to_products(uploaded_img)

#         # If no match is found in DB, use BLIP to generate a caption (text prompt)
#         if not matched_products:
#             caption = generate_caption(file_path)
#             print(f"Generated caption: {caption}")
#             # Now, search products using the caption text via RapidAPI
#             matched_products = search_products("cell phone",'8228a841camsh2b4989400084094p16dbd0jsn95bc8590ae4e')
#             print(f"Searching products", matched_products)

#         return JsonResponse({"products": matched_products})

#     return JsonResponse({"error": "No image received"}, status=400)
@csrf_exempt
def detect_object(request):
    """
    Django view to handle image upload and product detection.
    """
    if request.method == "GET":
        return render(request, "camera.html")

    if request.method == "POST" and request.FILES.get("image"):
        try:
            image_file = request.FILES["image"]
            
            # Save the image in UploadedImage model
            uploaded_image = UploadedImage.objects.create(image=image_file)
            file_path = uploaded_image.image.path
            
            # Open the uploaded image using Pillow
            uploaded_img = Image.open(file_path)
            
            # First try to match with stored products
            matched_local_products = compare_image_to_products(uploaded_img)
            
            # Generate caption for text comparison
            caption = generate_caption(file_path)
            print(f"Generated caption: {caption}")
            
            # Search products using RapidAPI
            api_key = '3bb32231d3msh540c378a06635a7p18be36jsn7fe931169d1b'
            online_products = search_products(caption, api_key)
            
            if not online_products:
                # Fallback to generic search if no specific matches
                online_products = search_products("washing machine", api_key)
            
            # Combine results while keeping track of source
            all_products = []
            
            # Add matched local products if any
            if matched_local_products:
                all_products.extend(matched_local_products)
            
            # Add online products if any
            if online_products:
                all_products.extend(online_products)
            
            return JsonResponse({
                "success": True,
                "products": all_products
            })
            
        except Exception as e:
            print(f"Error in detect_object: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "success": False,
        "error": "No image received"
    }, status=400)


import numpy as np
from scipy.spatial.distance import cosine

def compare_image_to_products(uploaded_img):
    """Compare the uploaded image to product images using multiple comparison methods."""
    matched_products = []
    
    # Calculate multiple hashes for uploaded image
    uploaded_avg_hash = imagehash.average_hash(uploaded_img)
    uploaded_phash = imagehash.phash(uploaded_img)
    uploaded_dhash = imagehash.dhash(uploaded_img)
    
    # Calculate color histogram for uploaded image
    uploaded_hist = get_color_histogram(uploaded_img)

    for prod in product.objects.all():
        try:
            product_img = Image.open(prod.productimage.path)
            
            # Calculate multiple hashes for product image
            product_avg_hash = imagehash.average_hash(product_img)
            product_phash = imagehash.phash(product_img)
            product_dhash = imagehash.dhash(product_img)
            
            # Calculate color histogram for product image
            product_hist = get_color_histogram(product_img)
            
            # Calculate various similarity scores
            avg_hash_diff = uploaded_avg_hash - product_avg_hash
            phash_diff = uploaded_phash - product_phash
            dhash_diff = uploaded_dhash - product_dhash
            color_similarity = 1 - cosine(uploaded_hist, product_hist)
            
            # Combine scores with different weights
            weighted_score = (
                0.3 * (1 - avg_hash_diff / 64) +  # Normalize to 0-1 range
                0.3 * (1 - phash_diff / 64) +
                0.2 * (1 - dhash_diff / 64) +
                0.2 * color_similarity
            )
            
            # Add all products with their similarity scores
            matched_products.append({
                'source': 'database',
                'prid': int(prod.id),  
                "productname": prod.productname,
                "productimage": prod.productimage.url,
                "productprice": prod.productprice,
                "offerprice": prod.offerprice,
                "discountvalue": prod.discountvalue,
                "stock": prod.stock,
                "shopname": prod.shopname.shopname,
                "similarity": round(weighted_score * 100, 2)  # Convert to percentage
            })
      
                
        except Exception as e:
            print(f"Error comparing image for product {prod.productname}: {e}")
            
    # Sort matches by similarity score
    matched_products.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Filter results based on threshold - lowered to increase matches
    filtered_products = [p for p in matched_products if p['similarity'] > 90]  # 70% threshold
    
    # Return either matched products or a no match indicator
    if filtered_products:
        return filtered_products
    else:
        return None

def get_color_histogram(image, bins=8):
    """Calculate color histogram for the image."""
    # Convert image to RGB if it isn't already
    image = image.convert('RGB')
    
    # Resize image to speed up processing
    image = image.resize((150, 150))
    
    # Get image data
    pixels = np.array(image)
    
    # Calculate histogram for each channel
    hist_r = np.histogram(pixels[:,:,0], bins=bins, range=(0,256))[0]
    hist_g = np.histogram(pixels[:,:,1], bins=bins, range=(0,256))[0]
    hist_b = np.histogram(pixels[:,:,2], bins=bins, range=(0,256))[0]
    
    # Concatenate histograms and normalize
    hist = np.concatenate([hist_r, hist_g, hist_b])
    hist = hist.astype(float) / hist.sum()
    
    return hist

def generate_caption(image_path):
    """Generate a caption (text prompt) for the image using BLIP."""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

import requests
from typing import List, Dict
from django.core.files.storage import default_storage
from PIL import Image
import json
import re
def search_products(query: str, api_key: str) -> List[Dict]:
    """
    Search for products using RapidAPI Pricer, formatted for Django JsonResponse.
    
    Args:
        query (str): Search query string
        api_key (str): RapidAPI key
        
    Returns:
        List[Dict]: List of products formatted for frontend consumption
    """
    url = "https://pricer.p.rapidapi.com/str"
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "pricer.p.rapidapi.com"
    }
    
    params = {
        "q": query
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        results = response.json()
        products = []
        exchange_rate = 83 
        
        # Handle the case where results is a list
        items = results if isinstance(results, list) else results.get('results', [])
        
        for item in items:
            try:
                raw_price = str(item.get('price', '0.00'))
                cleaned_price = re.sub(r'[^\d.]', '', raw_price)
                price_usd = float(cleaned_price) if cleaned_price else 0.00  # Convert to float
                price_inr = round(price_usd * exchange_rate, 2)
                # More defensive parsing of the product data
                product = {
                    'source': 'api',
                    'name': str(item.get('title', 'Unknown Product')),
                    'price': str(price_inr),
                    'currency': 'INR',  # Default currency if not provided
                    'image': str(item.get('img', '')),
                    'url': str(item.get('link', '')),
                    'store': str(item.get('shop', 'Unknown Store'))
                }
                products.append(product)
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue
            
        print(f"Successfully processed {len(products)} products")
        return products[:10]
        
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return []
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Response Parsing Error: {e}")
        return []








# def shop_list(request):
#     shops = ShopRegister.objects.all()
#     return render(request, 'shop_list.html', {'shops': shops})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import shopregister, ShopPoster

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import shopregister, ShopPoster


# def add_poster(request):
#     email=request.session['semail']
#     try:
#         shop=shopregister.objects.get(email=email)
#     except  :
#         return redirect('shoplogin')
#     if request.method == 'POST' and request.FILES.get('poster'):
#         poster_image = request.FILES['poster']
#         ShopPoster.objects.create(shop=shop, poster=poster_image)
#         return redirect('poster_list')
#     return render(request,'add_poster.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from .models import shopregister, ShopPoster

def add_poster(request):
    email = request.session.get('semail')

    if not email:
        messages.error(request, "Please log in first.")
        return redirect('shoplogin')

    try:
        shop = shopregister.objects.get(email=email)
    except shopregister.DoesNotExist:
        messages.error(request, "Shop not found.")
        return redirect('shoplogin')

    if request.method == 'POST':
        if 'poster' in request.FILES:
            poster_image = request.FILES['poster']
            expire=request.POST.get('expire')
            ShopPoster.objects.create(shop=shop, poster=poster_image,expire_date=expire)
            messages.success(request, "Poster uploaded successfully!")
            # return redirect(reverse('poster_list'))
            return redirect(reverse('add_poster'))
        else:
            messages.error(request, "Please upload a valid poster image.")

    return render(request, 'add_poster.html')


# def add_poster(request):
#     email = request.session.get('email') 

#     try:
#         shop = shopregister.objects.filter(email=email)
#     except shopregister.DoesNotExist:
#         return HttpResponse("Shop not found for this email", status=404)

#     if request.method == 'POST' and request.FILES.get('poster'):
#         poster_image = request.FILES['poster']
#         ShopPoster.objects.create(shop=shop, poster=poster_image)
#         return redirect('poster_list')

#     return render(request, 'add_poster.html', {'shop': shop})


def poster_list(request):
    shops = ShopPoster.objects.all()
    return render(request, 'poster_list.html', {'shops': shops})

# from django.shortcuts import render, get_object_or_404
# from .models import shopregister

# def shop_detail(request, shop_id):
#     shop = get_object_or_404(shopregister, id=shop_id)
#     return render(request, 'shop_detail.html', {'shop': shop})


from django.shortcuts import render, get_object_or_404
from .models import product, shopregister

def shop_products(request, shop_id):
    shop = get_object_or_404(shopregister, id=shop_id)
    products = product.objects.filter(shopname=shop)

    return render(request, 'shop_detail.html', {'shop': shop, 'products': products})

from django.utils import timezone

def shop_posters(request):
    email = request.session.get('semail')

    if not email:
        messages.error(request, "Please log in first.")
        return redirect('shoplogin')

    try:
        shop = shopregister.objects.get(email=email)
    except shopregister.DoesNotExist:
        messages.error(request, "Shop not found.")
        return redirect('shoplogin')

    # Get today's date
    today = timezone.now().date()

    # Delete expired posters for this shop
    ShopPoster.objects.filter(shop=shop, expire_date__lt=today).delete()

    # Fetch only non-expired posters belonging to the logged-in shop
    posters = ShopPoster.objects.filter(shop=shop, expire_date__gte=today)

    return render(request, 'shop_posters.html', {'shop': shop, 'posters': posters})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import ShopPoster

def delete_poster(request, poster_id):
    poster = get_object_or_404(ShopPoster, id=poster_id)
    poster.delete()
    messages.success(request, "Poster deleted successfully!")
    return redirect('shop_posters')
