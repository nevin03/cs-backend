from django.contrib import admin
from django.utils.html import format_html
from .models import SEOPage


@admin.register(SEOPage)
class SEOPageAdmin(admin.ModelAdmin):
    list_display = [
        "page", "meta_title", "title_len", "description_len", "updated_at"
    ]
    readonly_fields = ["updated_at", "og_preview"]
    search_fields = ["page", "meta_title", "meta_description"]

    fieldsets = (
        ("Page", {"fields": ("page",)}),
        ("Core SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords", "canonical_url"),
            "description": (
                "Title: max 70 chars | Description: max 160 chars. "
                "Keywords tip: 'software development in Trivandrum', "
                "'affordable software company Kerala', "
                "'best web development company Kochi / Calicut / Idukki / Wayanad'"
            ),
        }),
        ("Open Graph (Social Sharing)", {
            "fields": ("og_title", "og_description", "og_image", "og_preview"),
            "classes": ("collapse",),
        }),
        ("Meta", {"fields": ("updated_at",), "classes": ("collapse",)}),
    )

    def title_len(self, obj):
        length = len(obj.meta_title)
        color = "green" if length <= 70 else "red"
        return format_html('<span style="color:{}">{}/70</span>', color, length)
    title_len.short_description = "Title Length"

    def description_len(self, obj):
        length = len(obj.meta_description)
        color = "green" if length <= 160 else "red"
        return format_html('<span style="color:{}">{}/160</span>', color, length)
    description_len.short_description = "Desc Length"

    def og_preview(self, obj):
        if obj.og_image:
            return format_html(
                '<img src="{}" style="max-width:300px;border-radius:6px;" />', obj.og_image.url
            )
        return "No OG image uploaded."
    og_preview.short_description = "OG Image Preview"
