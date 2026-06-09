# Resume Upload Guide

## How to Upload Your Resume

### Step 1: Access Admin Panel
1. Open your browser and go to: `http://127.0.0.1:8000/admin`
2. Login with your superuser credentials

### Step 2: Navigate to Profile
1. Click on **"Profile"** in the left sidebar (under PORTFOLIO section)
2. Click on your profile entry (should be "Karthik Aarupalli")

### Step 3: Upload Resume
You'll see a **"Media"** section with two options:

#### Option A: Upload Resume File (Recommended)
1. Find the **"Resume"** field
2. Click **"Choose File"** or **"Browse"**
3. Select your PDF resume from your computer
4. Click **"Save"** at the bottom of the page

**Notes:**
- Preferred format: PDF
- Recommended file size: Under 5MB
- File will be stored in: `media/resumes/your_resume.pdf`

#### Option B: Resume URL (Alternative)
If you have your resume hosted elsewhere (Google Drive, Dropbox, etc.):
1. Find the **"Resume url"** field
2. Paste the direct download link
3. Click **"Save"**

### Step 4: Verify Upload
After saving, you should see:
- **"Current Resume"** section showing your uploaded file
- A gold **"📄 Download Resume"** button to test the file
- The filename displayed below the button

### Step 5: Test Frontend
1. Go to your portfolio: `http://127.0.0.1:8000/`
2. Click the **"Download Résumé"** button in the hero section
3. Your resume should download automatically

## Resume Field Details

### Which field does what?

| Field | Purpose | Priority |
|-------|---------|----------|
| **Resume** (File Upload) | Upload PDF directly to your server | **HIGH** (Frontend checks this first) |
| **Resume url** | Link to external resume (e.g., Google Drive) | LOW (Fallback option) |

### Priority Logic
The frontend checks in this order:
1. If `resume` file exists → Use uploaded file ✅
2. Else if `resume_url` exists → Use URL
3. Else → Button shows but doesn't work

## Troubleshooting

### "No resume uploaded yet" message
- The **Resume** field is empty
- Upload a file using the "Choose File" button

### Resume button doesn't work on frontend
1. Go to admin panel
2. Check that either `resume` or `resume_url` has a value
3. Click "Save" to ensure changes are applied

### File upload fails
1. Check file size (should be under 5MB)
2. Ensure file format is PDF
3. Check that `media/resumes/` folder exists and has write permissions

### Can't find Profile in admin
1. Make sure Django server is running: `python manage.py runserver`
2. Check that you loaded default data: `python manage.py load_default_data`
3. If still missing, create manually:
   ```bash
   python manage.py shell
   >>> from portfolio.models import Profile
   >>> Profile.objects.create(name="Your Name", tagline="Your Tagline", about="About text")
   ```

## Admin Panel Features

### Resume Preview
- See which file is currently uploaded
- Download button to test the file
- Shows filename and upload status

### Avatar Preview
- See your profile picture in admin
- Circular preview matching frontend design

### Media Organization
All your files are organized in the `media/` folder:
```
media/
├── resumes/           # Your resume PDFs
├── images/
│   ├── avatars/      # Profile pictures
│   ├── projects/     # Project thumbnails
│   ├── companies/    # Company logos
│   └── backgrounds/  # Site backgrounds
```

## Best Practices

### Resume File Naming
✅ **Good:**
- `Karthik_Aarupalli_Resume_2024.pdf`
- `resume_karthik_2024.pdf`
- `CV_Karthik.pdf`

❌ **Avoid:**
- `resume final final (1).pdf`
- `my resume.pdf` (spaces can cause issues)
- `résumé.docx` (use PDF, not Word)

### Keeping Resume Updated
1. Login to admin: `http://127.0.0.1:8000/admin`
2. Go to Profile
3. Upload new file (old one gets replaced automatically)
4. Click Save
5. Test on frontend immediately

### Using Google Drive Links
If you prefer hosting on Google Drive:
1. Upload resume to Google Drive
2. Right-click → Share → Get link
3. Change permission to "Anyone with the link"
4. Copy the link
5. Paste in **Resume url** field in admin

## API Endpoint

The resume is served through the API:
```
GET http://127.0.0.1:8000/api/profile/
```

Response includes:
```json
{
  "name": "Karthik Aarupalli",
  "resume_file_url": "http://127.0.0.1:8000/media/resumes/karthik_resume.pdf",
  "resume_url": null,
  ...
}
```

Frontend JavaScript uses this to set the button's `href`.

## Security Notes

### Production Deployment
When deploying to production:
1. Resumes are publicly accessible (anyone can download)
2. Use HTTPS to serve resume files securely
3. Consider using cloud storage (AWS S3, Cloudinary) for files
4. Set up proper CORS headers

### Privacy
- Resume is public once uploaded
- Don't include sensitive personal data beyond what you'd share publicly
- Consider redacting phone number or address if concerned

## Quick Reference

| Action | Steps |
|--------|-------|
| Upload resume | Admin → Profile → Resume field → Choose File → Save |
| Update resume | Same as upload (replaces old file) |
| Test download | Frontend → Click "Download Résumé" button |
| Check API | Visit `http://127.0.0.1:8000/api/profile/` in browser |
| Remove resume | Admin → Profile → Clear checkbox → Save |

## Need Help?

### Common Questions

**Q: Can I upload Word documents?**
A: No, only PDF format is supported. Convert to PDF first.

**Q: How large can the file be?**
A: Recommended under 5MB. Adjust in Django settings if needed.

**Q: Will old resumes be saved?**
A: No, uploading a new resume replaces the old one.

**Q: Can I have multiple resumes?**
A: No, only one resume per profile. Upload your most recent version.

**Q: Does the resume get indexed by Google?**
A: Yes, if your site is public. Use robots.txt to prevent if needed.

---

✅ **You're all set!** Upload your resume and users can download it from your portfolio.
