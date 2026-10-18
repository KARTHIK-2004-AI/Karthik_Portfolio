"""
Portfolio app serializers - DRF serializers for all models
"""
from rest_framework import serializers
from .models import (
    Profile, Project, Skill, Experience, 
    Education, ContactInfo, SocialLink, SiteSettings, Section,
    ContactMessage
)


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    avatar_url = serializers.SerializerMethodField()
    resume_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'tagline', 'about', 'avatar', 'avatar_url',
            'resume', 'resume_file_url', 'resume_url', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_avatar_url(self, obj):
        """Return absolute URL for avatar image"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None
    
    def get_resume_file_url(self, obj):
        """Return absolute URL for resume file"""
        if obj.resume:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.resume.url)
            return obj.resume.url
        return None


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'tech_stack', 'live_url',
            'repo_url', 'thumbnail', 'thumbnail_url',
            'journey', 'challenges', 'architecture',
            'is_featured', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_thumbnail_url(self, obj):
        """Return absolute URL for thumbnail image"""
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None
    
    def validate_tech_stack(self, value):
        """Ensure tech_stack is a list"""
        if not isinstance(value, list):
            raise serializers.ValidationError("tech_stack must be a list of strings")
        return value


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category', 'category_display', 'icon_url',
            'proficiency', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for Experience model"""
    logo_url = serializers.SerializerMethodField()
    is_current = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Experience
        fields = [
            'id', 'company', 'role', 'start_date', 'end_date',
            'bullets', 'logo', 'logo_url', 'is_current', 'order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_logo_url(self, obj):
        """Return absolute URL for company logo"""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    
    def validate_bullets(self, value):
        """Ensure bullets is a list"""
        if not isinstance(value, list):
            raise serializers.ValidationError("bullets must be a list of strings")
        return value


class EducationSerializer(serializers.ModelSerializer):
    """Serializer for Education model"""
    
    class Meta:
        model = Education
        fields = [
            'id', 'institution', 'degree', 'year', 'description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactInfoSerializer(serializers.ModelSerializer):
    """Serializer for ContactInfo model"""
    
    class Meta:
        model = ContactInfo
        fields = [
            'id', 'email', 'phone', 'availability_note',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SocialLinkSerializer(serializers.ModelSerializer):
    """Serializer for SocialLink model"""
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = SocialLink
        fields = [
            'id', 'platform', 'platform_display', 'url', 'icon_url',
            'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer for runtime portfolio appearance settings"""
    background_image_url = serializers.SerializerMethodField()
    theme_display = serializers.CharField(source='get_theme_display', read_only=True)
    font_style_display = serializers.CharField(source='get_font_style_display', read_only=True)
    hero_layout_display = serializers.CharField(source='get_hero_layout_display', read_only=True)

    class Meta:
        model = SiteSettings
        fields = [
            'id', 'site_title', 'meta_description', 'theme', 'theme_display',
            'font_style', 'font_style_display', 'hero_layout', 'hero_layout_display',
            'background_color', 'surface_color', 'text_color', 'secondary_text_color',
            'accent_color', 'accent_dim_color', 'background_image', 'background_image_url',
            'custom_css', 'draft_mode', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_background_image_url(self, obj):
        """Return absolute URL for background image"""
        if obj.background_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.background_image.url)
            return obj.background_image.url
        return None


class SectionSerializer(serializers.ModelSerializer):
    """Serializer for top-level section controls"""
    key_display = serializers.CharField(source='get_key_display', read_only=True)

    class Meta:
        model = Section
        fields = [
            'id', 'key', 'key_display', 'nav_label', 'section_label',
            'heading', 'is_visible', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectReorderSerializer(serializers.Serializer):
    """Serializer for reordering projects"""
    id = serializers.IntegerField()
    order = serializers.IntegerField()


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

