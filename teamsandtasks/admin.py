from django.contrib import admin
from teamsandtasks.models import Pessoa, Tarefa, Categoria, Nota

class Pessoas(admin.ModelAdmin):
    list_display = ('id','nome','nucleo','diretoria')
    list_display_links = ('id','nome')
    search_fields = ('nome',)

class Tarefas(admin.ModelAdmin):
    search_fields = ('id','nome',)
    
class Categorias(admin.ModelAdmin):
    search_fields = ('nome',)

admin.site.register(Pessoa, Pessoas)
admin.site.register(Tarefa, Tarefas)
admin.site.register(Categoria, Categorias)
admin.site.register(Nota)
# Register your models here.
