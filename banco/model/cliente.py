from tkinter import CASCADE
from django.db import models

# Create your models here.
class Cliente(models.Model):
	id = models.AutoField(primary_key=True)
	nome = models.CharField(max_length=50)
	sobrenome = models.CharField(max_length=150)
	data_nascimento = models.DateField(null=True)
	cpf = models.CharField(max_length=11)
	email = models.CharField(max_length=255)
	senha = models.CharField(max_length=255, default='')

	def __str__(self) -> str:
		return self.nome
