from django.db import models

class ClientLogo(models.Model):
    logo = models.ImageField(upload_to="clients/logos/", help_text="Client logo / icon.")
    alt_text = models.CharField(max_length=200, help_text="Alternative text for the logo.")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client Logo"
        verbose_name_plural = "Client Logos"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.alt_text
