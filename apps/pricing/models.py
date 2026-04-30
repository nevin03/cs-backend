from django.db import models


class PricingPackage(models.Model):
    package_name = models.CharField(max_length=150)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in INR (or your preferred currency).",
    )
    price_label = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Optional label, e.g. '/month', 'one-time', 'starting from'.",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Highlight this package (e.g. 'Most Popular').",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pricing Package"
        verbose_name_plural = "Pricing Packages"
        ordering = ["order"]

    def __str__(self):
        return f"{self.package_name} — ₹{self.price}"


class PricingFeature(models.Model):
    package = models.ForeignKey(
        PricingPackage,
        on_delete=models.CASCADE,
        related_name="features",
    )
    feature_text = models.CharField(max_length=300)
    is_included = models.BooleanField(
        default=True,
        help_text="False = feature is NOT included (shown as crossed out).",
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Pricing Feature"
        verbose_name_plural = "Pricing Features"

    def __str__(self):
        return f"{'✓' if self.is_included else '✗'} {self.feature_text}"
