from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer

# Create your views here.

def index(request):
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
    return render(request, 'index.html', data)


def validateCustomer(customer):
    error_message = None
    if not customer.first_name:
        error_message = "First Name required !!"
    elif len(customer.first_name) < 4:
        error_message = 'FirstName must be atleast 4'
    elif not customer.last_name:
        error_message = 'LastName required !!'
    elif len(customer.last_name) < 4:
        error_message = 'Must be atleast of 4 char'
    elif not customer.phone:
        error_message = 'Phone no required'
    elif len(customer.phone) != 10:
        error_message = 'Indian phone number is of length 10'
    elif not customer.password:
        error_message = 'Password Required'
    elif len(customer.password) < 4:
        error_message = 'Password length must be greater than 4'
    elif customer.isExists():
        error_message = 'already signed-up with this email'


def registerUser(request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # validation

        value = {
            'first_name ' : first_name,
            'last_name' : last_name,
            'phone' : phone,
            'email' : email
        }

        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

        error_message = validateCustomer(customer)


        # saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')

        else:
            data = {
                'error' : error_message,
                'values' : value
            }
            return render(request, 'signup.html', data)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        return registerUser(request)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        return render(request, 'login.html', {'error' : error_message})


