from rest_framework import viewsets, mixins
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse

from .models import HomeVideo
from .serializers import HomeVideoSerializer


HOME_VIDEO_EXAMPLE = OpenApiExample(
    "Active home video",
    summary="Single active hero video",
    description="The currently active background/hero video for the home page.",
    value={
        "id": 1,
        "video_url": "https://your-bucket.s3.ap-south-1.amazonaws.com/media/hero.mp4",
        "is_active": True,
        "updated_at": "2024-04-20T10:30:00+05:30",
    },
    response_only=True,
    status_codes=["200"],
)

NOT_FOUND_EXAMPLE = OpenApiExample(
    "No active video",
    summary="No video configured yet",
    value={"detail": "No active home video configured."},
    response_only=True,
    status_codes=["404"],
)


@extend_schema_view(
    list=extend_schema(
        operation_id="home_video_get",
        summary="Get active home video",
        description=(
            "Returns the single currently active hero video for the home page.\n\n"
            "Only **one** video can be active at a time. Activating a new video "
            "automatically deactivates the previous one.\n\n"
            "Returns `404` if no video has been configured yet."
        ),
        tags=["Home"],
        responses={
            200: OpenApiResponse(
                response=HomeVideoSerializer,
                description="Active home video",
                examples=[HOME_VIDEO_EXAMPLE],
            ),
            404: OpenApiResponse(
                description="No active video configured",
                examples=[NOT_FOUND_EXAMPLE],
            ),
        },
    )
)
class HomeVideoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """GET /api/v1/home-video/ — returns the single active hero video."""

    serializer_class = HomeVideoSerializer
    pagination_class = None

    def get_queryset(self):
        return HomeVideo.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        if instance is None:
            return Response({"detail": "No active home video configured."}, status=404)
        return Response(self.get_serializer(instance).data)
