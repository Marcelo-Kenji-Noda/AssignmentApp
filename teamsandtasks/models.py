from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length = 200)
    def __str__(self):
        return self.nome
    
    def __unicode__(self):
        return self.nome

class Tarefa(models.Model):
    nome = models.CharField(max_length=200)
    categoria = models.ManyToManyField(Categoria)
    tempo_estimado = models.FloatField(default=0.0)
    tem_resp = models.BooleanField(default=False)
    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    NUCLEO_CHOICES = (
        ('EST','Estatística'),
        ('COMP','Computação'),
    )
    DIRETORIA_CHOICES = (
        ('MKT','Marketing'),
        ('GP', 'Gestão de Pessoas'),
        ('VND','Vendas'),
        ('QLD','Qualidade'),
        ('PRS','Presidência'),
        ('JFN','Jurídico Financeiro')
    )
    nome = models.CharField(max_length=30)
    nucleo = models.CharField(max_length=4, choices=NUCLEO_CHOICES)
    diretoria = models.CharField(max_length=4, choices= DIRETORIA_CHOICES)
    tarefas = models.ManyToManyField(Tarefa, blank = True)

    def __str__(self):
        return self.nome


class Nota(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null = True)
    value = models.IntegerField(default = 0)
    pessoa = models.ForeignKey(Pessoa,on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.pessoa.nome + ': ' + self.categoria.nome+ ' ' + str(self.value)
# Create your models here.
