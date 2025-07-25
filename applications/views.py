from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .models import JobApplication
from resume_builder.models import Resume
from jobs.models import Job


# List of user applications
@login_required
def application_list(request):
    applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'applications/application_list.html', {'applications': applications})


# Apply for a job
@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    user_resumes = Resume.objects.filter(user=request.user)

    if request.method == "POST":
        resume_id = request.POST.get('resume')
        cover_letter = request.POST.get('cover_letter', '')

        # Check if already applied
        if JobApplication.objects.filter(applicant=request.user, job=job).exists():
            messages.warning(request, "You have already applied for this job.")
            return redirect('jobs:job_detail', job_id=job.pk)

        # Create application
        application = JobApplication.objects.create(
            applicant=request.user,
            job=job,
            cover_letter=cover_letter,
        )

        # Attach resume if provided
        if resume_id:
            try:
                resume = Resume.objects.get(pk=resume_id, user=request.user)
                application.resume = resume
                application.save()
            except Resume.DoesNotExist:
                pass

        messages.success(request, "Your application has been submitted.")
        return redirect('jobs:job_detail', job_id=job.pk)

    context = {
        'job': job,
        'user_resumes': user_resumes,
    }
    return render(request, 'applications/apply.html', context)


# Application detail
@login_required
def application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, applicant=request.user)
    return render(request, 'applications/application_detail.html', {'application': application})


# Edit application
class ApplicationUpdateView(UpdateView):
    model = JobApplication
    fields = ['resume', 'cover_letter']
    template_name = 'applications/application_form.html'

    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)

    def get_success_url(self):
        return reverse_lazy('applications:application_detail', kwargs={'pk': self.object.pk})


# Withdraw application
@login_required
def withdraw_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, applicant=request.user)
    if application.status == 'pending':
        application.status = 'withdrawn'
        application.save()
        messages.info(request, "You have withdrawn your application.")
    else:
        messages.warning(request, "You cannot withdraw this application.")
    return redirect('applications:application_detail', pk=pk)
