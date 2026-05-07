from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q

from .models import Customer, Restaurant, Item, Cart, AdminUser, Order

import razorpay
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'delivery/index.html')

def open_signin(request):
    return render(request, 'delivery/signin.html')

def open_signup(request):
    return render(request, 'delivery/signup.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        try:
            Customer.objects.get(username = username)
            return HttpResponse("Duplicate username!")
        except Customer.DoesNotExist:
            try:
                Customer.objects.create(
                    username = username,
                    password = password,
                    email = email,
                    mobile = mobile,
                    address = address,
                )
            except Exception as e:
                return HttpResponse(f"Database Error: {e}. If on Vercel, ensure your DATABASE_URL is configured to a PostgreSQL database (SQLite is read-only).")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
            
    return render(request, 'delivery/signin.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            Customer.objects.get(username = username, password = password)
            restaurantList = Restaurant.objects.all()
            return render(request, 'delivery/customer_home.html',{"restaurantList" : restaurantList, "username" : username})
        except Customer.DoesNotExist:
            return render(request, 'delivery/fail.html')
        except Exception as e:
            print(f"Error during signin: {e}")
            return render(request, 'delivery/fail.html')
    
    return render(request, 'delivery/signin.html')

def customer_home(request, username):
    query = request.GET.get('q', '')
    cuisine_filter = request.GET.get('cuisine', '')
    
    restaurantList = Restaurant.objects.all()
    
    if query:
        restaurantList = restaurantList.filter(
            Q(name__icontains=query) | Q(items__name__icontains=query)
        ).distinct()
        
    if cuisine_filter:
        restaurantList = restaurantList.filter(cuisine__icontains=cuisine_filter)
        
    # Extract unique cuisines for the filter buttons
    all_cuisines = Restaurant.objects.values_list('cuisine', flat=True).distinct()
    
    # Process cuisines (split by comma if multiple cuisines are in one string)
    processed_cuisines = set()
    for c in all_cuisines:
        if c:
            for part in c.split(','):
                if part.strip():
                    processed_cuisines.add(part.strip())
    
    cuisines = sorted(list(processed_cuisines))

    return render(request, 'delivery/customer_home.html', {
        "restaurantList": restaurantList, 
        "username": username,
        "query": query,
        "current_cuisine": cuisine_filter,
        "cuisines": cuisines
    })

def open_admin_login(request):
    return render(request, 'delivery/admin_login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            AdminUser.objects.get(username=username, password=password)
            return render(request, 'delivery/admin_home.html', {'username': username})
        except AdminUser.DoesNotExist:
            return render(request, 'delivery/fail.html')
        except Exception as e:
            print(f"Error during admin signin: {e}")
            return render(request, 'delivery/fail.html')
            
    return render(request, 'delivery/admin_login.html')

def open_admin_signup(request):
    return render(request, 'delivery/admin_signup.html')

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        try:
            AdminUser.objects.get(username=username)
            return HttpResponse("Duplicate admin username!")
        except AdminUser.DoesNotExist:
            try:
                AdminUser.objects.create(
                    username=username,
                    password=password,
                    email=email,
                )
                return render(request, 'delivery/admin_login.html')
            except Exception as e:
                return HttpResponse(f"Database Error: {e}. If on Vercel, ensure your DATABASE_URL is configured correctly.")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
            
    return render(request, 'delivery/admin_login.html')

def admin_home(request):
    return render(request, 'delivery/admin_home.html', {'username': 'admin'})
    
def open_add_restaurant(request):
    return render(request, 'delivery/add_restaurant.html', {'username': 'admin'})

def add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        try:
            Restaurant.objects.get(name = name)
            return HttpResponse("Duplicate restaurant!")
        except:
            Restaurant.objects.create(
                name = name,
                picture = picture,
                cuisine = cuisine,
                rating = rating,
            )
    return render(request, 'delivery/admin_home.html', {'username': 'admin'})

def open_show_restaurant(request):
    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html',{"restaurantList" : restaurantList, 'username': 'admin'})

def open_update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    return render(request, 'delivery/update_restaurant.html', {"restaurant" : restaurant, 'username': 'admin'})

def update_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')
        
        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()

    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html',{"restaurantList" : restaurantList, 'username': 'admin'})


def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    restaurant.delete()

    restaurantList = Restaurant.objects.all()
    return render(request, 'delivery/show_restaurants.html',{"restaurantList" : restaurantList, 'username': 'admin'})


def open_update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'delivery/update_menu.html',{"itemList" : itemList, "restaurant" : restaurant, 'username': 'admin'})
    
def update_menu(request, restaurant_id):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        vegeterian = request.POST.get('vegeterian') == 'on'
        picture = request.POST.get('picture')
        
        try:
            Item.objects.get(name = name)
            return HttpResponse("Duplicate item!")
        except:
            Item.objects.create(
                restaurant = restaurant,
                name = name,
                description = description,
                price = price,
                vegeterian = vegeterian,
                picture = picture,
            )
    return render(request, 'delivery/admin_home.html', {'username': 'admin'})

def view_menu(request, restaurant_id, username):
    restaurant = Restaurant.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    #itemList = Item.objects.all()
    return render(request, 'delivery/customer_menu.html'
                  ,{"itemList" : itemList,
                     "restaurant" : restaurant, 
                     "username":username})

def add_to_cart(request, item_id, username):
    item = Item.objects.get(id = item_id)
    customer = Customer.objects.get(username = username)

    cart, created = Cart.objects.get_or_create(customer = customer)

    cart.items.add(item)

    return redirect('show_cart', username=username)

def show_cart(request, username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer=customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'delivery/cart.html',{"itemList" : items, "total_price" : total_price, "username":username})

# Checkout View
def checkout(request, username):
    # Fetch customer and their cart
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Debug: print current Razorpay keys (temporary)
    print(f"DEBUG: RAZORPAY_KEY_ID={settings.RAZORPAY_KEY_ID!r}, RAZORPAY_KEY_SECRET={settings.RAZORPAY_KEY_SECRET!r}")

    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return render(request, 'delivery/checkout.html', {
            'username': username,
            'cart_items': cart_items,
            'total_price': total_price,
            'error': 'Payment gateway is not configured. Please contact support.',
        })

    try:
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create Razorpay order
        order_data = {
            'amount': int(total_price * 100),  # Amount in paisa
            'currency': 'INR',
            'payment_capture': '1',  # Automatically capture payment
        }
        order = client.order.create(data=order_data)
    except Exception as e:
        print("Razorpay error:", e)
        return render(request, 'delivery/checkout.html', {
            'username': username,
            'cart_items': cart_items,
            'total_price': total_price,
            'error': 'Unable to start Razorpay checkout right now. Please try again later.',
        })

    # Pass the order details to the frontend
    return render(request, 'delivery/checkout.html', {
        'username': username,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })


def place_order(request, username):
    customer = get_object_or_404(Customer, username=username)
    cart = Cart.objects.filter(customer=customer).first()

    if cart and cart.items.exists():
        total_price = cart.total_price()
        order = Order.objects.create(customer=customer, total_price=total_price)
        order.items.set(cart.items.all())
        cart.items.clear()
        
        return render(request, 'delivery/order_success.html', {
            'username': username,
            'customer': customer,
            'order': order,
        })
    
    return redirect('customer_home', username=username)

# Orders Page
def orders(request, username):
    customer = get_object_or_404(Customer, username=username)
    order_history = Order.objects.filter(customer=customer).order_by('-created_at')

    return render(request, 'delivery/orders.html', {
        'username': username,
        'order_history': order_history,
    })
