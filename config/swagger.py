from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# setting for "drf-yasg" - lib for generate real Swagger/OpenAPI 2.0
# specifications from a Django Rest Framework API.

schema_view = get_schema_view(
    openapi.Info(
        title="Kerfuffle social-network",
        default_version='v1',
        description="""`Django rest framework API`
                  The `swagger-ui` view can be found [here](/swagger).
                  The `ReDoc` view can be found [here](/redoc).""",
        contact=openapi.Contact(url="https://www.linkedin.com/in/viashino/"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'swagger^(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]