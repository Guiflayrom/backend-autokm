from rest_framework import serializers
from .models import Oficina, Parcela, Link, Imagem, Nota
from django.contrib.auth.models import User


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class OficinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oficina
        fields = [
            "id",
            "dono",
            "logo",
            "empresa_nome",
            "cnpj",
            "home_link",
            "maps_link",
        ]


class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = [
            "id",
            "identificacao",
            "parcela",
            "vencimento",
            "situacao",
            "valor",
            "file_url",
            "numeracao_boleto",
        ]


class LinkSerializer(serializers.ModelSerializer):
    file64 = serializers.CharField(read_only=True)

    class Meta:
        model = Link
        fields = ["title", "filename", "file_url", "size", "file64"]


class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = ["id", "src"]


class NotaSerializer(serializers.ModelSerializer):
    oficina_id = serializers.UUIDField(write_only=True)
    oficina = OficinaSerializer(read_only=True)
    parcelas = ParcelaSerializer(read_only=True, many=True)
    links = LinkSerializer(read_only=True, many=True)
    Imagens = ImagemSerializer(read_only=True, many=True)

    class Meta:
        model = Nota
        fields = [
            "id",
            "numero_nota",
            "data_emissao",
            "valor_nota",
            "destinatario",
            "cnpj",
            "nome_carro",
            "cliente",
            "oficina_id",
            "oficina",
            "parcelas",
            "links",
            "Imagens",
        ]
