from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy

from applications.models import JobApplication
from resume_builder.models import Resume
from jobs.models import Job

from allauth.account.models import EmailAddress
from allauth.account.views import EmailView, ConfirmEmailView


# ------------------------
# Custom Confirm Email View (redirect after email confirmation)
# ------------------------
class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)

        if self.object:  # If confirmation was successful
            messages.success(self.request, "Your email has been confirmed. Thank you!")
            return redirect('dashboard')  # Redirect to dashboard after verification

        return response


# ------------------------
# Custom Email View (resend verification email → redirect to settings)
# ------------------------
class CustomEmailView(EmailView):
    def form_valid(self, form):
        messages.success(self.request, "Verification email sent successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('settings')


# ------------------------
# Dashboard View
# ------------------------
@login_required(login_url='/accounts/login/')
def dashboard(request):
    user = request.user

    recent_applications = JobApplication.objects.filter(applicant=user).order_by('-applied_date')[:5]
    recent_resumes = Resume.objects.filter(user=user).order_by('-last_modified')[:5]

    recent_activities = []

    for app in recent_applications:
        recent_activities.append({
            'time': app.applied_date,
            'type': 'success',
            'content': f'You applied for {app.job.title}'
        })

    for resume in recent_resumes:
        recent_activities.append({
            'time': resume.last_modified,
            'type': 'info',
            'content': f'You updated resume: {resume.title}'
        })

    recent_activities.sort(key=lambda x: x['time'], reverse=True)

    context = {
        'total_resumes': Resume.objects.filter(user=user).count(),
        'total_applications': JobApplication.objects.filter(applicant=user).count(),
        'total_jobs': Job.objects.count(),
        'recent_applications': recent_applications,
        'recent_resumes': recent_resumes,
        'recent_activities': recent_activities,
    }

    return render(request, 'dashboard/dashboard.html', context)


# ------------------------
# Settings View (profile + password)
# ------------------------
@login_required(login_url='/accounts/login/')
def settings_view(request):
    user = request.user
    email_verified = EmailAddress.objects.filter(user=user, verified=True).exists()

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.phone = request.POST.get('phone')
            user.save()
            messages.success(request, 'Profile updated successfully.')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('settings')
        else:
            password_form = PasswordChangeForm(user)
    else:
        password_form = PasswordChangeForm(user)

    context = {
        'email_verified': email_verified,
        'password_form': password_form,
    }

    return render(request, 'dashboard/settings.html', context)


# ------------------------
# Edit Profile View
# ------------------------
@login_required(login_url='/accounts/login/')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('settings')

    return render(request, 'dashboard/edit_profile.html', {'user': user})
