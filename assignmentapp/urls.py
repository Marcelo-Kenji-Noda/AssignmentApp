from django.contrib import admin
from django.urls import path, include
from teamsandtasks.views import PessoaViewset, CategoriaViewset, TarefaViewset, NotaViewset, NotasPorPessoa, CalculateValues,GetChoiceFieldsDiretorias, GetChoiceFieldsNucleos, AllNotasFields,CategoriaComNotas
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pessoas',PessoaViewset, basename='Pessoas')
router.register('tarefas',TarefaViewset, basename='Tarefas')
router.register('categorias',CategoriaViewset, basename='Categorias')
router.register('notas',NotaViewset, basename='Notas')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('pessoa/<int:pk>/notas/',NotasPorPessoa.as_view()),
    path('calculatevalues',CalculateValues.as_view()),
    path('lista/diretorias',GetChoiceFieldsDiretorias.as_view()),
    path('lista/nucleos',GetChoiceFieldsNucleos.as_view()),
    path('allnotas/',AllNotasFields.as_view()),
    path('allnotas/<int:pk>/',AllNotasFields.as_view()),
    path('categoriacomnotas/<int:pk>/',CategoriaComNotas.as_view())
]
