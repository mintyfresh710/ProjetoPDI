from django.db import models

class PDI(models.Model):
    nome = models.CharField(max_length=255)
    ra = models.CharField(max_length=20)
    curso = models.CharField(max_length=255)
    perfil = models.TextField()
    competencias = models.TextField()
    gaps = models.TextField(verbose_name="Gaps a serem trabalhados")
    linkedin = models.URLField(blank=True)
    certificados = models.TextField(blank=True)
    inicio_jornada = models.TextField(verbose_name="Início da Jornada de Desenvolvimento")
    desenvolvimento_permanente = models.TextField()
    jobs_desenvolvidos = models.TextField(blank=True)
    
    # Campos para os pitchs dos projetos integradores por semestre
    pitch_1_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 1º Semestre")
    pitch_2_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 2º Semestre")
    pitch_3_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 3º Semestre")
    pitch_4_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 4º Semestre")
    pitch_5_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 5º Semestre")
    pitch_6_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 6º Semestre")
    pitch_7_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 7º Semestre")
    pitch_8_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 8º Semestre")
    pitch_9_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 9º Semestre")
    pitch_10_semestre = models.TextField(blank=True, null=True, verbose_name="Pitch 10º Semestre")
    
    link_tcc = models.URLField(blank=True, null=True, verbose_name="Link do TCC")
    acoes_voluntarias = models.TextField(blank=True, null=True, verbose_name="Ações Voluntárias")
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome} - {self.ra}"
