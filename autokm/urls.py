from django.contrib import admin  # Importar o módulo admin do Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    UsuarioViewSet,
    OficinaViewSet,
    ParcelaViewSet,
    LinkViewSet,
    ImagemViewSet,
    NotaViewSet,
    EntryDataOperations,
    UserInfo,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Sua API",
        default_version="v1",
        description="Documentação da API",
        terms_of_service="https://www.seusite.com/terms/",
        contact=openapi.Contact(email="contato@seusite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r"usuarios", UsuarioViewSet)
router.register(r"oficinas", OficinaViewSet)
router.register(r"parcelas", ParcelaViewSet)
router.register(r"links", LinkViewSet)
router.register(r"imagens", ImagemViewSet)
router.register(r"notas", NotaViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/data/<user_id>/",
        EntryDataOperations.as_view(),
        name="entry_data",
    ),
    path(
        "api/info/<user_id>/",
        UserInfo.as_view(),
        name="entry_data",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/auth/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/auth/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
