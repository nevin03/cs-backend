from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from .models import FeaturedProject, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    max_num = 4
    fields = ["image", "alt_text", "order", "image_preview"]
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return "—"
    image_preview.short_description = "Preview"

    def clean(self):
        # Count non-deleted images in formset
        count = sum(
            1 for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )
        if count > 4:
            raise ValidationError("A project can have at most 4 images.")


@admin.register(FeaturedProject)
class FeaturedProjectAdmin(admin.ModelAdmin):
    list_display = [
        "project_name", "tag", "is_active", "order", "image_count", "updated_at"
    ]
    list_filter = ["is_active", "tag"]
    search_fields = ["title", "project_name", "tag"]
    prepopulated_fields = {"slug": ("project_name",)}
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ProjectImageInline]
    list_editable = ["order", "is_active"]

    fieldsets = (
        ("Content", {
            "fields": ("title", "tag", "project_name", "slug", "description")
        }),
        ("Media", {
            "fields": ("project_video", "project_video_url"),
            "description": "Upload a video file OR provide an external URL. Max 4 images via the section below.",
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords"),
            "classes": ("collapse",),
        }),
        ("Display", {
            "fields": ("is_active", "order"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def image_count(self, obj):
        count = obj.images.count()
        color = "green" if count <= 4 else "red"
        return format_html('<span style="color:{}">{}/4</span>', color, count)
    image_count.short_description = "Images"
