from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

# Import custom views for email handling (override AllAuth)
from dashboard.views import CustomEmailView, CustomConfirmEmailView

# ------------------------
# Web Routes
# ------------------------
web_patterns = [
    path('admin/', admin.site.urls),  # ✅ Django admin panel
    path('web/', include('resume_builder.web.urls')),
    path('web/', include('accounts.web.urls')),

    # ✅ Override AllAuth's email confirm and resend views
    path('accounts/confirm-email/<key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/email/', CustomEmailView.as_view(), name='account_email'),

    path('accounts/', include('allauth.urls')),  # AllAuth login, logout, signup
    path('jobs/', include('jobs.urls')),         # Jobs listing and detail
    path('applications/', include(('applications.urls', 'applications'), namespace='applications')),
    path('', include('dashboard.urls')),         # Dashboard as homepage
]

# ------------------------
# API Routes
# ------------------------
apis_patterns = [
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include('resume_builder.api.urls')),
    path('api/v1/', include('accounts.api.urls')),
]

# ------------------------
# Final URL Patterns
# ------------------------
urlpatterns = web_patterns + apis_patterns

# ✅ Serve media and static only in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
