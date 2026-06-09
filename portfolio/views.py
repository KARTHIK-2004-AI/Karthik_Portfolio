"""
Portfolio app views - DRF ViewSets for all models
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import (
    Profile, Project, Skill, Experience,
    Education, ContactInfo, SocialLink, SiteSettings, Section
)
from .serializers import (
    ProfileSerializer, ProjectSerializer, SkillSerializer,
    ExperienceSerializer, EducationSerializer, ContactInfoSerializer,
    SocialLinkSerializer, SiteSettingsSerializer, SectionSerializer,
    ProjectReorderSerializer
)
from .permissions import IsAdminOrReadOnly


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Profile (singleton).
    GET: Retrieve profile
    PUT/PATCH: Update profile (admin only)
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'put', 'patch']  # No POST or DELETE
    
    def list(self, request, *args, **kwargs):
        """Return single profile object instead of list"""
        profile = Profile.objects.first()
        if profile:
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve profile by ID"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Projects.
    Supports full CRUD operations.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAdminOrReadOnly])
    def reorder(self, request):
        """
        Reorder projects.
        Expects: [{"id": 1, "order": 0}, {"id": 2, "order": 1}, ...]
        """
        serializer = ProjectReorderSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        
        for item in serializer.validated_data:
            project = get_object_or_404(Project, id=item['id'])
            project.order = item['order']
            project.save()
        
        return Response({"detail": "Projects reordered successfully"})


class SkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Skills.
    Supports full CRUD operations.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['category']  # Allow filtering by category


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Experience.
    Supports full CRUD operations.
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAdminOrReadOnly]


class EducationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Education.
    Supports full CRUD operations.
    """
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAdminOrReadOnly]


class ContactInfoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ContactInfo (singleton).
    GET: Retrieve contact info
    PUT/PATCH: Update contact info (admin only)
    """
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'put', 'patch']  # No POST or DELETE
    
    def list(self, request, *args, **kwargs):
        """Return single contact info object instead of list"""
        contact = ContactInfo.objects.first()
        if contact:
            serializer = self.get_serializer(contact)
            return Response(serializer.data)
        return Response({"detail": "Contact info not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve contact info by ID"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SocialLinkViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Social Links.
    Supports full CRUD operations.
    """
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAdminOrReadOnly]


class SiteSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SiteSettings (singleton).
    GET: Retrieve frontend appearance settings
    PUT/PATCH: Update settings (admin only)
    """
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'put', 'patch']

    def list(self, request, *args, **kwargs):
        """Return single settings object instead of list"""
        settings, _ = SiteSettings.objects.get_or_create()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve settings by ID"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for top-level portfolio sections.
    Admins can update labels, visibility, headings, and ordering.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrReadOnly]
