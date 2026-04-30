"""
Usage:
    python manage.py seed_seo

Creates default SEOPage records for all pages if they don't already exist.
Safe to re-run — won't overwrite existing data.
"""

from django.core.management.base import BaseCommand
from apps.seo.models import SEOPage

DEFAULTS = [
    {
        "page": "home",
        "meta_title": "Best Software Development Company in Trivandrum, Kerala",
        "meta_description": (
            "Affordable web & mobile app development in Trivandrum. "
            "We serve clients across Kerala — Kochi, Calicut, Idukki, Wayanad. "
            "Get a free quote today."
        ),
        "meta_keywords": (
            "software development in Trivandrum, affordable software company Kerala, "
            "best web development company Kochi, web development Calicut, "
            "web development Idukki, web development Wayanad, "
            "mobile app development Kerala, IT company Trivandrum"
        ),
        "og_title": "Best Software Development Company in Kerala",
        "og_description": "Delivering world-class web & app solutions across Kerala at affordable prices.",
    },
    {
        "page": "projects",
        "meta_title": "Our Projects — Software Portfolio | Kerala Dev Company",
        "meta_description": (
            "Explore our portfolio of web apps, mobile applications, and e-commerce platforms "
            "built for clients across Trivandrum, Kochi, Calicut and beyond."
        ),
        "meta_keywords": (
            "software portfolio Kerala, web development projects Trivandrum, "
            "app development portfolio Kerala"
        ),
        "og_title": "Our Work — Web & App Projects",
        "og_description": "See what we've built for clients across Kerala and beyond.",
    },
    {
        "page": "pricing",
        "meta_title": "Affordable Web Development Pricing Plans — Kerala",
        "meta_description": (
            "Transparent, affordable pricing for websites, web apps, and mobile apps. "
            "Serving businesses in Trivandrum, Kochi, Calicut, Wayanad, and Idukki."
        ),
        "meta_keywords": (
            "affordable web development Kerala, cheap website design Trivandrum, "
            "website pricing Kerala, software development cost Kerala"
        ),
        "og_title": "Simple, Transparent Pricing",
        "og_description": "Affordable packages for startups and established businesses across Kerala.",
    },
    {
        "page": "feedback",
        "meta_title": "Client Testimonials — Software Company Kerala",
        "meta_description": (
            "See what our clients across Kerala say about our software development services. "
            "Trusted by businesses in Trivandrum, Kochi, Calicut, Idukki, and Wayanad."
        ),
        "meta_keywords": (
            "software company reviews Kerala, web development testimonials Trivandrum, "
            "client feedback Kerala IT company"
        ),
        "og_title": "What Our Clients Say",
        "og_description": "Real testimonials from businesses we've helped across Kerala.",
    },
    {
        "page": "contact",
        "meta_title": "Contact Us — Software Development Trivandrum, Kerala",
        "meta_description": (
            "Get in touch with our team for web development, app development, or digital solutions. "
            "Serving all of Kerala — Trivandrum, Kochi, Calicut, Wayanad, Idukki."
        ),
        "meta_keywords": (
            "contact software company Trivandrum, hire web developer Kerala, "
            "web development enquiry Kochi, IT company contact Kerala"
        ),
        "og_title": "Let's Build Something Great Together",
        "og_description": "Reach out to our team for a free consultation on your next project.",
    },
]


class Command(BaseCommand):
    help = "Seed default SEO data for all portfolio pages."

    def handle(self, *args, **options):
        created = 0
        for data in DEFAULTS:
            _, was_created = SEOPage.objects.get_or_create(
                page=data["page"],
                defaults={k: v for k, v in data.items() if k != "page"},
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  Created SEO for: {data['page']}"))
            else:
                self.stdout.write(f"  Skipped (already exists): {data['page']}")

        self.stdout.write(self.style.SUCCESS(f"\nDone — {created} new SEO page(s) seeded."))
