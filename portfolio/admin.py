"""
Portfolio app admin - Django admin customization
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Profile, Project, Skill, Experience,
    Education, ContactInfo, SocialLink,
    SiteSettings, Section
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for Profile model"""
    list_display = ['name', 'tagline', 'is_available', 'updated_at']
    list_editable = ['is_available']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'about')
        }),
        ('Media', {
            'fields': ('avatar', 'avatar_preview', 'resume', 'resume_preview', 'resume_url')
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
    )
    
    readonly_fields = ['avatar_preview', 'resume_preview']
    
    def avatar_preview(self, obj):
        """Display avatar preview in admin"""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 50%;" />',
                obj.avatar.url
            )
        return "No avatar uploaded"
    avatar_preview.short_description = "Avatar Preview"
    
    def resume_preview(self, obj):
        """Display resume download link in admin"""
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank" class="button" style="padding: 10px 15px; background: #BF8A30; color: white; text-decoration: none; border-radius: 5px; display: inline-block;">'
                '<span style="margin-right: 8px;">📄</span> Download Resume'
                '</a>'
                '<p style="margin-top: 10px; color: #666; font-size: 12px;">File: {}</p>',
                obj.resume.url,
                obj.resume.name.split('/')[-1]
            )
        return format_html(
            '<p style="color: #999;">No resume uploaded yet</p>'
            '<p style="margin-top: 8px; font-size: 12px; color: #666;">Upload a PDF file using the "Resume" field above</p>'
        )
    resume_preview.short_description = "Current Resume"
    
    def has_add_permission(self, request):
        """Prevent adding more than one profile"""
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting the profile"""
        return False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin for Project model"""
    list_display = ['title', 'is_featured', 'order', 'created_at', 'thumbnail_preview']
    list_editable = ['is_featured', 'order']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description', 'tech_stack')
        }),
        ('Links', {
            'fields': ('live_url', 'repo_url')
        }),
        ('Media', {
            'fields': ('thumbnail', 'thumbnail_preview')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
    )
    
    readonly_fields = ['thumbnail_preview', 'created_at', 'updated_at']
    
    def thumbnail_preview(self, obj):
        """Display thumbnail preview in admin"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px;" />',
                obj.thumbnail.url
            )
        return "No thumbnail uploaded"
    thumbnail_preview.short_description = "Thumbnail Preview"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin for Skill model"""
    list_display = ['name', 'category', 'proficiency', 'icon_display']
    list_filter = ['category', 'proficiency']
    search_fields = ['name']
    ordering = ['category', '-proficiency', 'name']
    
    def icon_display(self, obj):
        """Display skill icon if available"""
        if obj.icon_url:
            return format_html(
                '<img src="{}" style="width: 32px; height: 32px;" />',
                obj.icon_url
            )
        return "No icon"
    icon_display.short_description = "Icon"


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Admin for Experience model"""
    list_display = ['company', 'role', 'start_date', 'end_date', 'is_current', 'order']
    list_editable = ['order']
    list_filter = ['start_date', 'end_date']
    search_fields = ['company', 'role']
    ordering = ['order', '-start_date']
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company', 'role', 'logo', 'logo_preview')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date')
        }),
        ('Details', {
            'fields': ('bullets',)
        }),
        ('Display Settings', {
            'fields': ('order',)
        }),
    )
    
    readonly_fields = ['logo_preview']
    
    def logo_preview(self, obj):
        """Display company logo preview in admin"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px;" />',
                obj.logo.url
            )
        return "No logo uploaded"
    logo_preview.short_description = "Logo Preview"


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Admin for Education model"""
    list_display = ['institution', 'degree', 'year']
    search_fields = ['institution', 'degree']
    ordering = ['-year']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Admin for ContactInfo model"""
    list_display = ['email', 'phone', 'updated_at']
    
    fieldsets = (
        ('Contact Details', {
            'fields': ('email', 'phone')
        }),
        ('Availability', {
            'fields': ('availability_note',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent adding more than one contact info"""
        if ContactInfo.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting contact info"""
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """Admin for SocialLink model"""
    list_display = ['platform', 'url', 'order', 'icon_display']
    list_editable = ['order']
    list_filter = ['platform']
    ordering = ['order', 'platform']
    
    def icon_display(self, obj):
        """Display social icon if available"""
        if obj.icon_url:
            return format_html(
                '<img src="{}" style="width: 24px; height: 24px;" />',
                obj.icon_url
            )
        return "Default icon"
    icon_display.short_description = "Icon"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin for Site Settings"""
    list_display = ['site_title', 'theme', 'draft_mode', 'updated_at']
    
    fieldsets = (
        ('General', {
            'fields': ('site_title', 'meta_description', 'draft_mode')
        }),
        ('Appearance', {
            'fields': ('theme', 'font_style', 'hero_layout')
        }),
        ('Colors', {
            'fields': (
                'background_color',
                'surface_color',
                'text_color',
                'secondary_text_color',
                'accent_color',
                'accent_dim_color',
            ),
            'classes': ('collapse',)
        }),
        ('Background', {
            'fields': ('background_image',),
            'classes': ('collapse',)
        }),
        ('Advanced', {
            'fields': ('custom_css',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent adding more than one settings"""
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting settings"""
        return False


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """Admin for Section model"""
    list_display = ['key', 'nav_label', 'is_visible', 'order']
    list_editable = ['nav_label', 'is_visible', 'order']
    list_filter = ['is_visible']
    ordering = ['order', 'id']
    
    fieldsets = (
        ('Section Configuration', {
            'fields': ('key', 'nav_label', 'section_label', 'heading')
        }),
        ('Display Settings', {
            'fields': ('is_visible', 'order')
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manually adding sections - they should be auto-created"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting sections"""
        return obj.key != 'home' if obj else False


# Customize admin site header and title
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"
