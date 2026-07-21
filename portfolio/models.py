"""
Portfolio app models - all content models for the portfolio website
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    """
    Singleton model for user profile information.
    Only one instance should exist.
    """
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300)
    about = models.TextField()
    avatar = models.ImageField(upload_to='images/avatars/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, help_text="Upload your resume (PDF)")
    resume_url = models.URLField(blank=True, null=True, help_text="Or provide a URL to your resume")
    is_available = models.BooleanField(default=True, help_text="Available for work")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Ensure only one profile exists"""
        if not self.pk and Profile.objects.exists():
            raise ValueError("Only one Profile instance is allowed")
        return super().save(*args, **kwargs)


class Project(models.Model):
    """Model for portfolio projects"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.JSONField(default=list, help_text="List of technologies used")
    live_url = models.URLField(blank=True, null=True)
    repo_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images/projects/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Display order (lower = first)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.title


class Skill(models.Model):
    """Model for technical skills"""
    CATEGORY_CHOICES = [
        ('languages', 'Languages'),
        ('ai_ml', 'AI / Machine Learning'),
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('libraries', 'Libraries & Frameworks'),
        ('tools', 'Tools & Databases'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    icon_url = models.URLField(blank=True, null=True, help_text="URL to skill icon/logo")
    proficiency = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Proficiency level (1-5)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', '-proficiency', 'name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(models.Model):
    """Model for work experience"""
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if currently working")
    bullets = models.JSONField(default=list, help_text="List of responsibilities/achievements")
    logo = models.ImageField(upload_to='images/companies/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order (lower = first)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = "Experience"
        verbose_name_plural = "Experience"
    
    def __str__(self):
        return f"{self.role} at {self.company}"
    
    @property
    def is_current(self):
        """Check if this is current employment"""
        return self.end_date is None


class Education(models.Model):
    """Model for education history"""
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    year = models.CharField(max_length=50, help_text="e.g., '2020-2024' or '2024'")
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year']
        verbose_name = "Education"
        verbose_name_plural = "Education"
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"


class ContactInfo(models.Model):
    """
    Singleton model for contact information.
    Only one instance should exist.
    """
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    availability_note = models.TextField(
        blank=True,
        null=True,
        help_text="e.g., 'Available for freelance work' or 'Open to opportunities'"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return f"Contact: {self.email}"
    
    def save(self, *args, **kwargs):
        """Ensure only one contact info exists"""
        if not self.pk and ContactInfo.objects.exists():
            raise ValueError("Only one ContactInfo instance is allowed")
        return super().save(*args, **kwargs)


class SocialLink(models.Model):
    """Model for social media links"""
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('medium', 'Medium'),
        ('dev', 'Dev.to'),
        ('other', 'Other'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_url = models.URLField(blank=True, null=True, help_text="Custom icon URL (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower = first)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'platform']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
    
    def __str__(self):
        return f"{self.get_platform_display()}: {self.url}"


class SiteSettings(models.Model):
    """
    Singleton model for frontend appearance controls.
    These values are applied by the portfolio frontend at runtime.
    """
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('custom', 'Custom'),
    ]
    HERO_LAYOUT_CHOICES = [
        ('classic', 'Classic'),
        ('centered', 'Centered'),
        ('split', 'Split'),
    ]
    FONT_CHOICES = [
        ('classic', 'Classic Serif'),
        ('modern', 'Modern Sans'),
        ('system', 'System UI'),
    ]

    site_title = models.CharField(max_length=200, default='Karthik Aarupalli')
    meta_description = models.TextField(
        default='Portfolio of Karthik Aarupalli - AI Engineer specializing in intelligent automation, deep learning, and full-stack development.'
    )
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')
    font_style = models.CharField(max_length=20, choices=FONT_CHOICES, default='classic')
    hero_layout = models.CharField(max_length=20, choices=HERO_LAYOUT_CHOICES, default='classic')

    background_color = models.CharField(max_length=20, default='#FFFFFF')
    surface_color = models.CharField(max_length=20, default='#F5F5F7')
    text_color = models.CharField(max_length=20, default='#1D1D1F')
    secondary_text_color = models.CharField(max_length=20, default='#6E6E73')
    accent_color = models.CharField(max_length=20, default='#BF8A30')
    accent_dim_color = models.CharField(max_length=20, default='#9A7028')
    background_image = models.ImageField(upload_to='images/backgrounds/', blank=True, null=True)

    custom_css = models.TextField(
        blank=True,
        help_text='Optional advanced CSS. Use carefully; it is injected into the live portfolio.'
    )
    draft_mode = models.BooleanField(
        default=False,
        help_text='When enabled, use /?preview=1 to review changes before turning this off.'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        """Ensure only one settings record exists."""
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one SiteSettings instance is allowed")
        return super().save(*args, **kwargs)


class Section(models.Model):
    """
    Controls top-level portfolio sections.
    The frontend reads this table to show, hide, rename, and order sections.
    """
    SECTION_CHOICES = [
        ('home', 'Home'),
        ('about', 'About'),
        ('skills', 'Skills'),
        ('projects', 'Projects'),
        ('experience', 'Experience'),
        ('contact', 'Contact'),
    ]

    key = models.CharField(max_length=30, choices=SECTION_CHOICES, unique=True)
    nav_label = models.CharField(max_length=60)
    section_label = models.CharField(max_length=80, blank=True)
    heading = models.CharField(max_length=160, blank=True)
    is_visible = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.nav_label


class ContactMessage(models.Model):
    """Model to store contact form messages sent by visitors"""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

