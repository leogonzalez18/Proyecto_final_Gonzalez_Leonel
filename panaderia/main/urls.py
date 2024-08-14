from django.urls import path, include
from main.views import HomeView, AboutView, ContactView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('usuarios/', include('usuarios.urls')),
]
