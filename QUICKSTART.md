# Quick Start Guide

## Your Django backend is ready! Follow these steps:

### 1. Activate Virtual Environment (if not already active)
```powershell
venv\Scripts\activate
```

### 2. Run Setup Script
```powershell
.\setup.ps1
```

OR manually run these commands:

```powershell
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (you'll be prompted for username, email, password)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 3. Start Development Server
```powershell
python manage.py runserver
```

### 4. Access Your Backend

- **Admin Panel**: http://127.0.0.1:8000/admin
- **API Root**: http://127.0.0.1:8000/api/
- **Profile API**: http://127.0.0.1:8000/api/profile/
- **Projects API**: http://127.0.0.1:8000/api/projects/
- **Skills API**: http://127.0.0.1:8000/api/skills/
- **Experience API**: http://127.0.0.1:8000/api/experience/
- **Education API**: http://127.0.0.1:8000/api/education/
- **Contact API**: http://127.0.0.1:8000/api/contact/
- **Socials API**: http://127.0.0.1:8000/api/socials/

### 5. Add Content via Admin Panel

1. Login to admin panel with your superuser credentials
2. Add your profile information
3. Add projects, skills, experience, etc.
4. All changes are immediately available via API

### 6. Test API Endpoints

Open browser or use curl:
```powershell
# Get profile
curl http://127.0.0.1:8000/api/profile/

# Get all projects
curl http://127.0.0.1:8000/api/projects/

# Get all skills
curl http://127.0.0.1:8000/api/skills/
```

### 7. Connect Your Frontend

Update your frontend to fetch from:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Fetch profile
fetch(`${API_BASE_URL}/profile/`)
  .then(res => res.json())
  .then(data => console.log(data));
```

## Troubleshooting

### If you get "No module named 'portfolio'"
Make sure you're in the correct directory and the portfolio folder exists with all files.

### If migrations fail
Delete `db.sqlite3` and run migrations again:
```powershell
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### If you need to reset everything
```powershell
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Next Steps

1. ✅ Setup complete
2. ✅ Add content via admin
3. ✅ Test API endpoints
4. 🔄 Connect frontend to API
5. 🚀 Deploy to PythonAnywhere (see README_BACKEND.md)
