from django.urls import path
from . import views

urlpatterns = [
    path("", views.termsandpolicy, name="termsandpolicy"),
    path("krishi", views.krishi_pri, name="krishi_pri"),
    path("transport", views.transport_pri, name="transport_pri"),
    path("sonic", views.sonic_pri, name="sonic_pri"),
    path("skiltrix", views.skiltrix_pri, name="skiltrix_pri"),
    path("shop", views.shop_pri, name="shop_pri"),
    path("pdfix", views.pdfix_pri, name="pdfix_pri"),
    path("sfs", views.sfs, name="sfs_pri"),
    path("asmail", views.asmail, name="asmail_pri"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('disclaimer', views.disclaimer, name="disclaimer"),
]
