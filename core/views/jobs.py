# Python imports
import json

# djnago imports
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.http import JsonResponse
import time

# App imports
from core.forms import JobApplicationForm
from core.models import JobDescription, JobApplication, Candidate, HQUser, ReferralSource

def index(request):
    return render(request,'core/jobs/all_jobs.html')

def view_job(request, pub_id):
    return render(request,'core/jobs/view.html')



def apply(request, pub_id):
    jd = get_object_or_404(JobDescription, pub_id=pub_id)

    referral_code = request.GET.get('ref')
    referral_source = None

    if referral_code:
        try:
            referral_source = ReferralSource.objects.get(code=referral_code)
        except ReferralSource.DoesNotExist:
            print(f"Invalid referral code: {referral_code}")
    else:
        try:
            referral_source = ReferralSource.objects.get(name="Launchx Website")
        except ReferralSource.DoesNotExist:
            referral_source = ReferralSource.objects.create(name="Launchx Website", code="website")

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.jd = jd

            if request.user.is_authenticated:
                hq_user, created = HQUser.objects.get_or_create(user=request.user)
                candidate, created = Candidate.objects.get_or_create(hq_user=hq_user)
            else:
                hq_user, created = HQUser.objects.get_or_create(
                    user=None,
                    defaults={'name': job_application.candidate_name, 'email': job_application.email}
                )
                candidate, created = Candidate.objects.get_or_create(
                    hq_user=hq_user,
                    defaults={'resume': job_application.resume}
                )

            if not hq_user.email:
                hq_user.email = job_application.email
            if not hq_user.mobile:
                hq_user.mobile = job_application.phone_number
            hq_user.save()

            job_application.candidate = candidate
            job_application.referral_source = referral_source
            job_application.save()

            return JsonResponse({'success': True})
        else:
            return render(request, 'core/jobs/view.html', {'form': form, 'job': jd})
    else:
        form = JobApplicationForm()

    return render(request, 'core/jobs/view.html', {'form': form, 'job': jd})


def job_list(request):
    jobs = JobDescription.objects.filter(is_active=True).order_by('-created_at')
    context = {'jobs': jobs}
    return render(request, 'core/jobs/all_jobs.html', context)

def save_application(request, pub_id):
    """Handles job application submission."""
    jd = get_object_or_404(JobDescription, pub_id=pub_id)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.jd = jd
            job_application.stage = 'APP'
            job_application.status = 'APP'
            
            # Save candidate_name directly from form data
            job_application.candidate_name = form.cleaned_data.get('candidate_name')
            job_application.save()

            messages.success(request, 'Your application has been submitted successfully.')
            return redirect('http://127.0.0.1:8080/about/careers')  # Redirect to job list after submission
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = JobApplicationForm()

    return render(request, 'core/view.html', {'form': form, 'job': jd})