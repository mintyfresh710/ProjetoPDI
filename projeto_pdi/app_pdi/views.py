from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Usuarios
from django.shortcuts import render

def show_login(request):
    return render(request, 'index.html', {'page': 'login'})

def show_cadastro(request):
    return render(request, 'index.html', {'page': 'cadastro'})

def show_home(request):
    return render(request, 'home.html', {'page': 'home'})

def cadastro_view(request):

    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar = request.POST.get("confirmar_senha")

        # Check if all fields are filled
        if not nome or not email or not senha or not confirmar:
            return render(request, "index.html", {"erro": "Todos os campos devem ser preenchidos", "page": "cadastro"})

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return render(request, "index.html", {"erro": "Email inválido", "page": "cadastro"})

        # Check if passwords match
        if senha != confirmar:
            return render(request, "index.html", {"erro": "Senhas não coincidem", "page": "cadastro"})

        # Password strength check (minimum length example)
        if len(senha) < 8:
            return render(request, "index.html", {"erro": "A senha deve ter pelo menos 8 caracteres", "page": "cadastro"})

        # Create and save the user
        usuario = Usuarios(
            nome=nome,
            email=email,
            senha=make_password(senha)
        )
        usuario.save()
        return redirect('login')

    return render(request, "index.html", {"page": "cadastro"})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            usuario = Usuarios.objects.get(email=email)
            if check_password(senha, usuario.senha):
                return redirect('home')
            else:
                erro = "Senha incorreta"
        except Usuarios.DoesNotExist:
            erro = "Usuário não encontrado"

        return render(request, "index.html", {"erro": erro})

    return render(request, "index.html")

def plano_individual(request):
    """View para a página de plano individual"""
    return render(request, 'plano_individual.html')

def conta(request):
    """View para a página de conta do usuário"""
    return render(request, 'conta.html')