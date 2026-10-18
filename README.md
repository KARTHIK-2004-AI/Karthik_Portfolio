# Karthik Portfolio

A personal portfolio site for **Karthik Aarupalli** — an AI Engineer / Full-Stack Developer.

It is a single Django project that serves both:

- a **vanilla HTML/CSS/JS frontend** (hash-routed SPA, served from `index.html`), and
- a **Django REST Framework API + Django Admin CMS** that stores and serves all of the site's content.

> This README is the single source of truth for the project. The older
> `README_BACKEND.md`, `QUICKSTART.md`, `RESUME_FIX.md`, `RESUME_UPLOAD_GUIDE.md`
> and `GLOWY_WAVES_IMPLEMENTATION.md` files described an outdated layout and
> have been removed.

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Backend | Django 5.0.1, Django REST Framework 3.14, SimpleJWT |
| Frontend | Static `index.html` + vanilla JS hash router |
| Styling | Hand-written CSS design system (`static/css/style.css`) |
| Admin | Django admin with a custom theme (`templates/admin/base_site.html`) |
| Database | SQLite (development) / PostgreSQL (production) |
| Static files | WhiteNoise |
| Python | 3.11+ |

---

## Quick start (local)

```powershell
# 1. Activate the virtual environment
venv\Scripts\activate

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Create your environment file
copy .env.example .env      # then edit SECRET_KEY etc.

# 4. Apply migrations
python manage.py migrate

# 5. Create an admin user
python manage.py createsuperuser

# 6. Seed the site content (profile, projects, skills, sections, settings)
python manage.py seed_data --force

# 7. Collect static files (needed for production-like runs)
python manage.py collectstatic --noinput

# 8. Run the server
python manage.py runserver
```

Then open:

- Portfolio: <http://127.0.0.1:8000/>
- Admin CMS: <http://127.0.0.1:8000/admin/>
- API root: <http://127.0.0.1:8000/api/>

On Windows you can also use `run.bat "runserver"` (it uses the bundled venv).

### Seeding

There are two management commands:

- **`python manage.py seed_data --force`** — recommended. Clears and re-seeds all
  content *including* `SiteSettings` and `Section` rows, using the correct skill
  categories (`languages`, `ai_ml`, `libraries`, `tools`).
- **`python manage.py load_default_data`** — legacy minimal seeder. It no longer
  overwrites skills with wrong categories, but `seed_data` is preferred.

---

## Project structure

```
Karthik_Portfolio/
├── manage.py
├── run.bat                     # Windows helper (uses venv)
├── urls.py                     # Root URLs: frontend, admin, API, JWT
├── wsgi.py / asgi.py
├── requirements.txt
├── .env.example
├── index.html                  # The single-page frontend
├── settings/
│   ├── base.py                 # Shared settings (DRF, JWT, email, static/media)
│   ├── development.py          # SQLite + DEBUG
│   └── production.py           # PostgreSQL, security hardening
├── portfolio/
│   ├── models.py               # Content models
│   ├── serializers.py
│   ├── views.py                # DRF ViewSets
│   ├── permissions.py          # IsAdminOrReadOnly
│   ├── urls.py                 # DRF router
│   ├── admin.py                # Admin CMS customization
│   ├── tests.py                # API smoke + selector-contract tests
│   └── management/commands/
│       ├── seed_data.py
│       └── load_default_data.py
├── static/
│   ├── css/style.css
│   └── js/{app.js, waves.js}
└── templates/admin/base_site.html
```

---

## Data model

| Model | Notes |
|-------|-------|
| `Profile` | Singleton. Name, tagline, about, avatar, resume file **or** resume URL, availability |
| `Project` | Title, description, `tech_stack` (JSON), links, thumbnail, featured flag, order, and the **Know More** detail fields (`journey`, `challenges`, `architecture`) shown in the site's project modal |
| `Skill` | Name, `category`, `icon_url`, proficiency 1–5 |
| `Experience` | Company, role, dates, `bullets` (JSON), logo, order |
| `Education` | Institution, degree, year, description |
| `ContactInfo` | Singleton. Email, phone, availability note |
| `SocialLink` | Platform, URL, optional custom icon, order |
| `SiteSettings` | Singleton. Site title, meta, theme, fonts, colours, custom CSS, draft mode |
| `Section` | Nav label, section label, heading, visibility and order for each top-level section |
| `ContactMessage` | Visitor contact form submissions |

### Skill categories

`languages`, `ai_ml`, `frontend`, `backend`, `libraries`, `tools`, `other`.
The frontend groups the site's four columns from `languages`, `ai_ml`, `libraries`
and `tools`.

---

## API

All list endpoints are paginated (`PAGE_SIZE = 100`, responses wrapped in `results`).
Reads are public; writes require an authenticated **staff** user (or JWT).

### Public (GET)

```
GET /api/profile/          # single object
GET /api/projects/         # ?category filter not applicable; reorder via POST below
GET /api/skills/           # ?category=languages|ai_ml|libraries|tools|...
GET /api/experience/
GET /api/education/
GET /api/contact/          # single object
GET /api/socials/
GET /api/site-settings/    # single object
GET /api/sections/
```

### Contact form (public)

```
POST /api/messages/        # rate-limited to 30/hour via the "contact" throttle scope
```

The notification email is sent on a background thread so SMTP latency never
blocks the visitor's request.

### Authenticated writes

```
POST/PUT/PATCH/DELETE /api/projects/          (+ PATCH /api/projects/reorder/)
POST/PUT/PATCH/DELETE /api/skills/
... skills, experience, education, socials
PUT/PATCH /api/profile/          # no POST/DELETE (singleton)
PUT/PATCH /api/contact/          # no POST/DELETE (singleton)
PUT/PATCH /api/site-settings/    # no POST/DELETE (singleton)
PUT/PATCH /api/sections/{id}/    # read/update only — sections cannot be created/deleted
```

### JWT auth

```
POST /api/auth/token/          # {"username": ..., "password": ...} -> access + refresh
POST /api/auth/token/refresh/
```

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

---

## Admin CMS

Most content is managed from `/admin/`. Highlights:

- **Profile / Contact Info / Site Settings** are singletons (add/delete disabled).
- **Sections** cannot be added or deleted (prevents accidental data loss);
  edit the nav label, section label, heading, visibility and order inline.
  Section *order* also drives the nav order on the live site.
- **Experience** bullets and **Project** tech stacks are edited as plain
  text / comma-separated lists (no raw JSON required).
- **Contact Messages** are read-only; messages arrive via the frontend form.
- **Site Settings → Draft mode**: when enabled, the frontend only applies CMS
  appearance controls when the URL contains `?preview=1`, so you can review
  changes before going live.
- The admin theme is mobile-responsive (change-list tables scroll horizontally
  and labels stack above inputs on small screens).

---

## Résumé upload

1. Go to **Admin → Profile**.
2. Under **Media**, either upload a PDF to **Resume** (preferred) or paste a
   link into **Resume url** (fallback).
3. Save, then verify the gold **Download Resume** button appears in the admin.

On the frontend the hero "Download Résumé" button is **hidden until a resume
exists**, so it is never a dead link. The API exposes `resume_file_url` (from the
uploaded file) and `resume_url` (external link).

Uploaded files are stored under `media/`:

```
media/
├── resumes/
└── images/
    ├── avatars/
    ├── projects/
    ├── companies/
    └── backgrounds/
```

---

## Theming & fonts

- Default palette: **Deep Burgundy × Warm Gold** (`:root`, the site's "light"
  toggle state). `body[data-theme="dark"]` switches to a **Night Light**
  deep-olive / sage palette.
- The default is `data-theme="light"` in `index.html` (and in `SiteSettings`),
  so the site boots on-brand. A user's toggle choice is remembered in
  `localStorage`.
- Font styles: `classic` (Lora + Crimson Text), `modern` (Inter, loaded from
  Google Fonts) and `system`.
- `SiteSettings` colours / background image / custom CSS are applied at runtime
  by `static/js/app.js`.

---

## Testing

```powershell
python manage.py test portfolio
```

The suite covers:

1. **API smoke tests** — every endpoint responds and respects its contract
   (singletons, category filtering, JWT-protected writes, sections being
   read/update-only, the contact throttle scope, the async notification helper).
2. **Frontend selector-contract tests** — guarantee the JS selectors still match
   the markup in `index.html` (the class of bug where API data was silently
   discarded), and that the default theme and résumé button behaviour stay
   consistent.
3. **Seed data integrity** — `seed_data` uses the intended skill categories and
   creates sections/settings.

---

## Deployment (PythonAnywhere)

1. Upload/clone the code and create a virtualenv with Python 3.11.
2. `pip install -r requirements.txt`.
3. Set environment variables (Web tab → Environment variables):

   ```
   SECRET_KEY=<a long random string>
   DEBUG=False
   ALLOWED_HOSTS=your_username.pythonanywhere.com
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   DATABASE_URL=postgresql://...        # optional; SQLite is used otherwise
   ```

4. Point the WSGI file at the project and set
   `DJANGO_SETTINGS_MODULE=settings.production`.
5. Run `python manage.py migrate` and `python manage.py collectstatic --noinput`.
6. Configure static files in the Web tab:

   ```
   URL: /static/   -> /home/your_username/Karthik_Portfolio/staticfiles
   URL: /media/    -> /home/your_username/Karthik_Portfolio/media
   ```

7. Reload the web app.

`settings/production.py` refuses to start without a real `SECRET_KEY`, disables
CORS allow-all, and defaults SSL/cookie security flags to `True`.

---

## Troubleshooting

- **"duplicate column name: resume"** — this was a broken migration chain
  (`0002` added `Profile.resume`, `0004` re-added it). `0004` is now a no-op; run
  `python manage.py migrate`.
- **Static files missing in production** — run `collectstatic` and check the
  static-files mapping above; media is served by the web server in production,
  not Django.
- **No data on the site** — run `python manage.py seed_data --force`.
- **Contact form says "live content unavailable"** — the API is unreachable; the
  frontend shows a banner and falls back to the latest saved content.
- **Reset the dev database** — delete `db.sqlite3`, then `migrate` +
  `createsuperuser` + `seed_data --force`.
