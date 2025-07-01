from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Usuarios
from .models import W2HPlan
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

def show_login(request):
    return render(request, 'index.html', {'page': 'login'})

def show_cadastro(request):
    return render(request, 'index.html', {'page': 'cadastro'})

def show_home(request):

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('app_pdi:login')

    usuario = Usuarios.objects.get(id_usuario=usuario_id)

    return render(request, 'home.html', {'page': 'home'})

def show_pi(request):

    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('app_pdi:login')

    usuario = Usuarios.objects.get(id_usuario=usuario_id)

    return render(request, 'plano_individual.html')

def show_conta(request):
    try:
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('app_pdi:login')

        usuario = Usuarios.objects.get(id_usuario=usuario_id)

        data_apenas = usuario.data_criacao_conta.date()

        context = {
            'nome': usuario.nome,
            'email': usuario.email,
            'data': data_apenas,
        }

        return render(request, 'conta/conta.html', context)

    except Usuarios.DoesNotExist:
        return redirect('app_pdi:login')

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
        return redirect('app_pdi:login')

    usuario = Usuarios.objects.get(id_usuario=usuario_id)

    if request.method == "POST":
        novo_nome = request.POST.get("nome")
        novo_email = request.POST.get("email")

        if novo_nome:
            usuario.nome = novo_nome
        if novo_email:
            usuario.email = novo_email

        usuario.save()
        return redirect('app_pdi:conta')

    return render(request, 'conta/editar_perfil.html', {'usuario': usuario})


def alterar_senha(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('app_pdi:login')

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
        return redirect('app_pdi:conta')

    return render(request, 'conta/alterar_senha.html')

# Função 5w2h

@csrf_exempt
@require_http_methods(["GET", "POST"])
def w2h_plans_api(request):
    """API para listar e criar planos 5W2H por usuário"""
    # Verificar se o usuário está logado
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return JsonResponse({'success': False, 'message': 'Usuário não está logado'}, status=401)
    
    try:
        usuario = Usuarios.objects.get(id_usuario=usuario_id)
    except Usuarios.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Usuário não encontrado'}, status=404)
    
    if request.method == "GET":
        plans = W2HPlan.objects.filter(usuario=usuario).order_by('-created_at')
        plans_data = []
        for plan in plans:
            plans_data.append({
                'id': plan.id,
                'what': plan.what,
                'why': plan.why,
                'who': plan.who,
                'when': plan.when,
                'where': plan.where,
                'how': plan.how,
                'howmuch': plan.howmuch,
                'created_at': plan.created_at.strftime('%d/%m/%Y %H:%M')
            })
        return JsonResponse({'plans': plans_data})
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            plan = W2HPlan.objects.create(
                usuario=usuario,
                what=data.get('what', ''),
                why=data.get('why', ''),
                who=data.get('who', ''),
                when=data.get('when', ''),
                where=data.get('where', ''),
                how=data.get('how', ''),
                howmuch=data.get('howmuch', '')
            )
            return JsonResponse({
                'success': True,
                'message': 'Plano salvo com sucesso!',
                'plan': {
                    'id': plan.id,
                    'what': plan.what,
                    'why': plan.why,
                    'who': plan.who,
                    'when': plan.when,
                    'where': plan.where,
                    'how': plan.how,
                    'howmuch': plan.howmuch,
                    'created_at': plan.created_at.strftime('%d/%m/%Y %H:%M')
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def w2h_plan_detail_api(request, plan_id):
    """API para obter, atualizar e deletar um plano específico do usuário logado"""
    # Verificar se o usuário está logado
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return JsonResponse({'success': False, 'message': 'Usuário não está logado'}, status=401)
    
    try:
        usuario = Usuarios.objects.get(id_usuario=usuario_id)
    except Usuarios.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Usuário não encontrado'}, status=404)
    
    try:
        # Filtrar o plano pelo ID e pelo usuário logado
        plan = W2HPlan.objects.get(id=plan_id, usuario=usuario)
    except W2HPlan.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Plano não encontrado ou não pertence ao usuário'}, status=404)
    
    if request.method == "GET":
        return JsonResponse({
            'plan': {
                'id': plan.id,
                'what': plan.what,
                'why': plan.why,
                'who': plan.who,
                'when': plan.when,
                'where': plan.where,
                'how': plan.how,
                'howmuch': plan.howmuch,
                'created_at': plan.created_at.strftime('%d/%m/%Y %H:%M')
            }
        })
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            plan.what = data.get('what', plan.what)
            plan.why = data.get('why', plan.why)
            plan.who = data.get('who', plan.who)
            plan.when = data.get('when', plan.when)
            plan.where = data.get('where', plan.where)
            plan.how = data.get('how', plan.how)
            plan.howmuch = data.get('howmuch', plan.howmuch)
            plan.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Plano atualizado com sucesso!',
                'plan': {
                    'id': plan.id,
                    'what': plan.what,
                    'why': plan.why,
                    'who': plan.who,
                    'when': plan.when,
                    'where': plan.where,
                    'how': plan.how,
                    'howmuch': plan.howmuch,
                    'created_at': plan.created_at.strftime('%d/%m/%Y %H:%M')
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    elif request.method == "DELETE":
        plan.delete()
        return JsonResponse({'success': True, 'message': 'Plano excluído com sucesso!'})


