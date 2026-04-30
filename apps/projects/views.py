from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiExample,
    OpenApiResponse, OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes

from .models import FeaturedProject
from .serializers import FeaturedProjectSerializer, FeaturedProjectListSerializer
from .filters import FeaturedProjectFilter


# ── Inline response examples ──────────────────────────────────────────────────

PROJECT_LIST_EXAMPLE = OpenApiExample(
    "Projects list",
    summary="Paginated project list",
    value={
        "count": 3,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 1,
                "title": "E-Commerce Platform",
                "tag": "Web Development",
                "project_name": "ShopKerala",
                "slug": "shopkerala",
                "description": "A full-featured e-commerce platform built for a retailer in Kochi.",
                "thumbnail": "https://example.com/media/projects/images/shopkerala.jpg",
                "video": None,
            },
            {
                "id": 2,
                "title": "Restaurant App",
                "tag": "Mobile App",
                "project_name": "WayanadEats",
                "slug": "wayanadeats",
                "description": "Food ordering app for a restaurant chain in Wayanad.",
                "thumbnail": "https://example.com/media/projects/images/wayanadeats.jpg",
                "video": "https://example.com/media/projects/videos/wayanadeats.mp4",
            },
        ],
    },
    response_only=True,
    status_codes=["200"],
)

PROJECT_DETAIL_EXAMPLE = OpenApiExample(
    "Project detail",
    summary="Full project with images and video",
    value={
        "id": 1,
        "title": "E-Commerce Platform",
        "tag": "Web Development",
        "project_name": "ShopKerala",
        "slug": "shopkerala",
        "description": "A full-featured e-commerce platform for a Kochi retailer.",
        "images": [
            {"id": 1, "image_url": "https://example.com/media/img1.jpg", "alt_text": "Homepage", "order": 0},
            {"id": 2, "image_url": "https://example.com/media/img2.jpg", "alt_text": "Product page", "order": 1},
        ],
        "video": "https://example.com/media/projects/videos/shopkerala.mp4",
        "meta_title": "ShopKerala — E-Commerce Platform",
        "meta_description": "Online shopping platform for a Kochi-based retailer.",
        "meta_keywords": "ecommerce Kerala, online shop Kochi",
        "order": 1,
        "created_at": "2024-01-15T08:00:00+05:30",
    },
    response_only=True,
    status_codes=["200"],
)

TAGS_EXAMPLE = OpenApiExample(
    "Tags list",
    summary="All unique tags",
    value=["Mobile App", "UI/UX Design", "Web Development"],
    response_only=True,
    status_codes=["200"],
)


# ── ViewSet ───────────────────────────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(
        operation_id="projects_list",
        summary="List featured projects",
        description=(
            "Returns a paginated list of active portfolio projects.\n\n"
            "**Filtering:** Use `?tag=Web+Development` for exact match, "
            "`?tag_contains=mobile` for partial match.\n\n"
            "**Search:** `?search=ecommerce` searches title, name, tag, description.\n\n"
            "**Ordering:** `?ordering=order` (default) or `?ordering=-created_at`."
        ),
        tags=["Projects"],
        parameters=[
            OpenApiParameter("tag", OpenApiTypes.STR, description="Filter by exact tag (case-insensitive)", required=False),
            OpenApiParameter("tag_contains", OpenApiTypes.STR, description="Filter by partial tag match", required=False),
            OpenApiParameter("search", OpenApiTypes.STR, description="Search title, project name, tag, description", required=False),
            OpenApiParameter("ordering", OpenApiTypes.STR, description="Sort field. Prefix with `-` for descending. Options: `order`, `created_at`", required=False),
            OpenApiParameter("page", OpenApiTypes.INT, description="Page number", required=False),
            OpenApiParameter("page_size", OpenApiTypes.INT, description="Items per page (default 10)", required=False),
        ],
        responses={
            200: OpenApiResponse(
                response=FeaturedProjectListSerializer(many=True),
                description="Paginated project list",
                examples=[PROJECT_LIST_EXAMPLE],
            ),
        },
    ),
    retrieve=extend_schema(
        operation_id="projects_detail",
        summary="Get project detail",
        description=(
            "Returns full project data including all images (up to 4) and video.\n\n"
            "Look up by **slug** — e.g. `/api/v1/projects/shopkerala/`"
        ),
        tags=["Projects"],
        responses={
            200: OpenApiResponse(
                response=FeaturedProjectSerializer,
                description="Full project detail",
                examples=[PROJECT_DETAIL_EXAMPLE],
            ),
            404: OpenApiResponse(description="Project not found"),
        },
    ),
)
class FeaturedProjectViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET /api/v1/projects/          — paginated list
    GET /api/v1/projects/{slug}/   — full detail
    GET /api/v1/projects/tags/     — unique tag values
    """

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FeaturedProjectFilter
    search_fields = ["title", "project_name", "tag", "description"]
    ordering_fields = ["order", "created_at"]
    ordering = ["order"]
    lookup_field = "slug"

    def get_queryset(self):
        return FeaturedProject.objects.filter(is_active=True).prefetch_related("images")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FeaturedProjectSerializer
        return FeaturedProjectListSerializer

    @extend_schema(
        operation_id="projects_tags",
        summary="List all unique project tags",
        description=(
            "Returns a sorted list of all unique tag values used across active projects.\n\n"
            "Use these values with the `?tag=` filter on the projects list endpoint."
        ),
        tags=["Projects"],
        responses={
            200: OpenApiResponse(
                description="Array of unique tag strings",
                examples=[TAGS_EXAMPLE],
            ),
        },
    )
    @action(detail=False, methods=["get"], url_path="tags")
    def tags(self, request):
        tags = (
            FeaturedProject.objects.filter(is_active=True)
            .values_list("tag", flat=True)
            .distinct()
            .order_by("tag")
        )
        return Response(list(tags))
