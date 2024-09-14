from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Oficina(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    dono = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="oficina"
    )  # noqa
    logo = models.CharField(max_length=1000, blank=True, null=True)
    empresa_nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=255)
    home_link = models.CharField(max_length=1000, blank=True, null=True)
    maps_link = models.CharField(max_length=1000, blank=True, null=True)


class Parcela(models.Model):
    identificacao = models.CharField(max_length=255)
    parcela = models.CharField(max_length=50)
    vencimento = models.CharField(max_length=50)
    situacao = models.CharField(
        max_length=50,
        choices=(
            ("Atrasado", "Atrasado"),
            ("Pendente", "Pendente"),
            ("Pago", "Pago"),
        ),
    )
    valor = models.CharField(max_length=255)


class Link(models.Model):
    title = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    file_url = models.CharField(max_length=1000)
    size = models.IntegerField()


class Imagem(models.Model):
    src = models.CharField(max_length=1000)


class Nota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    numero_nota = models.CharField(max_length=255)
    data_emissao = models.CharField(max_length=10)
    valor_nota = models.CharField(max_length=255)
    destinatario = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=255)
    nome_carro = models.CharField(max_length=255)
    cliente = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="notas"
    )
    oficina = models.ForeignKey(
        Oficina, on_delete=models.PROTECT, related_name="notas"
    )
    parcelas = models.ManyToManyField(
        Parcela,
        related_name="nota",
        blank=True,
    )
    links = models.ManyToManyField(
        Link,
        related_name="nota",
        blank=True,
    )
    Imagens = models.ManyToManyField(
        Imagem,
        related_name="nota",
        blank=True,
    )
