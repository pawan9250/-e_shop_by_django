from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Customer
from .models import Product, Category, Order


# Create your views here.
def home(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()
    data = {}
    data['products'] = products
    data['categories'] = categories
    print('email: ', request.session.get('email'))
    print('name:', request.session.get('name'))  
    return render(request, 'index.html', data)


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(name__icontains=query))
    if products:
        data = {}
        data['products'] = products  
        return render(request, 'search.html', data)
    else:
        massage = 'Products Not found'
        return render(request, 'search.html', {'massage': massage} )

def signup(request):
    return render(request, 'register.html')
  
def signup_verify(request):
    postData = request.POST
    first_name = postData.get('firstname')
    last_name = postData.get('lastname')
    phone = postData.get('phone')
    email = postData.get('email')
    address = postData.get('address')
    password = postData.get('password')

    value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'address': address
        }
    customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)
    print(first_name, last_name, phone, email, password)
    customer.register()
    return redirect('/')

def login(request):
    return render(request, 'signin.html')

def login_verify(request):
    m = Customer.objects.get(email=request.POST['email'])
    if m.password == request.POST['password']:
        request.session['id'] = m.id
        request.session['name'] = m.first_name    
        return redirect('/')
    else:
        return HttpResponse("Your username and password didn't match.")

def logout(request):
    request.session.clear()
    return redirect('home')

def cart(request):
    product = request.POST.get('product')
    remove = request.POST.get('remove')
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product)
        if quantity:
            if remove:
                if quantity<=1:
                    cart.pop(product)
                else:
                    cart[product]  = quantity-1
            else:
                cart[product]  = quantity+1
        else:
            cart[product] = 1
    else:
        cart = {}
        cart[product] = 1

    request.session['cart'] = cart
    print('cart' , request.session['cart'])
    return redirect('cartpage')

def cartpage(request):
    cart = request.session.get('cart')
    if cart:
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'checkout.html' , {'products' : products})
    else:
        return render(request, 'checkout.html')

def product(request, id):
    
    product = Product.objects.get(id = id)
    print(product)
    return render(request, 'product.html', {'product': product})

def placeorder(request):
    customer = request.session.get('id')
    if customer:
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('id')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)
        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                            product=product,
                            price=product.price,
                            address=address,
                            phone=phone,
                            quantity=cart.get(str(product.id)))
        order.save()
        request.session['cart'] = {}

        return redirect('thankyou')
    else:
        return redirect('login')



def women(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        start = 27
        end = 47
        products = Product.get_all_product_by_women(start, end)
    data = {}
    data['products'] = products
    data['categories'] = categories
    print('cart: ', request.session.get('cart'))
    return render(request, 'women.html', data)

def men(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        start = 1
        end = 27
        products = Product.get_all_product_by_men(start, end)
    data = {}
    data['products'] = products
    data['categories'] = categories
    print('cart: ', request.session.get('cart'))
    return render(request, 'men.html', data)

def thankyou(request):
    return render(request, 'thankyou.html')

def contactus(request):
    return render(request, 'contactus.html')


def cartclear(request):
    request.session['cart'] = {}
    return redirect('cartpage')
# Create your views here.
