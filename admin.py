from django.contrib import admin
from .models import Resultado # Supondo que seu modelo se chame Resultado

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('jogador', 'pontuacao', 'tempo_total', 'fase_alcancada', 'data')
    search_fields = ('jogador',)
    ordering = ('-pontuacao', 'tempo_total')