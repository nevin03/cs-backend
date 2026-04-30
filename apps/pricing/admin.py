from django.contrib import admin
from .models import PricingPackage, PricingFeature


class PricingFeatureInline(admin.TabularInline):
    model = PricingFeature
    extra = 3
    fields = ["feature_text", "is_included", "order"]


@admin.register(PricingPackage)
class PricingPackageAdmin(admin.ModelAdmin):
    list_display = ["package_name", "price", "price_label", "is_featured", "is_active", "order"]
    list_filter = ["is_active", "is_featured"]
    list_editable = ["order", "is_active", "is_featured"]
    inlines = [PricingFeatureInline]
    readonly_fields = ["created_at"]
