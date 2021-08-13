from rest_framework.views import APIView
from django.db.models import query
from rest_framework import viewsets, generics
from teamsandtasks.models import Pessoa, Tarefa, Categoria, Nota
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import PessoaSerializer, TarefaSerializer,CategoriaSerializer, NotaSerializer, NotasPorPessoaSerializer, CalculateValuesSerializer, TodasNotasSerializer
from rest_framework import status

from rest_framework.response import Response

import numpy as np

from .utils import calculate_all

class PessoaViewset(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
    #authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated]

class TarefaViewset(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    #authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated]

class CategoriaViewset(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    #authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated]

class NotaViewset(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    #authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated]

class NotasPorPessoa(generics.ListAPIView):
    serializer_class = NotasPorPessoaSerializer
    def get_queryset(self):
        queryset = Nota.objects.filter(pessoa__id = self.kwargs['pk'])
        return queryset
    
    #authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated]

class CalculateValues(APIView):
    def post(self,request, *args, **kwargs):
        custom_data = request.data
        data = calculate_all(individual_resource=custom_data['b'])
        return Response(data)

class GetChoiceFieldsDiretorias(APIView):
    def get(self,request, *args, **kwrags):
        data = []
        Dir_escolhas = list(Pessoa.DIRETORIA_CHOICES)

        for item in Dir_escolhas:
            new_obj = {}
            new_obj['code'] = item[0]
            new_obj['nome'] = item[1]
            data.append(new_obj)
        return Response(data)

class GetChoiceFieldsNucleos(APIView):
    def get(self,request, *args, **kwrags):
        data = []
        Nucleo_escolhas = list(Pessoa.NUCLEO_CHOICES)

        for item in Nucleo_escolhas:
            new_obj = {}
            new_obj['code'] = item[0]
            new_obj['nome'] = item[1]
            data.append(new_obj)
        return Response(data)

class AllNotasFields(APIView):
    def post(self, request, *args, **kwargs):
        """
        Data = {"pessoa":id, "data":[{"categoria":2,"value":2}]}
        """
        data = request.data
        pessoa_pk = data["pessoa"]
        for i in range(len(data['data'])):
            if Nota.objects.filter(pessoa = Pessoa.objects.get(pk=pessoa_pk),categoria = Categoria.objects.get(pk=data["data"][i]['categoria'])).exists():
                aux_id = Nota.objects.filter(pessoa = Pessoa.objects.get(pk=pessoa_pk),categoria = Categoria.objects.get(pk=data["data"][i]['categoria'])).values_list('pk', flat=True)
                aux=  Nota.objects.get(pk=aux_id[0])
                aux.value = data["data"][i]['value']
                aux.save()
            else:
                aux = Nota(pessoa = Pessoa.objects.get(pk=pessoa_pk),categoria = Categoria.objects.get(pk=data["data"][i]['categoria']),value = data["data"][i]['value'])
                aux.save()
        return Response(data)
    def delete(self,request,pk,*args,**kwrags):
        Nota.objects.filter(pessoa = Pessoa.objects.get(pk=pk)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoriaComNotas(APIView):
    def get(self, request,pk, *args, **kwargs):
        data = []
        for category in Categoria.objects.all():
            aux_obj = {}
            if Nota.objects.filter(pessoa = Pessoa.objects.get(pk=pk),categoria = Categoria.objects.get(pk=category.id)).exists():
                aux_id = Nota.objects.filter(pessoa = Pessoa.objects.get(pk=pk),categoria = Categoria.objects.get(pk=category.id)).values_list('pk', flat=True)
                aux=  Nota.objects.get(pk=aux_id[0])
                aux_obj['categoria_id'] = category.id
                aux_obj['categoria'] = category.nome
                aux_obj['value'] = aux.value
            else:
                aux_obj['categoria_id'] = category.id
                aux_obj['categoria']=category.nome
                aux_obj['value'] = 0
            data.append(aux_obj)
        return Response(data)

# Create your views here.
