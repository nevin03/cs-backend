from django.db import models


class ContactSubmission(models.Model):
    """Stores all contact form submissions from the website."""

    name = models.CharField(max_length=200)
    email = models.EmailField()
    project_enquiry = models.TextField(help_text="Description of the project or enquiry.")

    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_read = models.BooleanField(default=False, help_text="Mark as read in admin.")
    notes = models.TextField(
        blank=True,
        help_text="Internal admin notes about this enquiry.",
    )

    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.submitted_at:%Y-%m-%d %H:%M}"
