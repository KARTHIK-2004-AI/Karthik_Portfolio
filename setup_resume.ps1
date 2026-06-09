# Resume Upload Setup Script
# Run this to add the resume upload field to your database

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Resume Upload Field Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Apply migration
Write-Host "[1/3] Applying database migration..." -ForegroundColor Yellow
python manage.py migrate portfolio
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Migration failed!" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Migration applied successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Create media directory
Write-Host "[2/3] Creating media directories..." -ForegroundColor Yellow
$mediaDir = "media\resumes"
if (!(Test-Path $mediaDir)) {
    New-Item -ItemType Directory -Path $mediaDir -Force | Out-Null
    Write-Host "✓ Created $mediaDir directory" -ForegroundColor Green
} else {
    Write-Host "✓ Directory already exists: $mediaDir" -ForegroundColor Green
}
Write-Host ""

# Step 3: Instructions
Write-Host "[3/3] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start Django server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Open admin panel:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/admin" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Navigate to Profile:" -ForegroundColor White
Write-Host "   Portfolio > Profile > Karthik Aarupalli" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Look for 'Media' section with:" -ForegroundColor White
Write-Host "   - Avatar (image upload)" -ForegroundColor Gray
Write-Host "   - Avatar preview" -ForegroundColor Gray
Write-Host "   - Resume (file upload) ← NEW!" -ForegroundColor Green
Write-Host "   - Resume preview ← NEW!" -ForegroundColor Green
Write-Host "   - Resume url (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Upload your resume PDF and click Save!" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
