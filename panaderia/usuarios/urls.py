from django.urls import path
from django.contrib.auth.views import LogoutView
from usuarios import views

urlpatterns = [
    path('login/', views.login_request, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', LogoutView.as_view(template_name='main/home.html'), name="logout"),
    path('profile/', views.profile, name="profile"),
    path('edit_user/', views.edit_user, name="edit_user"),
    path('change_password/', views.ChangePasswordView.as_view(), name="change_password"),
]
