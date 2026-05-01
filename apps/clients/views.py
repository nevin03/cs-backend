from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from .models import ClientLogo
from .serializers import ClientLogoSerializer


CLIENT_LOGO_EXAMPLE = OpenApiExample(
    "Client Logos List",
    summary="Active client logos",
    value=[
        {
            "id": 1,
            "image": "https://example.com/media/clients/logos/google.png",
            "alt_text": "Google"
        },
        {
            "id": 2,
            "image": "https://example.com/media/clients/logos/amazon.png",
            "alt_text": "Amazon"
        }
    ],
    response_only=True,
    status_codes=["200"],
)


@extend_schema_view(
    list=extend_schema(
        operation_id="clients_list",
        summary="List client logos",
        description="Returns a list of active client logos for display in sliders or sections.",
        tags=["Clients"],
        responses={
            200: OpenApiResponse(
                response=ClientLogoSerializer(many=True),
                description="List of active client logos",
                examples=[CLIENT_LOGO_EXAMPLE],
            )
        },
    )
)
class ClientLogoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """GET /api/v1/clients/ — list of active client logos."""

    serializer_class = ClientLogoSerializer

    def get_queryset(self):
        return ClientLogo.objects.filter(is_active=True)
