from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from productos.views import ProductsListView, ProductCreateView, ProductDeleteView, ProductUpdateView, CartListView, CartItemCreateView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products-list'),
    path('add/', ProductCreateView.as_view(), name='product-add'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    
    # Carrito de compras
    path('cart/', CartListView.as_view(), name='cart-list'),
    path('cart/add/<int:pk>/', CartItemCreateView.as_view(), name='cart-item-add'),
    path('cart/update/<int:pk>/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('cart/delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart-item-delete'),
    ]
