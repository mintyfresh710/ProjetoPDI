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

def show_pi(request):
    """View para a página de plano individual"""
    return render(request, 'plano_individual.html')

def show_conta(request):
    try:
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login')

        usuario = Usuarios.objects.get(id_usuario=usuario_id)

        data_apenas = usuario.data_criacao_conta.date()

        context = {
            'nome': usuario.nome,
            'email': usuario.email,
            'data': data_apenas,
        }

        return render(request, 'conta/conta.html', context)

    except Usuarios.DoesNotExist:
        return redirect('login')

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
        return redirect('app_pdi:login')

    return render(request, "index.html", {"page": "cadastro"})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            usuario = Usuarios.objects.get(email=email)
            if check_password(senha, usuario.senha):
                request.session['usuario_id'] = usuario.id_usuario
                return redirect("app_pdi:home")
            else:
                erro = "Senha incorreta"
        except Usuarios.DoesNotExist:
            erro = "Usuário não encontrado"

        return render(request, "index.html", {"erro": erro})

    return render(request, "index.html")

def editar_perfil(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuarios.objects.get(id_usuario=usuario_id)

    if request.method == "POST":
        novo_nome = request.POST.get("nome")
        novo_email = request.POST.get("email")

        if novo_nome:
            usuario.nome = novo_nome
        if novo_email:
            usuario.email = novo_email

        usuario.save()
        return redirect('conta')

    return render(request, 'conta/editar_perfil.html', {'usuario': usuario})


def alterar_senha(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuarios.objects.get(id_usuario=usuario_id)

    if request.method == "POST":
        senha_atual = request.POST.get("senha_atual")
        nova_senha = request.POST.get("nova_senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        if not check_password(senha_atual, usuario.senha):
            return render(request, "conta/alterar_senha.html", {"erro": "Senha atual incorreta"})

        if nova_senha != confirmar_senha:
            return render(request, "conta/alterar_senha.html", {"erro": "Senhas não coincidem"})

        usuario.senha = make_password(nova_senha)
        usuario.save()
        return redirect('conta')

    return render(request, 'conta/alterar_senha.html')