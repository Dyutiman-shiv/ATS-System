import pdfkit, json, tldextract

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.utils import dateparse
from django.template import Context, Template

# Third Party Includes
import core.settings as core_settings
from cloudinary.uploader import upload as cloudinary_upload

from core.utils import crypto_utils
from core.models import HQUser, Candidate, JobDescription, JobApplication
from core.forms import CandidateForm, HQUserForm, PreferenceForm

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        hq_user = HQUser.objects.get(email=request.user.email)
        cand = Candidate.objects.get(hq_user=hq_user)
        profile_counts = json.loads(cand.profile_counts)
        jds = JobDescription.objects.order_by('-id')[:8]

        meta = {'title': 'Dashboard of %s | HireQ.ai' % (hq_user.name,),
                'keywords': 'dashboard, %s, profile' % (hq_user.name),
                'description': 'Dashboard of %s | HireQ.ai' % (hq_user.name)}
        context = {'meta': meta,'page':'dashboard', 'cand': cand, 'hq_user': hq_user, 'profile_counts': profile_counts, 'jds':jds}
        return render(request, 'core/candidate/dashboard.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        hq_user = HQUser.objects.get(email=request.user.email)
        cand = Candidate.objects.get(hq_user=hq_user)
        profile_counts = json.loads(cand.profile_counts)
        if request.method == 'POST':
            cand_form = CandidateForm(request.POST, request.FILES or None, instance=cand)
            hq_user_form = HQUserForm(request.POST,instance=hq_user)
            if cand_form.is_valid() and hq_user_form.is_valid():
                cand_form.save()
                if len(request.FILES) > 0:
                    # Create thumbnail for profile
                    cl_resp = cloudinary_upload(cand.profile_image, width=256, height=256, format='jpg', gravity='face', crop='thumb')
                    cand.thumbnail_url = cl_resp['secure_url']
                    cand.save()
                hq_user_form.save()
                messages.add_message(request, messages.SUCCESS, 'Profile data updated successfully')
                return redirect('/candidate/profile')

        else:
            cand_form = CandidateForm(instance=cand)
            hq_user_form = HQUserForm(instance=hq_user)
        meta = {'title': 'HireQ.ai account preferences | %s' % (cand.hq_user.name,),
                'keywords': 'HireQ.ai, account preferences',
                'description': 'Account Preferences HireQ.ai'}
        context = {'meta': meta,'page':'about', 'cand':cand, 'hq_user':hq_user, 'cand_form':cand_form, 'hq_user_form':hq_user_form, 'profile_counts': profile_counts }
        return render(request, 'core/candidate/profile.html', context)

def preferences(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        hq_user = HQUser.objects.get(email=request.user.email)
        cand = Candidate.objects.get(hq_user=hq_user)
        profile_counts = json.loads(cand.profile_counts)
        if request.method == 'POST':
            pref_form = PreferenceForm(request.POST, instance=cand)
            if pref_form.is_valid():
                pref_form.save()
                messages.add_message(request, messages.SUCCESS, 'Preferences updated successfully!')
                return redirect('/candidate/preferences')
        else:
            pref_form = PreferenceForm(instance=cand)
        meta = {'title': 'Preferences | %s' % (cand.hq_user.name),
                'keywords': 'preferences, hireq',
                'description': 'Change your preferences here.'}
        context = {'meta': meta,'page':'prefs', 'cand':cand, 'hq_user':hq_user, 'profile_counts': profile_counts, 'pref_form':pref_form }
        return render(request, 'core/candidate/preferences.html', context)


