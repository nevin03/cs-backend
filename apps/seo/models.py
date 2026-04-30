from django.db import models


class SEOPage(models.Model):
    """
    SEO metadata for named pages of the site.
    One record per page (e.g. 'home', 'projects', 'pricing', 'contact').
    """

    PAGE_CHOICES = [
        ("home",     "Home"),
        ("projects", "Projects"),
        ("pricing",  "Pricing"),
        ("feedback", "Feedback / Testimonials"),
        ("contact",  "Contact"),
    ]

    page = models.CharField(
        max_length=50,
        unique=True,
        choices=PAGE_CHOICES,
        db_index=True,
        help_text="Unique identifier for the page. Used by the frontend to fetch SEO data.",
    )
    meta_title = models.CharField(
        max_length=70,
        help_text="Page title shown in browser tab and Google results (max 70 chars).",
    )
    meta_description = models.CharField(
        max_length=160,
        help_text="Short description shown in Google snippets (max 160 chars).",
    )
    meta_keywords = models.TextField(
        blank=True,
        help_text=(
            "Comma-separated keywords.\n"
            "Suggested: software development in Trivandrum, affordable software company Kerala, "
            "best web development company Kochi, web development Calicut, web development Idukki, "
            "web development Wayanad"
        ),
    )
    og_title = models.CharField(
        max_length=100,
        blank=True,
        help_text="Open Graph title for social sharing (Facebook, LinkedIn).",
    )
    og_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Open Graph description for social sharing.",
    )
    og_image = models.ImageField(
        upload_to="seo/og/",
        blank=True,
        null=True,
        help_text="Open Graph image (1200×630px recommended).",
    )
    canonical_url = models.URLField(
        blank=True,
        help_text="Canonical URL if different from the default.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Page"
        verbose_name_plural = "SEO Pages"
        ordering = ["page"]

    def __str__(self):
        return f"SEO: {self.get_page_display()}"
