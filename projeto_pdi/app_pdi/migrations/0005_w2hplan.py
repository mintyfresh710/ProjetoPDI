# Generated by Django 4.2.23 on 2025-06-18 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_pdi', '0004_remove_usuarios_pdi'),
    ]

    operations = [
        migrations.CreateModel(
            name='W2HPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('what', models.TextField(blank=True, null=True)),
                ('why', models.TextField(blank=True, null=True)),
                ('who', models.TextField(blank=True, null=True)),
                ('when', models.TextField(blank=True, null=True)),
                ('where', models.TextField(blank=True, null=True)),
                ('how', models.TextField(blank=True, null=True)),
                ('howmuch', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
