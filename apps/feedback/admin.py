from django.contrib import admin
from django.utils.html import format_html
from .models import ClientFeedback


@admin.register(ClientFeedback)
class ClientFeedbackAdmin(admin.ModelAdmin):
    list_display = ["client_name", "company_name", "rating", "is_active", "order", "avatar_preview"]
    list_filter = ["is_active", "rating"]
    search_fields = ["client_name", "company_name"]
    list_editable = ["order", "is_active"]
    readonly_fields = ["avatar_preview", "created_at"]

    def avatar_preview(self, obj):
        if obj.client_image:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;border-radius:50%;" />', obj.client_image.url
            )
        return "—"
    avatar_preview.short_description = "Photo"
