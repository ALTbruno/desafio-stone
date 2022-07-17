from rest_framework import serializers

from banco.model.cliente import Cliente

class ClienteSerializer(serializers.ModelSerializer):
	
	class Meta():
		model = Cliente
		fields = "__all__"