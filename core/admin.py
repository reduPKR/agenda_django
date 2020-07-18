from django.contrib import admin
from core.models import Evento

#Cabecalho do list
class EventoList(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento')
    list_filter = ('titulo','usuario',)

# Register your models here.
admin.site.register(Evento, EventoList)


