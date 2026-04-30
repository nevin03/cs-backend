# Portfolio Backend — Django + DRF

Production-ready REST API for a company portfolio website, built with Django 4.2 and Django REST Framework.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Quick Start](#quick-start)
3. [API Reference](#api-reference)
4. [Example API Responses](#example-api-responses)
5. [Admin Dashboard](#admin-dashboard)
6. [Next.js Frontend Integration](#nextjs-frontend-integration)
7. [SEO Strategy for Kerala / Trivandrum Keywords](#seo-strategy)
8. [Production Deployment](#production-deployment)

---

## Project Structure

```
portfolio_backend/
├── config/
│   ├── settings.py          # All settings, env-var driven
│   ├── urls.py              # Root URL config + Swagger docs
│   ├── api_urls.py          # API v1 router (all apps registered here)
│   └── wsgi.py
├── apps/
│   ├── home/                # Home video API
│   ├── projects/            # Featured projects API (with images/video)
│   ├── feedback/            # Client testimonials API
│   ├── pricing/             # Pricing packages API
│   ├── contact/             # Contact form POST API
│   └── seo/                 # SEO metadata API + seed command
├── requirements.txt
├── .env.example
└── manage.py
```

---

## Quick Start

### 1. Clone & create virtual environment

```bash
git clone <your-repo-url>
cd portfolio_backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your values (DB credentials, SECRET_KEY, etc.)
```

Minimum required fields in `.env`:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Create PostgreSQL database

```bash
# In psql
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
```

### 4. Run migrations & setup

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_seo          # Seeds default SEO pages with Kerala keywords
python manage.py collectstatic
```

### 5. Run development server

```bash
python manage.py runserver
```

Visit:
- **API:** `http://localhost:8000/api/v1/`
- **Swagger UI:** `http://localhost:8000/api/docs/`
- **Admin:** `http://localhost:8000/admin/`

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/home-video/` | Active home page video |
| GET | `/api/v1/projects/` | Paginated list of featured projects |
| GET | `/api/v1/projects/{slug}/` | Single project detail |
| GET | `/api/v1/projects/tags/` | List of unique project tags |
| GET | `/api/v1/feedback/` | Client testimonials |
| GET | `/api/v1/pricing/` | Pricing packages with features |
| POST | `/api/v1/contact/` | Submit contact enquiry |
| GET | `/api/v1/seo/` | SEO data for all pages |
| GET | `/api/v1/seo/{page}/` | SEO data for a specific page |

### Query Parameters

**Projects list** (`GET /api/v1/projects/`)
| Param | Example | Description |
|-------|---------|-------------|
| `tag` | `?tag=Web+Development` | Filter by exact tag |
| `tag_contains` | `?tag_contains=mobile` | Filter by partial tag match |
| `search` | `?search=ecommerce` | Full-text search |
| `ordering` | `?ordering=order` | Sort by field |
| `page` | `?page=2` | Page number |
| `page_size` | `?page_size=5` | Items per page |

---

## Example API Responses

### GET `/api/v1/home-video/`
```json
{
  "id": 1,
  "video_url": "https://your-bucket.s3.ap-south-1.amazonaws.com/media/hero.mp4",
  "is_active": true,
  "updated_at": "2024-04-20T10:30:00Z"
}
```

### GET `/api/v1/projects/`
```json
{
  "count": 12,
  "next": "http://localhost:8000/api/v1/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "E-Commerce Platform",
      "tag": "Web Development",
      "project_name": "ShopKerala",
      "slug": "shopkerala",
      "description": "A full-featured e-commerce platform built for a retailer in Kochi.",
      "thumbnail": "https://example.com/media/projects/images/shopkerala.jpg",
      "video": null
    }
  ]
}
```

### GET `/api/v1/projects/shopkerala/`
```json
{
  "id": 1,
  "title": "E-Commerce Platform",
  "tag": "Web Development",
  "project_name": "ShopKerala",
  "slug": "shopkerala",
  "description": "A full-featured e-commerce platform built for a retailer in Kochi.",
  "images": [
    {
      "id": 1,
      "image_url": "https://example.com/media/projects/images/img1.jpg",
      "alt_text": "Homepage screenshot",
      "order": 0
    },
    {
      "id": 2,
      "image_url": "https://example.com/media/projects/images/img2.jpg",
      "alt_text": "Product listing page",
      "order": 1
    }
  ],
  "video": "https://example.com/media/projects/videos/shopkerala-demo.mp4",
  "meta_title": "ShopKerala — E-Commerce Platform",
  "meta_description": "E-commerce solution for a Kochi retailer.",
  "meta_keywords": "ecommerce Kerala, online shop Kochi",
  "order": 1,
  "created_at": "2024-01-15T08:00:00Z"
}
```

### GET `/api/v1/projects/tags/`
```json
["Mobile App", "UI/UX Design", "Web Development"]
```

### GET `/api/v1/feedback/`
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "client_image_url": "https://example.com/media/feedback/avatars/john.jpg",
      "client_name": "Arun Menon",
      "company_name": "TechStart Kochi",
      "description": "Outstanding work! Delivered our web platform ahead of schedule.",
      "rating": 5
    }
  ]
}
```

### GET `/api/v1/pricing/`
```json
[
  {
    "id": 1,
    "package_name": "Starter",
    "price": "15000.00",
    "price_label": "one-time",
    "is_featured": false,
    "features": [
      { "id": 1, "feature_text": "5-page responsive website", "is_included": true, "order": 0 },
      { "id": 2, "feature_text": "Mobile optimised", "is_included": true, "order": 1 },
      { "id": 3, "feature_text": "E-commerce integration", "is_included": false, "order": 2 }
    ]
  },
  {
    "id": 2,
    "package_name": "Business",
    "price": "35000.00",
    "price_label": "one-time",
    "is_featured": true,
    "features": [
      { "id": 4, "feature_text": "Unlimited pages", "is_included": true, "order": 0 },
      { "id": 5, "feature_text": "E-commerce integration", "is_included": true, "order": 1 },
      { "id": 6, "feature_text": "Custom admin dashboard", "is_included": true, "order": 2 }
    ]
  }
]
```

### POST `/api/v1/contact/`

**Request:**
```json
{
  "name": "Priya Nair",
  "email": "priya@example.com",
  "project_enquiry": "I need a mobile app for my restaurant business in Wayanad."
}
```

**Response (201):**
```json
{
  "message": "Thank you! Your enquiry has been received. We'll get back to you shortly.",
  "id": 42
}
```

**Response (429 — rate limited):**
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

**Response (400 — validation error):**
```json
{
  "project_enquiry": ["Please describe your project in at least 20 characters."]
}
```

### GET `/api/v1/seo/home/`
```json
{
  "page": "home",
  "meta_title": "Best Software Development Company in Trivandrum, Kerala",
  "meta_description": "Affordable web & mobile app development in Trivandrum. We serve clients across Kerala — Kochi, Calicut, Idukki, Wayanad. Get a free quote today.",
  "meta_keywords": "software development in Trivandrum, affordable software company Kerala, best web development company Kochi, web development Calicut, web development Idukki, web development Wayanad, mobile app development Kerala, IT company Trivandrum",
  "og_title": "Best Software Development Company in Kerala",
  "og_description": "Delivering world-class web & app solutions across Kerala at affordable prices.",
  "og_image_url": "https://example.com/media/seo/og/home-og.jpg",
  "canonical_url": "https://yourcompany.com/",
  "updated_at": "2024-04-20T10:00:00Z"
}
```

---

## Admin Dashboard

Visit `/admin/` after creating a superuser.

| Section | What you can manage |
|---------|-------------------|
| **Home Videos** | Upload/swap the hero video; toggle active |
| **Featured Projects** | Add projects, drag-drop images (max 4), add video |
| **Client Feedback** | Add/edit testimonials, reorder, toggle visibility |
| **Pricing Packages** | Add packages + feature lists inline |
| **Contact Submissions** | View enquiries, mark as read, add internal notes |
| **SEO Pages** | Edit meta title/description/keywords/OG per page |

---

## Next.js Frontend Integration

### 1. Fetching APIs

Create a central API helper in `lib/api.js`:

```javascript
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchHomeVideo() {
  const res = await fetch(`${BASE_URL}/home-video/`, { next: { revalidate: 3600 } });
  if (!res.ok) return null;
  return res.json();
}

export async function fetchProjects({ tag, page = 1, pageSize = 9 } = {}) {
  const params = new URLSearchParams({ page, page_size: pageSize });
  if (tag) params.append('tag', tag);
  const res = await fetch(`${BASE_URL}/projects/?${params}`, { next: { revalidate: 600 } });
  return res.json();
}

export async function fetchProject(slug) {
  const res = await fetch(`${BASE_URL}/projects/${slug}/`, { next: { revalidate: 600 } });
  if (!res.ok) return null;
  return res.json();
}

export async function fetchProjectTags() {
  const res = await fetch(`${BASE_URL}/projects/tags/`, { next: { revalidate: 3600 } });
  return res.json();
}

export async function fetchFeedback() {
  const res = await fetch(`${BASE_URL}/feedback/`, { next: { revalidate: 3600 } });
  return res.json();
}

export async function fetchPricing() {
  const res = await fetch(`${BASE_URL}/pricing/`, { next: { revalidate: 3600 } });
  return res.json();
}

export async function fetchSEO(page) {
  const res = await fetch(`${BASE_URL}/seo/${page}/`, { next: { revalidate: 3600 } });
  if (!res.ok) return null;
  return res.json();
}

export async function submitContact(data) {
  const res = await fetch(`${BASE_URL}/contact/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw json;        // Throw validation errors to the form handler
  return json;
}
```

### 2. Dynamic SEO with Next.js App Router (metadata API)

In `app/page.js` (home page):

```javascript
import { fetchSEO } from '@/lib/api';

export async function generateMetadata() {
  const seo = await fetchSEO('home');
  if (!seo) return {};

  return {
    title: seo.meta_title,
    description: seo.meta_description,
    keywords: seo.meta_keywords,
    alternates: {
      canonical: seo.canonical_url || 'https://yoursite.com/',
    },
    openGraph: {
      title: seo.og_title || seo.meta_title,
      description: seo.og_description || seo.meta_description,
      images: seo.og_image_url ? [{ url: seo.og_image_url, width: 1200, height: 630 }] : [],
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title: seo.og_title || seo.meta_title,
      description: seo.og_description || seo.meta_description,
      images: seo.og_image_url ? [seo.og_image_url] : [],
    },
  };
}

export default async function HomePage() {
  // ... your page component
}
```

For a dynamic project page in `app/projects/[slug]/page.js`:

```javascript
import { fetchProject, fetchSEO } from '@/lib/api';

export async function generateMetadata({ params }) {
  const project = await fetchProject(params.slug);
  if (!project) return { title: 'Project Not Found' };

  return {
    title: project.meta_title || project.project_name,
    description: project.meta_description || project.description?.slice(0, 160),
    keywords: project.meta_keywords,
    openGraph: {
      title: project.meta_title || project.project_name,
      description: project.meta_description,
      images: project.images?.[0]?.image_url
        ? [{ url: project.images[0].image_url }]
        : [],
    },
  };
}
```

### 3. Using with Next.js Pages Router (next/head)

```javascript
import Head from 'next/head';
import { fetchSEO } from '@/lib/api';

export async function getStaticProps() {
  const seo = await fetchSEO('home');
  return { props: { seo }, revalidate: 3600 };
}

export default function HomePage({ seo }) {
  return (
    <>
      <Head>
        <title>{seo?.meta_title}</title>
        <meta name="description" content={seo?.meta_description} />
        <meta name="keywords" content={seo?.meta_keywords} />
        {seo?.canonical_url && <link rel="canonical" href={seo.canonical_url} />}
        <meta property="og:title" content={seo?.og_title || seo?.meta_title} />
        <meta property="og:description" content={seo?.og_description} />
        {seo?.og_image_url && <meta property="og:image" content={seo.og_image_url} />}
      </Head>
      {/* Page content */}
    </>
  );
}
```

---

## SEO Strategy

The `seed_seo` command pre-populates keywords targeting your local market. Key phrases to maintain:

| Target Area | Keywords |
|-------------|----------|
| Primary | `software development in Trivandrum` |
| State-wide | `affordable software company Kerala` |
| Kochi | `best web development company Kochi` |
| Calicut | `web development Calicut`, `IT company Calicut` |
| Idukki | `web development Idukki`, `app development Idukki` |
| Wayanad | `web development Wayanad`, `software company Wayanad` |
| General | `mobile app development Kerala`, `IT company Kerala` |

**Additional recommendations:**
- Add your business to **Google Business Profile** with all five Kerala city areas listed as service areas.
- Create individual landing pages per city (`/web-development-kochi`, `/web-development-calicut`) each with unique content.
- Use **Next.js ISR** (`revalidate: 3600`) so SEO content updates from the admin without a full redeploy.

---

## Production Deployment

### Environment changes for production

```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
USE_S3=True                         # Switch to S3 for media
CORS_ALLOWED_ORIGINS=https://yourfrontend.com
```

### Run with Gunicorn

```bash
gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120
```

### Nginx config snippet

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}

location /static/ {
    alias /path/to/portfolio_backend/staticfiles/;
}
```

### Checklist before going live

- [ ] `SECRET_KEY` is a long random string (never reused)
- [ ] `DEBUG=False`
- [ ] `USE_S3=True` and S3 bucket is configured
- [ ] `CORS_ALLOWED_ORIGINS` only includes your Next.js domain
- [ ] `python manage.py collectstatic` has been run
- [ ] SSL certificate is in place (HSTS will activate automatically)
- [ ] Superuser password is strong
- [ ] Run `python manage.py check --deploy` and fix any warnings
