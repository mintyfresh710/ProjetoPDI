from django.db import models

# Create your models here.
class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    email = models.EmailField((""), max_length=254)
    senha = models.CharField(max_length=128)
    data_criacao_conta = models.DateTimeField(auto_now_add=True)


class W2HPlan(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='planos_5w2h')
    what = models.TextField(blank=True, null=True)
    why = models.TextField(blank=True, null=True)
    who = models.TextField(blank=True, null=True)
    when = models.TextField(blank=True, null=True)
    where = models.TextField(blank=True, null=True)
    how = models.TextField(blank=True, null=True)
    howmuch = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"5W2H Plan - {self.usuario.nome} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

