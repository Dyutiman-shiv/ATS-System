from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from core.models import JobDescription

@require_GET
def job_descriptions_api(request, pub_id=None):
    if pub_id:
        job = JobDescription.objects.filter(pub_id=pub_id).values(
            'pub_id', 'title', 'job_type', 'location', 'experience', 'about', 'responsibilities', 'skills_required', 'qualifications'
        ).first()
        if job:
            return JsonResponse(job, safe=False)
        else:
            return JsonResponse({'error': 'Job not found'}, status=404)
    else:
        jobs = JobDescription.objects.filter(is_active=True).values(
            'pub_id', 'title', 'job_type', 'location', 'experience', 'about', 'responsibilities', 'skills_required', 'qualifications'
        )
        return JsonResponse(list(jobs), safe=False)