# Django Backend Setup Script
# Run this after activating your virtual environment

Write-Host "=== Django Backend Setup ===" -ForegroundColor Green

# Step 1: Make migrations
Write-Host "`nStep 1: Creating migrations..." -ForegroundColor Yellow
python manage.py makemigrations

# Step 2: Apply migrations
Write-Host "`nStep 2: Applying migrations..." -ForegroundColor Yellow
python manage.py migrate

# Step 3: Create superuser
Write-Host "`nStep 3: Create superuser (follow prompts)..." -ForegroundColor Yellow
python manage.py createsuperuser

# Step 4: Collect static files
Write-Host "`nStep 4: Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "Run 'python manage.py runserver' to start the development server" -ForegroundColor Cyan
Write-Host "Admin panel: http://127.0.0.1:8000/admin" -ForegroundColor Cyan
Write-Host "API endpoints: http://127.0.0.1:8000/api/" -ForegroundColor Cyan
