"""
Main project URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import FileResponse, Http404
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def portfolio_home(request):
    """Serve the portfolio frontend from the main site URL."""
    index_path = settings.BASE_DIR / 'index.html'
    if not index_path.exists():
        raise Http404("Portfolio frontend not found")
    return FileResponse(index_path.open('rb'), content_type='text/html')


urlpatterns = [
    # Portfolio frontend
    path('', portfolio_home, name='portfolio_home'),

    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('portfolio.urls')),
    
    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from django.views.static import serve
from django.urls import re_path

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

