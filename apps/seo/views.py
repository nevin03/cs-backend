from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import SEOPage
from .serializers import SEOPageSerializer


SEO_LIST_EXAMPLE = OpenApiExample(
    "All SEO pages",
    summary="SEO data for every configured page",
    value=[
        {
            "page": "home",
            "meta_title": "Best Software Development Company in Trivandrum, Kerala",
            "meta_description": "Affordable web & mobile app development in Trivandrum. Serving Kochi, Calicut, Idukki, Wayanad.",
            "meta_keywords": "software development in Trivandrum, affordable software company Kerala, best web development company Kochi",
            "og_title": "Best Software Development Company in Kerala",
            "og_description": "Delivering world-class web & app solutions at affordable prices.",
            "og_image_url": "https://example.com/media/seo/og/home-og.jpg",
            "canonical_url": "https://yourcompany.com/",
            "updated_at": "2024-04-20T10:00:00+05:30",
        },
        {
            "page": "projects",
            "meta_title": "Our Projects — Software Portfolio | Kerala Dev Company",
            "meta_description": "Explore our portfolio of web apps, mobile applications and e-commerce platforms.",
            "meta_keywords": "software portfolio Kerala, web development projects Trivandrum",
            "og_title": "Our Work — Web & App Projects",
            "og_description": "See what we've built for clients across Kerala and beyond.",
            "og_image_url": None,
            "canonical_url": "",
            "updated_at": "2024-04-20T10:00:00+05:30",
        },
    ],
    response_only=True,
    status_codes=["200"],
)

SEO_DETAIL_EXAMPLE = OpenApiExample(
    "Home page SEO",
    summary="SEO data for the home page",
    value={
        "page": "home",
        "meta_title": "Best Software Development Company in Trivandrum, Kerala",
        "meta_description": "Affordable web & mobile app development in Trivandrum. We serve clients across Kerala — Kochi, Calicut, Idukki, Wayanad. Get a free quote today.",
        "meta_keywords": "software development in Trivandrum, affordable software company Kerala, best web development company Kochi, web development Calicut, web development Idukki, web development Wayanad, mobile app development Kerala, IT company Trivandrum",
        "og_title": "Best Software Development Company in Kerala",
        "og_description": "Delivering world-class web & app solutions across Kerala at affordable prices.",
        "og_image_url": "https://example.com/media/seo/og/home-og.jpg",
        "canonical_url": "https://yourcompany.com/",
        "updated_at": "2024-04-20T10:00:00+05:30",
    },
    response_only=True,
    status_codes=["200"],
)


@extend_schema_view(
    list=extend_schema(
        operation_id="seo_list",
        summary="List SEO metadata for all pages",
        description=(
            "Returns SEO metadata for every configured page.\n\n"
            "Pagination is disabled — typically 5 pages total. "
            "Seed default pages with:\n```\npython manage.py seed_seo\n```"
        ),
        tags=["SEO"],
        responses={
            200: OpenApiResponse(
                response=SEOPageSerializer(many=True),
                description="SEO data for all pages",
                examples=[SEO_LIST_EXAMPLE],
            ),
        },
    ),
    retrieve=extend_schema(
        operation_id="seo_detail",
        summary="Get SEO metadata for a specific page",
        description=(
            "Fetch SEO data by **page identifier**.\n\n"
            "Available page identifiers:\n"
            "| Identifier | Page |\n"
            "|------------|------|\n"
            "| `home` | Home page |\n"
            "| `projects` | Projects listing |\n"
            "| `pricing` | Pricing page |\n"
            "| `feedback` | Testimonials page |\n"
            "| `contact` | Contact page |\n\n"
            "**Next.js usage:**\n"
            "```js\n"
            "const seo = await fetch('/api/v1/seo/home/').then(r => r.json());\n"
            "// Use seo.meta_title, seo.meta_description etc. in generateMetadata()\n"
            "```"
        ),
        tags=["SEO"],
        parameters=[
            OpenApiParameter(
                "page",
                OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Page identifier: `home` | `projects` | `pricing` | `feedback` | `contact`",
                enum=["home", "projects", "pricing", "feedback", "contact"],
            )
        ],
        responses={
            200: OpenApiResponse(
                response=SEOPageSerializer,
                description="SEO data for the requested page",
                examples=[SEO_DETAIL_EXAMPLE],
            ),
            404: OpenApiResponse(description="Page not found — run `python manage.py seed_seo` to create defaults"),
        },
    ),
)
class SEOPageViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET /api/v1/seo/         — list all pages
    GET /api/v1/seo/{page}/  — single page SEO (e.g. /api/v1/seo/home/)
    """

    serializer_class = SEOPageSerializer
    pagination_class = None
    lookup_field = "page"

    def get_queryset(self):
        return SEOPage.objects.all()
