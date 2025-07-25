from django.urls import path
from .views import dashboard, settings_view, edit_profile, CustomEmailView

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('settings/', settings_view, name='settings'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    
    # This handles the email management form and redirection after sending verification
    path('manage-email/', CustomEmailView.as_view(), name='account_email'),  # <--- added this
]
