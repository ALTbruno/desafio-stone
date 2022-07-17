from django.contrib import admin

from banco.models import Cliente, Conta

class ClienteAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'sobrenome', 'data_nascimento', 'cpf', 'email')

class ContaAdmin(admin.ModelAdmin):
	list_display = ('id', 'agencia', 'numero', 'saldo', 'cliente')

# Register your models here.
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Conta, ContaAdmin)
