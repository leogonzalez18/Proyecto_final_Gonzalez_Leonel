from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from usuarios.forms import UserRegisterForm, UserEditForm
from usuarios.models import Avatar


def login_request(request):
    msg_login = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('password')

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return render(request, "main/home.html")

        msg_login = "Usuario o contraseña incorrectos"

    form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form, "msg_login": msg_login})

def register(request):
    msg_register = ""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('home')  # Redirige a la página de inicio o a otra página de éxito
        
        # Si hay errores, concatenamos los mensajes de error en un solo string
        errors = form.non_field_errors()  # Obtiene los errores generales del formulario
        if errors:
            msg_register = " | ".join(errors)  # Combina todos los errores en un solo string

    else:
        form = UserRegisterForm()

    return render(request, "usuarios/signup.html", {"form": form, "msg_register": msg_register})


@login_required
def edit_user(request):
    usuario = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save()

            # Actualizar el avatar si se proporcionó una nueva imagen
            if form.cleaned_data.get('image'):
                # Verifica si el usuario ya tiene un avatar
                avatar, created = Avatar.objects.get_or_create(user=user)
                avatar.image = form.cleaned_data.get('image')
                avatar.save()
            
            # Redireccionar después de guardar el formulario
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('profile')  # Redirige a la página de perfil del usuario
    else:
        form = UserEditForm(instance=usuario)
    
    return render(request, 'usuarios/edit_user.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'usuarios/profile.html')

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'usuarios/change_pass.html'
    success_url = reverse_lazy('edit_user')
    
    def form_valid(self, form):
        messages.success(self.request, 'Contraseña cambiada exitosamente.')
        return super().form_valid(form)

