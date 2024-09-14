from django.contrib import admin
from .models import Oficina, Parcela, Link, Imagem, Nota


@admin.register(Oficina)
class OficinaAdmin(admin.ModelAdmin):
    list_display = ("id", "empresa_nome", "dono", "cnpj")
    search_fields = ("empresa_nome", "cnpj")
    list_filter = ("dono",)
    ordering = ("empresa_nome",)


@admin.register(Parcela)
class ParcelasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "identificacao",
        "parcela",
        "vencimento",
        "situacao",
        "valor",
    )
    search_fields = ("identificacao",)
    ordering = ("identificacao",)


@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ("id", "src")
    search_fields = ("src",)
    ordering = ("src",)


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "numero_nota",
        "data_emissao",
        "valor_nota",
        "destinatario",
        "cnpj",
        "nome_carro",
        "oficina",
    )
    search_fields = ("numero_nota", "destinatario", "cnpj", "nome_carro")
    list_filter = ("oficina",)
    ordering = ("data_emissao",)
