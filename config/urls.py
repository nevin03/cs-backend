"""
Root URL configuration for Portfolio Backend.

API endpoints:   /api/v1/
Swagger UI:      /api/docs/
ReDoc:           /api/redoc/
OpenAPI schema:  /api/schema/   (raw JSON/YAML — used by Swagger/ReDoc internally)
Admin:           /admin/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# ── Admin branding ─────────────────────────────────────────────────────────────
admin.site.site_header  = "Portfolio Admin"
admin.site.site_title   = "Portfolio Admin Panel"
admin.site.index_title  = "Manage Portfolio Content"


def redirect_to_docs(request):
    """Convenience: visiting / redirects to Swagger UI."""
    return HttpResponseRedirect("/api/docs/")


urlpatterns = [
    # Root → Swagger docs
    path("", redirect_to_docs),

    # Admin
    path("admin/", admin.site.urls),

    # ── API v1 ─────────────────────────────────────────────────────────────
    path("api/v1/", include("config.api_urls")),

    # ── Chatbot API ────────────────────────────────────────────────────────
    path("api/chat/", include("chatbot.urls")),

    # ── OpenAPI schema (raw) ───────────────────────────────────────────────
    # GET /api/schema/         → returns OpenAPI 3.0 JSON
    # GET /api/schema/?format=yaml → returns YAML
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # ── Swagger UI ─────────────────────────────────────────────────────────
    # Interactive docs at /api/docs/
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
            template_name="drf_spectacular/swagger_ui.html",  # custom branded template
        ),
        name="swagger-ui",
    ),

    # ── ReDoc ──────────────────────────────────────────────────────────────
    # Read-only docs at /api/redoc/
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

# Serve uploaded media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
