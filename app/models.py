from django.db import models

# Create your models here.



class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=80)
    email = models.CharField()
    setor = models.CharField()
    
