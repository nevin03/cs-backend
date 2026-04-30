from rest_framework import viewsets, mixins
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse

from .models import PricingPackage
from .serializers import PricingPackageSerializer


PRICING_EXAMPLE = OpenApiExample(
    "Pricing packages",
    summary="All active packages with features",
    value=[
        {
            "id": 1,
            "package_name": "Starter",
            "price": "15000.00",
            "price_label": "one-time",
            "is_featured": False,
            "features": [
                {"id": 1, "feature_text": "5-page responsive website", "is_included": True, "order": 0},
                {"id": 2, "feature_text": "Mobile optimised", "is_included": True, "order": 1},
                {"id": 3, "feature_text": "E-commerce integration", "is_included": False, "order": 2},
            ],
        },
        {
            "id": 2,
            "package_name": "Business",
            "price": "35000.00",
            "price_label": "one-time",
            "is_featured": True,
            "features": [
                {"id": 4, "feature_text": "Unlimited pages", "is_included": True, "order": 0},
                {"id": 5, "feature_text": "E-commerce integration", "is_included": True, "order": 1},
                {"id": 6, "feature_text": "Custom admin dashboard", "is_included": True, "order": 2},
                {"id": 7, "feature_text": "3 months free support", "is_included": True, "order": 3},
            ],
        },
        {
            "id": 3,
            "package_name": "Enterprise",
            "price": "75000.00",
            "price_label": "starting from",
            "is_featured": False,
            "features": [
                {"id": 8, "feature_text": "Custom web application", "is_included": True, "order": 0},
                {"id": 9, "feature_text": "Mobile app (iOS + Android)", "is_included": True, "order": 1},
                {"id": 10, "feature_text": "6 months dedicated support", "is_included": True, "order": 2},
            ],
        },
    ],
    response_only=True,
    status_codes=["200"],
)


@extend_schema_view(
    list=extend_schema(
        operation_id="pricing_list",
        summary="List pricing packages",
        description=(
            "Returns all active pricing packages with their nested feature lists.\n\n"
            "**`is_featured: true`** — highlight this package (e.g. 'Most Popular' badge).\n\n"
            "**`is_included: false`** on a feature — show it as crossed-out / not included.\n\n"
            "Pagination is disabled for this endpoint (typically 2–5 packages)."
        ),
        tags=["Pricing"],
        responses={
            200: OpenApiResponse(
                response=PricingPackageSerializer(many=True),
                description="List of pricing packages",
                examples=[PRICING_EXAMPLE],
            ),
        },
    )
)
class PricingPackageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """GET /api/v1/pricing/ — all active packages with features."""

    serializer_class = PricingPackageSerializer
    pagination_class = None

    def get_queryset(self):
        return PricingPackage.objects.filter(is_active=True).prefetch_related("features")
