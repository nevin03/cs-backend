from django.db import models


class HomeVideo(models.Model):
    """
    Stores the hero/background video shown on the home page.
    Only ONE record should be active at any time.
    """

    video_file = models.FileField(
        upload_to="hero_videos/",
        null=True,
        blank=True,
        help_text="Upload a video file from your computer.",
    )
    video_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Alternatively, provide a direct URL to a video (e.g. S3 link). Used if no file is uploaded.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Only one video should be active. Saving a new active video will deactivate others.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Video"
        verbose_name_plural = "Home Videos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Home Video ({self.get_video_url()[:60]})"

    def get_video_url(self):
        """Returns the best available video source."""
        if self.video_file:
            return self.video_file.url
        return self.video_url or ""

    def save(self, *args, **kwargs):
        # Enforce single active video
        if self.is_active:
            HomeVideo.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
