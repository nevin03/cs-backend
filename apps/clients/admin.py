from django.contrib import admin
from django.utils.html import format_html
from .models import ClientLogo


@admin.register(ClientLogo)
class ClientLogoAdmin(admin.ModelAdmin):
    list_display = ["alt_text", "is_active", "order", "logo_preview"]
    list_editable = ["is_active", "order"]
    search_fields = ["alt_text"]

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:40px; max-width:120px; object-fit:contain;" />', 
                obj.logo.url
            )
        return "—"
    logo_preview.short_description = "Logo Preview"
