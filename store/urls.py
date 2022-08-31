from django.contrib import admin
from django.urls import path
from .views import Index
from .views import  Login, Signup, logout, backto, Cart, OrderView
from .middlewares.auth import auth_middleware
from .views import CheckOut

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view()),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('backto', backto, name='backto'),
    path('cart', Cart.as_view(), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders')

]