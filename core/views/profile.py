# Django Includes
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib import messages

from core.models import Candidate

def view(request,public_profile_name):
    if not public_profile_name.isalnum():
        raise Http404('only letters and numbers')
    try:
        cand = Candidate.objects.get(public_profile_name=public_profile_name)
    except Candidate.DoesNotExist:
        raise Http404('No matching profile')
    if not cand.public_profile_enabled:
        raise Http404('profile view is disabled')
    meta = {'title': 'Profile of %s | %s | %s' % (cand.hq_user.name,cand.title, cand.city),
            'keywords': 'profile, %s' % (cand.hq_user.name,),
            'description': 'Profile of %s in HireQ.ai' % (cand.hq_user.name,)}
    context = {'meta': meta, 'page': 'dashboard', 'cand': cand, 'hq_user': cand.hq_user}
    return render(request, 'core/profile/view.html', context)

