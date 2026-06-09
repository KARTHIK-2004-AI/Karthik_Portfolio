# Resume Upload - Quick Fix Guide

## Problem
The `resume` FileField exists in your Profile model but NOT in the database yet.

## Solution - Run These Commands

Open PowerShell in your project directory and run:

```powershell
# Step 1: Apply the migration I created
python manage.py migrate portfolio

# Step 2: Create media folders (if they don't exist)
New-Item -ItemType Directory -Path "media\resumes" -Force

# Step 3: Start Django server
python manage.py runserver
```

## What This Does

### Migration File Created
I created: `portfolio/migrations/0004_profile_resume.py`

This adds the `resume` FileField to your database:
```python
migrations.AddField(
    model_name='profile',
    name='resume',
    field=models.FileField(upload_to='resumes/', blank=True, null=True),
)
```

### Admin Panel Updated
Updated `portfolio/admin.py` to show:
- Resume upload field
- Resume preview with download button
- Filename display

## After Running Migration

1. **Open Admin Panel:**
   ```
   http://127.0.0.1:8000/admin
   ```

2. **Go to Profile:**
   - Click "Profile" in sidebar
   - Click "Karthik Aarupalli"

3. **Find Media Section:**
   You'll now see:
   ```
   ┌─────────────────────────────────────┐
   │ Media                               │
   ├─────────────────────────────────────┤
   │ Avatar: [Choose File]               │
   │ Avatar preview: [Image/No image]    │
   │                                     │
   │ Resume: [Choose File] ← NEW!        │
   │ Resume preview: [Download] ← NEW!   │
   │                                     │
   │ Resume url: [Text field]            │
   └─────────────────────────────────────┘
   ```

4. **Upload Resume:**
   - Click "Choose File" next to Resume
   - Select your PDF
   - Click "Save" at bottom

5. **Verify:**
   - You'll see a gold "📄 Download Resume" button
   - Filename shows below
   - Frontend button now works

## Troubleshooting

### Migration already applied?
```powershell
python manage.py showmigrations portfolio
```
Should show:
```
[X] 0001_initial
[X] 0002_cms_settings_sections
[X] 0003_alter_profile_resume_url
[X] 0004_profile_resume  ← This should have X
```

### Still don't see Resume field?
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh admin page (Ctrl+F5)
3. Check Django console for errors

### "No such column" error?
The migration didn't run. Try:
```powershell
python manage.py migrate --run-syncdb
```

### Media folder permissions error?
Run PowerShell as Administrator, then:
```powershell
New-Item -ItemType Directory -Path "media\resumes" -Force
```

## File Locations

**Migration file:**
```
portfolio/migrations/0004_profile_resume.py
```

**Admin changes:**
```
portfolio/admin.py (lines 17-33)
```

**Uploaded files go to:**
```
media/resumes/your_resume.pdf
```

## Quick Test

After migration, test with Django shell:
```powershell
python manage.py shell
```

```python
from portfolio.models import Profile
p = Profile.objects.first()
print(p.resume)  # Should not error anymore
```

## Summary

✅ **Created:** Migration file `0004_profile_resume.py`
✅ **Updated:** Admin panel with resume preview
✅ **Ready:** Just run `python manage.py migrate portfolio`

The "Media" section will appear in admin after migration!
