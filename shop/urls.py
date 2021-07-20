from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='shopHome'),
    path('about/', views.about, name='AboutUs'),
    path('contact/', views.contact, name='ContactUs'),
    path('tracker/', views.tracker, name='tracker'),
    path('search/', views.search, name='search'),
    path('products/<int:id>', views.productview, name='productview'),
    path('checkout/', views.checkout, name='chekout'),


]