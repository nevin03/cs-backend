from django.contrib import admin
from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "short_enquiry", "submitted_at", "is_read", "ip_address"]
    list_filter = ["is_read", "submitted_at"]
    search_fields = ["name", "email", "project_enquiry"]
    readonly_fields = ["name", "email", "project_enquiry", "submitted_at", "ip_address"]
    list_editable = ["is_read"]
    ordering = ["-submitted_at"]

    fieldsets = (
        ("Submission", {
            "fields": ("name", "email", "project_enquiry", "submitted_at", "ip_address")
        }),
        ("Admin", {
            "fields": ("is_read", "notes"),
        }),
    )

    def short_enquiry(self, obj):
        return obj.project_enquiry[:80] + ("…" if len(obj.project_enquiry) > 80 else "")
    short_enquiry.short_description = "Enquiry"

    def has_add_permission(self, request):
        # Submissions are created via API only, not manually from admin
        return False
