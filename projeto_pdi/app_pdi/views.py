from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuarios

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

        if senha == confirmar:
            usuario = Usuarios(
                nome=nome,
                email=email,
                senha=make_password(senha)
            )
            usuario.save()
            return redirect('login')
        else:
            return render(request, "index.html", {"erro": "Senhas não coincidem"})

    return render(request, "index.html", {"page": "cadastro"})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            usuario = Usuarios.objects.get(email=email)
            if check_password(senha, usuario.senha):
                # Login bem-sucedido
                return redirect('home')
            else:
                erro = "Senha incorreta"
        except Usuarios.DoesNotExist:
            erro = "Usuário não encontrado"

        return render(request, "index.html", {"erro": erro})

    return render(request, "index.html")

