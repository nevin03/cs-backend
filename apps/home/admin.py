from django.contrib import admin
from .models import HomeVideo


@admin.register(HomeVideo)
class HomeVideoAdmin(admin.ModelAdmin):
    list_display = ["id", "get_video_display", "is_active", "updated_at"]
    list_filter = ["is_active"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("video_file", "video_url", "is_active")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_video_display(self, obj):
        return obj.get_video_url()[:50]
    get_video_display.short_description = "Video Source"

    def save_model(self, request, obj, form, change):
        # Admin also respects the single-active constraint
        super().save_model(request, obj, form, change)
