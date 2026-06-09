# Portfolio Backend - Django REST API

A complete Django REST API backend for a portfolio website, deployable to PythonAnywhere. All content (bio, projects, skills, experience, education, contact info, social links) is managed through Django's admin panel and served via REST API endpoints.

## Features

- **Full REST API** with Django REST Framework
- **JWT Authentication** for admin operations
- **Django Admin Dashboard** for content management
- **Image Upload Support** for avatars, project thumbnails, company logos
- **CORS Enabled** for frontend integration
- **Production Ready** with Whitenoise for static files
- **PythonAnywhere Deployment** instructions included

## Tech Stack

- Python 3.11+
- Django 5.0
- Django REST Framework 3.14
- Simple JWT for authentication
- SQLite (development) / PostgreSQL (production)
- Pillow for image handling
- Whitenoise for static file serving

## Project Structure

```
portfolio_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── wsgi.py
├── asgi.py
├── urls.py
├── settings_base.py          # Base settings
├── settings_development.py   # Development settings
├── settings_production.py    # Production settings
└── portfolio/
    ├── portfolio_models.py
    ├── portfolio_serializers.py
    ├── portfolio_views.py
    ├── portfolio_urls.py
    ├── portfolio_admin.py
    ├── portfolio_permissions.py
    ├── portfolio_apps.py
    └── portfolio_init.py
```

## Models

### 1. Profile (Singleton)
- name, tagline, about, avatar, resume_url, is_available

### 2. Project
- title, description, tech_stack (JSON), live_url, repo_url, thumbnail, is_featured, order

### 3. Skill
- name, category (frontend/backend/tools/other), icon_url, proficiency (1-5)

### 4. Experience
- company, role, start_date, end_date, bullets (JSON), logo, order

### 5. Education
- institution, degree, year, description

### 6. ContactInfo (Singleton)
- email, phone, availability_note

### 7. SocialLink
- platform, url, icon_url, order

## API Endpoints

### Public Endpoints (GET)
```
GET /api/profile/              # Get profile
GET /api/projects/             # List all projects
GET /api/projects/{id}/        # Get single project
GET /api/skills/               # List all skills
GET /api/experience/           # List all experience
GET /api/education/            # List all education
GET /api/contact/              # Get contact info
GET /api/socials/              # List all social links
```

### Admin Endpoints (Requires JWT)
```
POST   /api/projects/          # Create project
PUT    /api/projects/{id}/     # Update project
DELETE /api/projects/{id}/     # Delete project
PATCH  /api/projects/reorder/  # Reorder projects

# Similar CRUD for skills, experience, education, socials
PUT    /api/profile/           # Update profile
PUT    /api/contact/           # Update contact info
```

### Authentication
```
POST /api/auth/token/          # Get access + refresh tokens
POST /api/auth/token/refresh/  # Refresh access token
```

## Local Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd portfolio_backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

### 5. Create Portfolio App Structure
Since files are created separately, organize them into the portfolio app:
```bash
mkdir portfolio
mv portfolio_*.py portfolio/
cd portfolio
mv portfolio_models.py models.py
mv portfolio_serializers.py serializers.py
mv portfolio_views.py views.py
mv portfolio_urls.py urls.py
mv portfolio_admin.py admin.py
mv portfolio_permissions.py permissions.py
mv portfolio_apps.py apps.py
mv portfolio_init.py __init__.py
cd ..
```

### 6. Create Settings Package
```bash
mkdir settings
mv settings_*.py settings/
cd settings
mv settings_base.py base.py
mv settings_development.py development.py
mv settings_production.py production.py
touch __init__.py
cd ..
```

### 7. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser
```bash
python manage.py createsuperuser
```

### 9. Run Development Server
```bash
python manage.py runserver
```

### 10. Access Admin Panel
Navigate to: `http://127.0.0.1:8000/admin`

## PythonAnywhere Deployment

### Step 1: Upload Code
```bash
# In PythonAnywhere bash console
git clone <your-repo-url>
cd portfolio_backend
```

### Step 2: Create Virtual Environment
```bash
mkvirtualenv --python=python3.11 portfolio-env
workon portfolio-env
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Organize Files (if not done)
```bash
# Create portfolio app
mkdir portfolio
mv portfolio_*.py portfolio/
cd portfolio
mv portfolio_models.py models.py
mv portfolio_serializers.py serializers.py
mv portfolio_views.py views.py
mv portfolio_urls.py urls.py
mv portfolio_admin.py admin.py
mv portfolio_permissions.py permissions.py
mv portfolio_apps.py apps.py
mv portfolio_init.py __init__.py
cd ..

# Create settings package
mkdir settings
mv settings_*.py settings/
cd settings
mv settings_base.py base.py
mv settings_development.py development.py
mv settings_production.py production.py
touch __init__.py
cd ..
```

### Step 5: Configure Environment Variables
In PythonAnywhere Web tab → Environment variables:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your_username.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Step 6: Configure WSGI File
In PythonAnywhere Web tab → Code section → WSGI configuration file:
```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/your_username/portfolio_backend'
if path not in sys.path:
    sys.path.append(path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 7: Configure Static Files
In PythonAnywhere Web tab → Static files section:
```
URL: /static/
Directory: /home/your_username/portfolio_backend/staticfiles

URL: /media/
Directory: /home/your_username/portfolio_backend/media
```

### Step 8: Run Migrations and Collect Static
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 9: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 10: Reload Web App
Click "Reload" button in PythonAnywhere Web tab

### Step 11: Access Your API
- Admin: `https://your_username.pythonanywhere.com/admin`
- API: `https://your_username.pythonanywhere.com/api/`

## Frontend Integration

### React/Next.js Example
```javascript
// Fetch projects
const response = await fetch('https://your_username.pythonanywhere.com/api/projects/');
const projects = await response.json();

// Fetch profile
const profileResponse = await fetch('https://your_username.pythonanywhere.com/api/profile/');
const profile = await profileResponse.json();
```

### Next.js with Revalidation
```javascript
// app/page.js
export const revalidate = 60; // Revalidate every 60 seconds

async function getProjects() {
  const res = await fetch('https://your_username.pythonanywhere.com/api/projects/', {
    next: { revalidate: 60 }
  });
  return res.json();
}

export default async function Home() {
  const projects = await getProjects();
  return <ProjectList projects={projects} />;
}
```

### Plain JavaScript
```javascript
// Fetch all data
async function loadPortfolio() {
  const baseURL = 'https://your_username.pythonanywhere.com/api';
  
  const [profile, projects, skills, experience] = await Promise.all([
    fetch(`${baseURL}/profile/`).then(r => r.json()),
    fetch(`${baseURL}/projects/`).then(r => r.json()),
    fetch(`${baseURL}/skills/`).then(r => r.json()),
    fetch(`${baseURL}/experience/`).then(r => r.json())
  ]);
  
  return { profile, projects, skills, experience };
}
```

## Admin Operations with JWT

### Get Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

### Create Project (with token)
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Project",
    "description": "Project description",
    "tech_stack": ["Python", "Django", "React"],
    "is_featured": true,
    "order": 0
  }'
```

## Database Schema

### Profile
```sql
- id (PK)
- name (VARCHAR)
- tagline (VARCHAR)
- about (TEXT)
- avatar (ImageField)
- resume_url (URL)
- is_available (BOOLEAN)
- created_at (DATETIME)
- updated_at (DATETIME)
```

### Project
```sql
- id (PK)
- title (VARCHAR)
- description (TEXT)
- tech_stack (JSON)
- live_url (URL)
- repo_url (URL)
- thumbnail (ImageField)
- is_featured (BOOLEAN)
- order (INTEGER)
- created_at (DATETIME)
- updated_at (DATETIME)
```

## Security Notes

1. **Change SECRET_KEY** in production
2. **Set DEBUG=False** in production
3. **Configure ALLOWED_HOSTS** properly
4. **Use HTTPS** in production
5. **Restrict CORS_ALLOWED_ORIGINS** to your frontend domain
6. **Keep JWT tokens secure** on the client side

## Troubleshooting

### Issue: Static files not loading
```bash
python manage.py collectstatic --noinput
# Check STATIC_ROOT and STATIC_URL in settings
```

### Issue: Media files not accessible
```bash
# Ensure media directory exists
mkdir media
# Check MEDIA_ROOT and MEDIA_URL in settings
```

### Issue: Database errors
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: CORS errors
```python
# In settings/production.py
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',
]
# Or for development:
CORS_ALLOW_ALL_ORIGINS = True
```

## License

MIT License - feel free to use this for your portfolio!

## Support

For issues or questions, please open an issue on GitHub.
