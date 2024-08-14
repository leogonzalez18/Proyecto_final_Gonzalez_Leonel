from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from productos.models import Product, Cart, CartItem
from productos.forms import ProductForm


# ---------------Manejo de productos---------------
class ProductsListView(ListView):
    model = Product
    template_name = 'productos/products_list.html'
    context_object_name = 'products'

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'productos/product_add.html'
    success_url = reverse_lazy('products-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Producto añadido con éxito.')
        return response
    
    def test_func(self):
        return self.request.user.is_superuser
    
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'productos/product_update.html'
    success_url = reverse_lazy('products-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Producto actualizado con éxito.')
        return response
    
    def test_func(self):
        return self.request.user.is_superuser

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'productos/product_delete.html'
    success_url = reverse_lazy('products-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Producto eliminado con éxito.')
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_superuser

# ---------------Manejo del carrito---------------
class CartListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'productos/cart_list.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        # Calcula el monto total del carrito
        total_amount = sum(item.get_total_price() for item in cart.items.all())
        context['total_amount'] = total_amount
        return context
    
    def post(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        if cart.items.exists():
            # Vaciar el carrito después de la compra
            cart.items.all().delete()
            messages.success(request, f"Se realizó el pedido correctamente. Se envió un correo a {request.user.email} con el comprobante de pago.")
        else:
            messages.error(request, "El carrito está vacío. No se pudo realizar el pedido.")
        return redirect('cart-list')

class CartItemCreateView(LoginRequiredMixin, CreateView):
    model = CartItem
    fields = ['quantity']
    template_name = 'productos/cart_item_add.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += form.cleaned_data['quantity']
        cart_item.save()
        messages.success(self.request, f'Producto {product.name} añadido al carrito con éxito.')
        return redirect('cart-list')

class CartItemUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem
    fields = ['quantity']
    template_name = 'productos/cart_item_update.html'
    success_url = reverse_lazy('cart-list')
    
    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
        if created:
            cart_item.quantity = form.cleaned_data['quantity']
        else:
            cart_item.quantity += form.cleaned_data['quantity']
    
        cart_item.save()
        messages.success(self.request, f'Producto {product.name} añadido al carrito con éxito.')
        return redirect('cart-list')

class CartItemDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = 'productos/cart_item_delete.html'
    success_url = reverse_lazy('cart-list')
    
    def form_valid(self, form):
        cart_item = self.get_object()
        product_name = cart_item.product.name
        messages.success(self.request, f'Producto {product_name} eliminado del carrito correctamente.')
        return super().form_valid(form)
    