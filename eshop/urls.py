from django.urls import path
from eshop import views
from . import settings

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("signup_verify", views.signup_verify, name="signup_verify"),
    path("login_verify", views.login_verify, name="login_verify"),
    path("cart", views.cart, name="cart"), 
    path("cartpage", views.cartpage, name="cartpage"), 
    path("product/<int:id>", views.product, name="product"),  
    path("placeorder", views.placeorder, name="placeorder"), 
    path("search", views.search, name="search"),    
    path("logout", views.logout, name="logout"),    
    path("men", views.men, name="men"),    
    path("cartclear", views.cartclear, name="cartclear"), 
    path("women", views.women, name="women"), 
    path("thankyou", views.thankyou, name="thankyou"), 
    path("contactus", views.contactus, name="contactus"), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
