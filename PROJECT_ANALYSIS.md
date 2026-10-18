# Project Analysis — Karthik Portfolio

> Full audit of the codebase: bugs, broken APIs, UI/UX issues, admin panel, redundancy and **responsiveness** (the biggest problem area).
> Generated after reading every source file in the repo (Django backend + vanilla HTML/CSS/JS frontend + admin theme).

---

## 0. Severity Legend

| Tag | Meaning |
|-----|---------|
| 🔴 **Critical** | Feature is outright broken / data silently lost |
| 🟠 **High** | Wrong behaviour, security risk, or bad on real devices |
| 🟡 **Medium** | Noticeable defect, inconsistency, or maintenance hazard |
| 🔵 **Low** | Cosmetic, polish, or technical debt |

---

## 1. Project Overview

| Layer | Tech | Notes |
|-------|------|-------|
| Backend | Django 5.0.1 + DRF 3.14 + SimpleJWT | API + Admin CMS |
| Frontend | Static `index.html` served by `FileResponse` | Vanilla JS "SPA" via hash routing |
| Styling | Hand-written CSS (`static/css/style.css`, 1418 lines) | "Apple × Gold" system |
| Admin | Django admin + custom CSS theme (`templates/admin/base_site.html`) | |
| DB | SQLite (dev) / PostgreSQL (prod) | |

### File inventory
- **Backend:** `manage.py`, `urls.py`, `wsgi.py`, `asgi.py`, `settings/{base,development,production}.py`, `portfolio/{models,views,serializers,admin,permissions,urls,apps}.py`, `portfolio/management/commands/{load_default_data,seed_data}.py`, 5 migrations.
- **Frontend:** `index.html` (545 lines), `static/css/style.css`, `static/js/app.js` (871 lines), `static/js/waves.js`.
- **Admin:** `templates/admin/base_site.html` (1032 lines of overrides).
- **Docs / scripts (redundant):** `README_BACKEND.md`, `QUICKSTART.md`, `RESUME_FIX.md`, `RESUME_UPLOAD_GUIDE.md`, `GLOWY_WAVES_IMPLEMENTATION.md`, `setup.ps1`, `setup_resume.ps1`, `run.bat`, `powershell.cmd`, `deploy.sh`.

`python manage.py check` currently passes (no model/URL errors). The problems below are behavioural, not import-time.

---

## 2. 🔴 Critical — Broken API ↔ UI Bindings

These are the most important: the Django REST API works, but the frontend queries selectors that **do not exist in the markup**, so API data is fetched and thrown away.

### 2.1 Contact info never reaches the page
- JS targets `.contact-card` and `.contact-card-value`:
  - `static/js/app.js:469` → `document.querySelectorAll('.contact-card')`
  - `static/js/app.js:473` → `contactCards[0].querySelector('.contact-card-value')`
- Real markup uses `.cc-contact-item` / `.cc-item-value`:
  - `index.html:456`, `index.html:462` (email), `index.html:466`, `index.html:472` (phone)
- **Result:** editing email/phone/`availability_note` in the API/admin updates nothing on the site (except `availability_note`, which correctly targets `.contact-subtext` at `app.js:482`).

### 2.2 Social links never render from the API
- JS targets `.social-row`: `static/js/app.js:491` → `document.querySelector('.social-row')`
- Real markup class is `.cc-social-row`: `index.html:488`
- **Result:** the social-link loop (`app.js:495-517`) silently does nothing; the hardcoded GitHub/LinkedIn icons remain forever. `icon_url` from the admin is also ignored (only a 2-entry `iconMap` exists).

### 2.3 Contact section heading override fails
- JS: `page.querySelector('.section-heading, .contact-heading')` (`app.js:198`)
- The contact page has no `.section-heading` and no `.contact-heading` — it uses `.cc-title` (`index.html:451`).
- **Result:** a custom heading set in Admin → Sections has no effect on Contact.

### 2.4 Résumé button is a dead link by default
- Hero button starts as `href="#"`: `index.html:119`
- `app.js:247-253` only assigns an `href` **if** `resume_file_url` or `resume_url` exists.
- The seeded/default profile has **no résumé** (`load_default_data.py`, `seed_data.py:84-101`).
- **Result:** "Download Résumé" does nothing and silently jumps to the top of the page (because `href="#"`). Documented as a "known" behaviour in `RESUME_UPLOAD_GUIDE.md` but it is a broken UX.

### 2.5 Section re-ordering (admin "order") has no visual effect
- JS sets `page.style.order` (`app.js:182`), but pages are plain block children of `<main>` (`index.html:90`). CSS `order` only applies to **flex/grid** items.
- **Result:** changing section order in Admin → Sections reorders nothing on the live site (nav labels reorder because `.nav-menu` is flex, so nav and page order can drift apart).

---

## 3. 🟠 High — Backend / API Issues

### 3.1 `filterset_fields` is dead code (filtering by category does nothing)
- `SkillViewSet.filterset_fields = ['category']` — `portfolio/views.py:96`
- `REST_FRAMEWORK` in `settings/base.py:111-128` has **no** `DEFAULT_FILTER_BACKENDS`, so `django-filter` (installed as an app at `base.py:28`) is never wired in.
- **Result:** `GET /api/skills/?category=ai_ml` is ignored.

### 3.2 The `contact` throttle is never applied
- Rate defined: `'contact': '30/hour'` — `settings/base.py:125`
- `ContactMessageViewSet` (`views.py:195-207`) has **no** `throttle_scope` and no per-action throttle.
- **Result:** the dedicated contact rate limit is dead; only the global `anon` `100/hour` applies. The JS 429 handler (`app.js:797-799`) rarely/never fires as intended.

### 3.3 Notification email is sent synchronously inside the request
- `perform_create` calls `send_mail(..., fail_silently=False)` — `views.py:226-232`
- **Result:** a slow/unreachable SMTP server blocks the HTTP response and can time out the visitor's form submit. Should be async (Celery/RQ) or at least `fail_silently=True` with a background task.

### 3.4 Section CRUD is inconsistent with the admin guard
- Admin **blocks** adding/deleting sections (`admin.py:357-363`).
- `SectionViewSet` (`views.py:185-192`) allows full `ModelViewSet` CRUD via JWT — including `POST` and `DELETE` (even of `home`, which the admin explicitly protects).
- **Result:** API and Admin disagree on the rules; an admin token can delete `home`.

### 3.5 `SiteSettingsViewSet.list` shadows the Django `settings` object
- `settings, _ = SiteSettings.objects.get_or_create()` — `views.py:174` shadows the module-level `from django.conf import settings` import. It works today only because `list()` doesn't use Django settings — fragile and confusing.

### 3.6 Two contradictory seeders
- `load_default_data.py:64-98` maps skill categories to **wrong** values (`'frontend'` for languages, `'backend'` for AI/ML, `'tools'` for libraries, `'other'` for databases) and gives everything proficiency `5`.
- `seed_data.py:149-176` uses the **correct** categories (`languages`, `ai_ml`, `libraries`, `tools`) and realistic proficiencies.
- Running both (or `load_default_data` after `seed_data`) corrupts category grouping and overwrites the 3-dot design with 5-dot.
- They also disagree on data shape (project titles, education strings, etc.).

### 3.7 Media is served by Django in production
- `urls.py:46-49` uses `django.views.static.serve` for `/media/` when `DEBUG=False`. This is documented as insecure/inefficient and not meant for production; PythonAnywhere/WhiteNoise won't serve it efficiently.

### 3.8 Permissive production CORS default
- `settings/production.py:30-31`: if `CORS_ALLOWED_ORIGINS` is empty it silently sets `CORS_ALLOW_ALL_ORIGINS = True`.
- Also `CORS_ALLOWED_ORIGINS` is read from a config key that isn't in `.env.example` (the example uses `CORS_ALLOWED_ORIGINS`, so it matches — but the insecure fallback remains a risk).

### 3.9 No automated tests
- There are no `tests.py`/`tests/` anywhere. Every regression from section 2 (selector drift) went undetected precisely because there are zero UI/integration tests.

### 3.10 Serializer/field duplicates
- `Profile` has **both** `resume` (FileField) and `resume_url` (URLField) → two sources of truth for one feature (`models.py:17-18`).

---

## 4. 🟠 High — Frontend / JS Issues

### 4.1 Silent failure on every API call
- `fetchAPI` swallows errors and returns `null` (`app.js:93-96`); no loading or error state is shown. If the API is down, users see stale hardcoded content with no indication anything failed.

### 4.2 Theme system is self-contradictory
- `:root` default palette is **deep burgundy** (`style.css:7-37`).
- `body[data-theme="dark"]` is a **green "Night Light"** palette (`style.css:87-109`).
- `index.html:39` ships `data-theme="dark"` → the site actually boots **green**, contradicting the "Clear White, Rich Gold" header comment (`style.css:3`) and the "Apple × Gold" branding.
- `SiteSettings` default `theme='light'` plus JS (`app.js:138-141`) fights with the user's `localStorage` toggle → first-paint flash and inconsistent colors between visits/devices.
- **Note:** you said colors are "OK" — the colors themselves are fine, but the **default** and the **light/dark naming** (`light`=burgundy-dark, `dark`=green) are backwards and confusing.

### 4.3 "Modern Sans" font never loads
- `body[data-font-style="modern"]` requests `Inter` (`style.css:78-80`), but only Crimson Text / Lora / Courier Prime are loaded (`index.html:21`). It silently falls back to Segoe UI/Arial.

### 4.4 Entrance animations are inconsistent
- Only `.hero-name-line` and `.hero-stats-pills` start at `opacity:0` (`style.css:568-575`, `600-607`). `.hero-role`, `.hero-tagline`, `.hero-ctas` are fully visible from the first frame, so the `[data-animate]` timeline (`app.js:698-708`) is a no-op for them.

### 4.5 Dead / meaningless code
- `profileImg.innerHTML = '';` on an `<img>` does nothing (`app.js:239`).
- `ProfileViewSet`/`ContactInfoViewSet` custom `retrieve` methods (`views.py:55-59`, `144-148`) add nothing over the default.
- Empty `<img src="">` triggers a guaranteed browser request + error before the fallback (`index.html:192`).
- `loadProjects` overwrites `.project-links`, discarding the static "18 modules · 0 failures" text (`index.html:337`) whenever a repo URL exists (`app.js:283-294`).
- Featured/project live link label renders `View Live ->` instead of an arrow (`app.js:291`, `327`).

### 4.6 Hardcoded stats can desync from CMS
- `data-target="5/18/10"` is hardcoded (`index.html:159-161`) and not driven by the API. Adding projects will never update these counters.

---

## 5. 🔴 Responsiveness — The Real Problem

The CSS is desktop-first with a few tacked-on breakpoints. Breakpoints used: `639`, `640-1023`, `1024`, `1440` (`style.css:1360-1404`) plus contact at `767/768` (`1308-1333`) and nav/theme at `1023` (`350-360`). Key defects:

### 5.1 Horizontal overflow on small phones (clipped content)
- `.skills-grid { grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }` — `style.css:816-820`
- `.container` adds `2rem` (32px) padding each side (`style.css:378`), and `.nav-container` uses `2rem` too.
- On a **320px** viewport: `320 − 64 = 256px` available, but the grid track minimum is **260px** → **overflow**, and `body { overflow-x: hidden }` (`style.css:71`) **clips** the cards instead of scrolling. Fix: `minmax(min(260px, 100%), 1fr)` or lower the min at small widths.

### 5.2 Hero name can overflow on narrow screens
- `--text-hero: clamp(3.5rem, 8vw, 7rem)` — `style.css:40`
- The floor is `3.5rem = 56px`. "Aarupalli" at 56px ≈ 250px+, which collides with the 256px content width at 320px → clipping. Needs a smaller clamp floor (e.g. `2.2rem`) at `<400px`.

### 5.3 "Dual timeline" is never actually dual
- `@media (min-width: 1024px) { .dual-timeline { grid-template-columns: 1fr; } }` — `style.css:1399`
- Education and Certifications always stack in one column, even on wide desktop, despite the markup comment "dual-timeline" (`index.html:376`) and the `.timeline-column:last-child` styling that assumes a two-column layout. Either make it `repeat(2, 1fr)` on desktop or remove the "dual" naming/styling.

### 5.4 Fixed theme toggle overlaps form/footer on mobile
- Below `1023px` the theme toggle is `position: fixed; bottom: 24px; right: 24px; z-index: 1001` (`style.css:350-360`).
- On the Contact page it can sit over the "Send Message" button / footer text, and it stays fixed across all pages, covering content. Should hide on scroll or move into the mobile menu.

### 5.5 Spacing is not scaled down for mobile
- `--space-xl: 8rem` (`style.css:51`) is used for `section` padding (`style.css:377`) and `.achievements-section` / `.contact-section`. There is **no** mobile override, producing huge dead vertical gaps on phones. Similarly `--space-lg: 4rem`.
- `.about-section`/`.skills-section`/`.projects-section`/`.experience-section` use `padding-top: calc(72px + var(--space-lg))` (`style.css:679, 790, 854, 920`) — not reduced on mobile.

### 5.6 Contact form column has no tablet tuning
- The contact card only becomes two columns at `min-width: 768px` (`style.css:1308-1311`). Between 640–768 it's a single tall column — acceptable, but `.cc-info-panel` uses `justify-content: space-between` and can leave awkward gaps. On very short landscape phones the section is `min-height: 100vh` and will overflow awkwardly.

### 5.7 Nav breakpoints leave a "no visual toggle" ambiguity
- Hamburger appears at `<=1023px` (`style.css:350, 1360, 1381`), but the mobile menu background is `rgba(0,0,0,0.88)` with `backdrop-filter` (`style.css:266-271`) — heavy on low-end mobiles and can cause jank.

### 5.8 Admin panel is not mobile-responsive
- `templates/admin/base_site.html:987-1017` only pads font/padding at `<=767px`; it never adds horizontal scrolling for Django's wide change-list tables (`#result_list`). Django admin tables overflow and break on phones. No `overflow-x: auto` wrapper is applied.
- `body.login #container { min-width: 340px }` (`base_site.html:813-817`) can overflow very small phones.
- `.aligned label { width: 180px }` (`base_site.html:524-526`) is fixed and crushes form fields on narrow screens.
- Global overrides use `!important` heavily and `border-radius: 980px` on `.button`/inputs, which can distort admin widgets at small sizes.

### 5.9 Minor responsive gaps
- `.corner-plus` icons are absolutely positioned at `-12px` (`style.css:1069-1072`); on small screens they can clip against the viewport edge (partially mitigated to `-9px` under 767px).
- `.hero { min-height: calc(100vh - 72px) }` with `padding-top: 72px` (`style.css:446-449`) — on short landscape phones the hero content can overflow the viewport.
- No `overflow-x: auto` on `.projects-grid`/`.skills-grid` (they use grid, so fine) but the same cannot be said for future wide embeds.
- `stats-grid` and most clamps (`--text-display`, `--text-body`) are reasonable; the grid min-track and hero font floor are the two real breakers.

---

## 6. 🟠 Admin Panel Issues

1. **Responsiveness** — see 5.8. This is the main admin complaint.
2. **Heavy `!important` theme** — `base_site.html` overrides ~1000 lines with `!important`; any Django admin upgrade risks visual breakage.
3. **Section delete guard asymmetry** — `admin.py:361-363` lets you delete any non-`home` section, but `has_add_permission` returns `False` (`admin.py:357-359`), so a deleted section can only be restored via shell/migration. Easy data loss.
4. **`SiteSettings` has no `readonly_fields`** for `created_at`/`updated_at`, and they're omitted from fieldsets; harmless but inconsistent with `ProjectAdmin` (`admin.py:174`).
5. **ContactMessage admin is read-only** (`admin.py:376`) — good, but messages can only be deleted one-by-one; no bulk "mark read"/archive; no unread indicator.
6. **No link from admin to the live preview** despite `draft_mode` / `?preview=1` being a designed workflow (`models.py:241-244`).
7. **`load_default_data` output tells users to visit `http://127.0.0.1:8080`** (`load_default_data.py:173`) while everywhere else uses `8000` — wrong port in the message.

---

## 7. 🟡 Unstructured / Redundant Features

The project has **two overlapping product directions** bolted together, which is the root of the "unstructured" feel:

1. **Static hardcoded site vs. API-driven CMS.** `index.html` ships full hardcoded content that the API only *partially* overrides (and in several places fails to — section 2). This dual source of truth is fragile.
2. **Two seed commands** with conflicting data (3.6).
3. **Two résumé fields** (`resume` file + `resume_url`) (3.10).
4. **Two theme systems**: CSS `data-theme`/`:root` palettes **and** API `SiteSettings` colors (`style.css:7-109` vs `app.js:107-141`).
5. **Five overlapping markdown docs** (`README_BACKEND.md`, `QUICKSTART.md`, `RESUME_FIX.md`, `RESUME_UPLOAD_GUIDE.md`, `GLOWY_WAVES_IMPLEMENTATION.md`) plus this file — no single source of truth.
6. **Redundant setup scripts**: `setup.ps1` vs `setup_resume.ps1`; `run.bat` hardcodes an absolute machine path (`run.bat:2`) and a separate `powershell.cmd`.
7. **Three "page transition" mechanisms** (CSS `.page.active/.exiting`, Router timeouts, `observeReveals`) with hardcoded 200/220ms timings that must stay in sync (`app.js:599-611`).
8. **`README_BACKEND.md` documents an architecture that doesn't match the repo** (it describes `portfolio_*.py` files and `settings_*.py` that no longer exist), so it actively misleads.
9. **`admin.py` `BulletListFormField`/`TechStackFormField`** exist only for the admin; the API accepts raw JSON — two editing paradigms for the same JSON fields.

---

## 8. 🟠 Security Notes

| Item | Location | Risk |
|------|----------|------|
| `SECRET_KEY` fallback default | `settings/base.py:13` | High if env not set in prod |
| `CORS_ALLOW_ALL_ORIGINS = True` fallback | `settings/production.py:31` | High |
| `SECURE_SSL_REDIRECT = False` default | `settings/production.py:37` | Medium |
| Media served by Django | `urls.py:46-49` | Medium |
| `custom_css` injected raw into `<style>` | `models.py:237`, `app.js:162-168` | Medium (admin-only, but stored XSS if admin account compromised) |
| `heading` injected as `innerHTML` | `app.js:200` | Low–Medium (admin-controlled) |
| `.env` present on disk | root | Ensure it is never committed (currently **not** tracked by git — verified) |

---

## 9. 🟡 Performance Notes

- `body { background-attachment: fixed }` (`style.css:73`) + multiple radial gradients causes repaint jank on mobile.
- `backdrop-filter: blur()` used on navbar, role badge, pills, mobile menu — expensive on low-end devices.
- `waves.js` runs a full `requestAnimationFrame` loop with `shadowBlur` per wave (5 waves) — `waves.js:142-167`; heavy on mobile even when the hero is off-screen. It never pauses when the tab/page is hidden.
- `waves.js` draws every 4px across the full width every frame at device pixel ratio 1 (canvas not DPR-scaled), so it looks soft on retina and wastes cycles.
- No HTTP caching headers on the `index.html` `FileResponse` (`urls.py:16-21`); no `ETag`/`Last-Modified`.
- Fonts load 3 families with many weights up front (`index.html:21`).
- API returns up to `PAGE_SIZE = 100` per list with no client caching (`base.py:118-119`).

---

## 10. 🔵 Accessibility

- SPA hash-routing changes `document.title` (`app.js:614-624`) but does not move focus or announce page changes to screen readers.
- Custom cursor + hover-only affordances (`mouseover`/`mouseout`) have no keyboard equivalent for the "hover" cursor state (acceptable, but the cursor-ring is purely decorative).
- Empty `alt` fallback image and the `data:image/svg+xml` favicon are fine; the profile fallback uses pseudo-element text "KA" (`style.css:766-775`) which is not announced.
- Form errors are injected into `<span>` but there is no `aria-live` region (`index.html:504-519`), so screen readers won't hear validation errors.
- Mobile menu sets `aria-expanded`/`aria-hidden` (`app.js:675-692`) — good. But `Escape` does not close it.

---

## 11. Prioritized Fix List

### P0 — Broken features (do first)
1. Fix contact binding: `.contact-card`/`.contact-card-value` → `.cc-contact-item`/`.cc-item-value` (`app.js:469-478`).
2. Fix socials binding: `.social-row` → `.cc-social-row` (`app.js:491`).
3. Fix contact heading target: include `.cc-title` (`app.js:198`).
4. Make section `order` actually work (make `<main>` a flex/grid column, or reorder DOM nodes) (`app.js:182`, `index.html:90`).
5. Résumé button: hide/disable when no file/URL, or ship a real default résumé (`index.html:119`, `app.js:247-253`).
6. Add `DEFAULT_FILTER_BACKENDS` (DjangoFilterBackend) so `filterset_fields` works; or remove it (`base.py:111`, `views.py:96`).
7. Wire the `contact` throttle (`throttle_scope = 'contact'` on `ContactMessageViewSet`).

### P1 — Responsiveness (the headline issue)
8. `skills-grid` min-track → `minmax(min(260px, 100%), 1fr)` (`style.css:818`).
9. Lower hero font floor on `<400px` (`style.css:40`).
10. Add mobile overrides for `--space-xl`/`--space-lg` and section paddings (`style.css:377, 679, 790, 854, 920`).
11. Fix theme toggle overlap / hide-on-scroll on mobile (`style.css:350-360`).
12. Decide `.dual-timeline`: real 2 columns on desktop or remove "dual" theming (`style.css:1399`).
13. Admin: add horizontal scroll wrapper for `#result_list`, responsive `.aligned label` (`base_site.html:524, 987`).

### P2 — Backend hygiene
14. Async (or `fail_silently`) contact email (`views.py:226`).
15. Remove/rename duplicated seeder and fix categories (`load_default_data.py:64-98`).
16. Restrict `SectionViewSet` methods to match admin rules (`views.py:185`).
17. Serve media via web server in prod; remove `django.views.static.serve` (`urls.py:46-49`).
18. Tighten production CORS/SSL defaults (`production.py:31,37`).
19. Fix `SiteSettingsViewSet.list` variable shadowing (`views.py:174`).

### P3 — Consistency / cleanup
20. Unify theming (pick one palette default; fix `light`/`dark` semantics) (`style.css:7-109`, `app.js:138-141`).
21. Load Inter or drop the "modern" font option (`style.css:78`).
22. Remove dead code (`app.js:239`, redundant `retrieve` methods, `profileImg.innerHTML`).
23. Consolidate the 5 docs into one README; delete stale `README_BACKEND.md` claims.
24. Remove machine-specific paths from `run.bat`.
25. Add tests (at minimum: API smoke tests + a JS selector contract test) to prevent the section-2 class of bugs.
26. Pause `waves.js` when the hero is not visible / tab hidden; scale canvas by `devicePixelRatio`.

---

## 12. One-line Summary

The backend is generally sound and `manage.py check` passes, but the site is held back by **(a) a handful of frontend selectors that no longer match the markup so key API data is silently discarded**, **(b) a desktop-first CSS system whose two real breakers are the 260px skills grid and a 56px hero font floor on narrow phones**, and **(c) an unstructured double architecture** (hardcoded content + partial CMS, two seeders, two résumé fields, two theme systems) that keeps drifting out of sync.
