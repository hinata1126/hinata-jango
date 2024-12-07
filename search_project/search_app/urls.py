from django.urls import path 
from . import views 
from django.contrib.auth.views import LoginView


urlpatterns = [ 
    path('', views.search_view, name='search_view'),
    path('search/', views.search_view, name='search_view'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete', views.product_delete, name='product_delete'),
    path('product/', views.product_list, name='product_list'), 
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
]