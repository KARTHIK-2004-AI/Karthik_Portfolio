"""
Portfolio app URLs - API endpoints routing
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet, ProjectViewSet, SkillViewSet,
    ExperienceViewSet, EducationViewSet, ContactInfoViewSet,
    SocialLinkViewSet, SiteSettingsViewSet, SectionViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'education', EducationViewSet, basename='education')
router.register(r'contact', ContactInfoViewSet, basename='contact')
router.register(r'socials', SocialLinkViewSet, basename='social')
router.register(r'site-settings', SiteSettingsViewSet, basename='site-settings')
router.register(r'sections', SectionViewSet, basename='section')

urlpatterns = [
    path('', include(router.urls)),
]
