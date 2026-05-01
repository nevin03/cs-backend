from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class ProjectTag(models.Model):
    """
    Tags attached to a FeaturedProject.
    """
    project = models.ForeignKey(
        "FeaturedProject",
        on_delete=models.CASCADE,
        related_name="tags",
    )
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Project Tag"
        verbose_name_plural = "Project Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name


class FeaturedProject(models.Model):
    """
    A featured project shown in the portfolio section.
    Supports up to 4 images and 1 video.
    """

    title = models.CharField(max_length=200)
    # tags is now a related manager via ProjectTag
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    project_image_item = models.ImageField(
        upload_to="projects/banners/",
        blank=True,
        null=True,
        help_text="Banner image for the project.",
    )
    banner_video = models.FileField(
        upload_to="projects/videos/",
        blank=True,
        null=True,
        help_text="Banner video for the project.",
    )
    industry = models.CharField(max_length=100, blank=True, null=True)


    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated keywords.",
    )

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Featured Project"
        verbose_name_plural = "Featured Projects"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.project_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.project_name)
            slug = base
            counter = 1
            while FeaturedProject.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def video(self):
        """Returns the banner_video URL."""
        return self.banner_video.url if self.banner_video else None


class ProjectImage(models.Model):
    """
    Images attached to a FeaturedProject.
    Max 4 images per project (enforced in clean()).
    """

    project = models.ForeignKey(
        FeaturedProject,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="projects/images/")
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"Image for {self.project.project_name} ({self.order})"

    def clean(self):
        # Enforce max 4 images per project
        if self.pk is None:  # only on create
            existing = ProjectImage.objects.filter(project=self.project).count()
            if existing >= 4:
                raise ValidationError(
                    "A project can have at most 4 images. Remove an existing image first."
                )


class ProjectLink(models.Model):
    """
    External links for a FeaturedProject (e.g. Website, App Store, Play Store).
    """

    project = models.ForeignKey(
        FeaturedProject,
        on_delete=models.CASCADE,
        related_name="links",
    )
    label = models.CharField(max_length=100, help_text="Link label, e.g. 'Website', 'App Store'.")
    url = models.URLField(max_length=500)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Project Link"
        verbose_name_plural = "Project Links"

    def __str__(self):
        return f"{self.label} for {self.project.project_name}"
