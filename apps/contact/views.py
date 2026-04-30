from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
from .throttles import ContactRateThrottle


# ── Request examples ──────────────────────────────────────────────────────────

CONTACT_REQUEST_EXAMPLE = OpenApiExample(
    "Standard enquiry",
    summary="Typical project enquiry",
    value={
        "name": "Priya Nair",
        "email": "priya@example.com",
        "project_enquiry": "I need a mobile app for my restaurant business in Wayanad. Looking for iOS and Android.",
    },
    request_only=True,
)

CONTACT_SUCCESS_EXAMPLE = OpenApiExample(
    "Submission accepted",
    summary="201 — Successfully submitted",
    value={
        "message": "Thank you! Your enquiry has been received. We'll get back to you shortly.",
        "id": 42,
    },
    response_only=True,
    status_codes=["201"],
)

CONTACT_VALIDATION_ERROR_EXAMPLE = OpenApiExample(
    "Validation error",
    summary="400 — Invalid input",
    value={
        "email": ["Enter a valid email address."],
        "project_enquiry": ["Please describe your project in at least 20 characters."],
    },
    response_only=True,
    status_codes=["400"],
)

CONTACT_RATE_LIMITED_EXAMPLE = OpenApiExample(
    "Rate limited",
    summary="429 — Too many requests",
    value={"detail": "Request was throttled. Expected available in 3541 seconds."},
    response_only=True,
    status_codes=["429"],
)


@extend_schema_view(
    create=extend_schema(
        operation_id="contact_submit",
        summary="Submit a contact enquiry",
        description=(
            "Creates a new contact form submission and stores it in the database.\n\n"
            "### Validation rules\n"
            "- `name` — required, min 2 characters\n"
            "- `email` — required, must be a valid email address\n"
            "- `project_enquiry` — required, min 20 characters\n\n"
            "### Spam protection\n"
            "Rate-limited to **5 requests per hour per IP address**. "
            "Exceeding this returns HTTP `429`.\n\n"
            "The submitter's IP address is recorded server-side (not returned in the response)."
        ),
        tags=["Contact"],
        examples=[
            CONTACT_REQUEST_EXAMPLE,
            CONTACT_SUCCESS_EXAMPLE,
            CONTACT_VALIDATION_ERROR_EXAMPLE,
            CONTACT_RATE_LIMITED_EXAMPLE,
        ],
        responses={
            201: OpenApiResponse(description="Enquiry submitted successfully", examples=[CONTACT_SUCCESS_EXAMPLE]),
            400: OpenApiResponse(description="Validation error", examples=[CONTACT_VALIDATION_ERROR_EXAMPLE]),
            429: OpenApiResponse(description="Rate limit exceeded", examples=[CONTACT_RATE_LIMITED_EXAMPLE]),
        },
    )
)
class ContactSubmissionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """POST /api/v1/contact/ — submit a contact form enquiry."""

    serializer_class = ContactSubmissionSerializer
    throttle_classes = [ContactRateThrottle]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def perform_create(self, serializer):
        serializer.save(ip_address=self.get_client_ip(self.request))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Thank you! Your enquiry has been received. We'll get back to you shortly.",
                "id": serializer.instance.id,
            },
            status=status.HTTP_201_CREATED,
        )
