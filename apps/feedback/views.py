from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse

from .models import ClientFeedback
from .serializers import ClientFeedbackSerializer


FEEDBACK_LIST_EXAMPLE = OpenApiExample(
    "Testimonials list",
    summary="Client testimonials",
    value={
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 1,
                "image_url": "https://example.com/media/feedback/arun.jpg",
                "client_name": "Arun Menon",
                "company_name": "TechStart Kochi",
                "description": "Outstanding work! Delivered our web platform ahead of schedule and within budget.",
                "rating": 5,
            },
            {
                "id": 2,
                "image_url": None,
                "client_name": "Divya Krishnan",
                "company_name": "WayanadEats",
                "description": "The mobile app they built for us has transformed our business. Highly recommend!",
                "rating": 5,
            },
        ],
    },
    response_only=True,
    status_codes=["200"],
)


from rest_framework.pagination import PageNumberPagination

class FeedbackPagination(PageNumberPagination):
    page_size = 25


@extend_schema_view(
    list=extend_schema(
        operation_id="feedback_list",
        summary="List client testimonials",
        description=(
            "Returns a paginated list of active client testimonials.\n\n"
            "`image_url` will be `null` if no photo was uploaded for that client."
        ),
        tags=["Feedback"],
        responses={
            200: OpenApiResponse(
                response=ClientFeedbackSerializer(many=True),
                description="Paginated testimonials",
                examples=[FEEDBACK_LIST_EXAMPLE],
            ),
        },
    )
)
class ClientFeedbackViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """GET /api/v1/feedback/ — paginated list of active testimonials."""

    serializer_class = ClientFeedbackSerializer
    pagination_class = FeedbackPagination

    def get_queryset(self):
        return ClientFeedback.objects.filter(is_active=True)
