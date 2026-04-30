from django.db import models


class ClientFeedback(models.Model):
    client_image = models.ImageField(
        upload_to="feedback/avatars/",
        blank=True,
        null=True,
        help_text="Client profile photo (optional).",
    )
    client_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=200)
    description = models.TextField(help_text="Client testimonial / feedback text.")
    rating = models.PositiveSmallIntegerField(
        default=5,
        help_text="Star rating out of 5.",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client Feedback"
        verbose_name_plural = "Client Feedbacks"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.client_name} — {self.company_name}"
