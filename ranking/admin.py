from django.contrib import admin
from .models import Resultado

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('jogador', 'pontuacao', 'tempo_segundos')