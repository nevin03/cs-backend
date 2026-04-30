"""
API v1 URL routing.
All app routers are registered here.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.home.views import HomeVideoViewSet
from apps.projects.views import FeaturedProjectViewSet
from apps.feedback.views import ClientFeedbackViewSet
from apps.pricing.views import PricingPackageViewSet
from apps.contact.views import ContactSubmissionViewSet
from apps.seo.views import SEOPageViewSet

router = DefaultRouter()
router.register(r"home-video",      HomeVideoViewSet,          basename="home-video")
router.register(r"projects",        FeaturedProjectViewSet,    basename="projects")
router.register(r"feedback",        ClientFeedbackViewSet,     basename="feedback")
router.register(r"pricing",         PricingPackageViewSet,     basename="pricing")
router.register(r"contact",         ContactSubmissionViewSet,  basename="contact")
router.register(r"seo",             SEOPageViewSet,            basename="seo")

urlpatterns = [
    path("", include(router.urls)),
]
