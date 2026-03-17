from django.shortcuts import render

# HireSure Includes
from django.conf import settings
import core.settings as core_settings
import hq.settings as site_settings
from core.utils import crypto_utils


def index(request):
    meta = {'title': 'HireQ.ai | Beautiful looking resumes, pre-verified job/education and access to HireQ network of companies',
            'keywords': 'resume template, job, job portal, job verify',
            'description': 'Get beautiful looking resumes, pre-verify your jobs/education and get access to thousands of companies in HireQ network'}
    context = {'meta': meta, 'core_settings': core_settings, }
    response = render(request, 'core/home.html', context=context)
    response.set_cookie('visitor', crypto_utils.token_alphanum8())
    return response