from rest_framework import viewsets
from .models import Oficina, Parcela, Link, Imagem, Nota
from django.contrib.auth.models import User
from .serializers import (
    UsuarioSerializer,
    OficinaSerializer,
    ParcelaSerializer,
    LinkSerializer,
    ImagemSerializer,
    NotaSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import xml.etree.ElementTree as ET
import base64


class UserInfo(APIView):  # TODO

    def get(self, request, user_id="", format=None):
        try:
            User.objects.get(id=user_id).oficina.id
            tipo_usuario = "dono"
        except Exception:
            tipo_usuario = "cliente"

        data = {
            "id_usuario": user_id,
            "tipo_usuario": tipo_usuario,
        }

        return Response(data, status=status.HTTP_200_OK)


class EntryDataOperations(APIView):  # TODO
    def get(self, request, user_id="", format=None):
        try:
            id_oficina = User.objects.get(id=user_id).oficina.id
            notas = Nota.objects.filter(oficina=id_oficina)
        except Exception:
            notas = Nota.objects.filter(cliente=user_id)

        data = NotaSerializer(notas, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, user_id, *args, **kwargs):
        try:
            # Verificar campos obrigatórios no request.data
            required_fields = [
                "nome_do_carro",
                "arquivo_xml_base64",
                "links",
                "imagens",
            ]
            missing_fields = [
                field
                for field in required_fields
                if field not in request.data or not request.data.get(field)
            ]

            if missing_fields:
                return Response(
                    {
                        "error": f"Os seguintes campos estão faltando: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Decodificar o arquivo XML de Base64
            try:
                xml_content = base64.b64decode(
                    request.data["arquivo_xml_base64"]
                ).decode("utf-8")
                tree = ET.ElementTree(ET.fromstring(xml_content))
                root = tree.getroot()
            except Exception as e:
                return Response(
                    {
                        "error": "Erro ao decodificar e processar o arquivo XML",
                        "details": str(e),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Definir o namespace do XML
            ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

            # Extrair as informações do XML
            nnf_element = root.find(".//nfe:infNFe/nfe:ide/nfe:nNF", ns)
            dhEmi_element = root.find(".//nfe:infNFe/nfe:ide/nfe:dhEmi", ns)
            vNF_element = root.find(
                ".//nfe:infNFe/nfe:total/nfe:ICMSTot/nfe:vNF", ns
            )
            nome_dest_element = root.find(
                ".//nfe:infNFe/nfe:dest/nfe:xNome", ns
            )
            cnpj_dest_element = root.find(
                ".//nfe:infNFe/nfe:dest/nfe:CNPJ", ns
            )

            # Truncar a data de emissão para os primeiros 10 caracteres (YYYY-MM-DD)
            data_emissao = (
                dhEmi_element.text[:10]
                if dhEmi_element is not None
                else "Não encontrado"
            )
            des = data_emissao.split("-")
            data_emissao = f"{des[2]}/{des[1]}/{des[0]}"
            del des
            # Dados básicos extraídos do XML
            numero_nota = (
                nnf_element.text
                if nnf_element is not None
                else "Não encontrado"
            )
            valor_nota = (
                vNF_element.text
                if vNF_element is not None
                else "Não encontrado"
            )
            nome_destinatario = (
                nome_dest_element.text
                if nome_dest_element is not None
                else "Não encontrado"
            )
            cnpj_destinatario = (
                cnpj_dest_element.text
                if cnpj_dest_element is not None
                else "Não encontrado"
            )

            # Extrair campos do request (links e imagens)
            nome_do_carro = request.data.get("nome_do_carro", "Desconhecido")

            # Buscar a oficina no banco de dados utilizando o user_id da URL
            try:
                Oficina.objects.get(id=user_id)
            except Oficina.DoesNotExist:
                return Response(
                    {"error": "Oficina não encontrada"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Verificar se o cliente (usuário) já existe com base no CNPJ
            try:
                cliente = User.objects.get(
                    username=cnpj_destinatario
                )  # Supondo que o CNPJ seja usado como username
            except User.DoesNotExist:
                # Se o cliente não existir, criar um novo
                cliente = User.objects.create(
                    username=cnpj_destinatario,
                    first_name=nome_destinatario,
                    email=f"{cnpj_destinatario}@exemplo.com",
                )

            # Processar e criar os Links
            links_data = request.data.get("links", [])
            link_ids = []
            for link in links_data:
                link_serializer = LinkSerializer(data=link)
                if link_serializer.is_valid(raise_exception=True):
                    link_obj = link_serializer.save()
                    link_ids.append(link_obj.id)

            # Processar e criar as Imagens
            imagens_data = request.data.get("imagens", [])
            imagem_ids = []
            for imagem in imagens_data:
                imagem_serializer = ImagemSerializer(data={"src": imagem})
                if imagem_serializer.is_valid(raise_exception=True):
                    imagem_obj = imagem_serializer.save()
                    imagem_ids.append(imagem_obj.id)

            # Processar as Parcelas do XML
            parcelas = root.findall(".//nfe:infNFe/nfe:cobr/nfe:dup", ns)
            parcela_objs = []
            for index, parcela in enumerate(parcelas):
                nDup = (
                    parcela.find("nfe:nDup", ns).text
                    if parcela.find("nfe:nDup", ns) is not None
                    else "Não encontrado"
                )
                dVenc = (
                    parcela.find("nfe:dVenc", ns).text
                    if parcela.find("nfe:dVenc", ns) is not None
                    else "Não encontrado"
                )
                dvs = dVenc.split("-")
                dVenc = f"{dvs[2]}/{dvs[1]}/{dvs[0]}"
                vDup = (
                    parcela.find("nfe:vDup", ns).text
                    if parcela.find("nfe:vDup", ns) is not None
                    else "Não encontrado"
                )

                parcela_data = {
                    "identificacao": nDup,
                    "parcela": f"{index+1}/{len(parcelas)}",
                    "vencimento": dVenc,
                    "situacao": "Pendente",
                    "valor": vDup,
                }

                parcela_serializer = ParcelaSerializer(data=parcela_data)
                if parcela_serializer.is_valid(raise_exception=True):
                    parcela_obj = parcela_serializer.save()
                    parcela_objs.append(parcela_obj)

            # Criar a Nota (sem Many-to-Many inicialmente)
            nota_data = {
                "numero_nota": numero_nota,
                "data_emissao": data_emissao,
                "valor_nota": valor_nota,
                "destinatario": nome_destinatario,
                "cnpj": cnpj_destinatario,
                "nome_carro": nome_do_carro,
                "cliente": cliente.id,  # Cliente encontrado ou criado
                "oficina_id": str(user_id),  # Passar o ID da oficina
            }

            nota_serializer = NotaSerializer(data=nota_data)
            if nota_serializer.is_valid(raise_exception=True):
                nota_obj = nota_serializer.save()

                # Agora associar os Many-to-Many fields
                nota_obj.parcelas.set(parcela_objs)  # Associar parcelas
                nota_obj.links.set(link_ids)  # Associar links
                nota_obj.Imagens.set(imagem_ids)  # Associar imagens

                nota_obj.save()

            return Response(
                {"message": "Nota e objetos relacionados criados com sucesso"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            transaction.set_rollback(True)
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer


class OficinaViewSet(viewsets.ModelViewSet):
    queryset = Oficina.objects.all()
    serializer_class = OficinaSerializer


class ParcelaViewSet(viewsets.ModelViewSet):
    queryset = Parcela.objects.all()
    serializer_class = ParcelaSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer


class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
