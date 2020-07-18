from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Evento(models.Model):
    titulo = models.CharField(max_length = 100)
    descricao = models.TextField(blank = True, null=True)
    local = models.TextField()
    data_evento = models.DateTimeField()
    data_criacao = models.DateTimeField(auto_now = True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)

    # Evita que o migrate nomeie automaticamente como core_evento
    class Meta:
        db_table = 'evento'
    
    #Visualizacao do evento para n ficar como object
    def __str__(self):
        return self.titulo

    def get_data(self):
        return self.data_evento.strftime('%d/%m/%Y - %H:%M')
    
    def get_data_input(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')
