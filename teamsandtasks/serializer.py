from django.utils import tree
from rest_framework import serializers
from teamsandtasks.models import Tarefa, Pessoa, Categoria, Nota

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = '__all__'

class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'

class NotasPorPessoaSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.ReadOnlyField(source='categoria.nome')
    class Meta:
        model = Nota
        fields = ['categoria_nome','value']

class CalculateValuesSerializer(serializers.Serializer):
    value = serializers.FloatField()

class TodasNotasSerializer(serializers.Serializer):
    pessoa = serializers.IntegerField()
    data = serializers.ListField()