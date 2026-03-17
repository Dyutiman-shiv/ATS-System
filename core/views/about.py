# Django Includes
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

# HireSure Includes
import core.settings as core_settings
from core.forms import ContactForm
#from core.views.faqs import *

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send mail
            context = {'email': {'name': contact.name,'is_company':contact.is_company, 'mobile': contact.mobile,'email':contact.email,'subject':contact.subject, 'message': contact.message}}
            html_content = render_to_string('core/emails/contact.html', context=context)
            msg = EmailMessage(subject='Contact Message on HireQ.ai',
                               body=html_content,
                               from_email=settings.DEFAULT_FROM_EMAIL,
                               to=settings.CS_MANAGER_EMAILS,
                               bcc=settings.HQ_OWNER_EMAILS, )
            msg.content_subtype = "html"
            msg.send(fail_silently=True)
            messages.add_message(request, messages.SUCCESS, 'Your message is received! We will get back in 1-2 working days.')
            return HttpResponseRedirect('/about/contact')
    else:
        form = ContactForm()
    meta = {'title': 'Contact Us | HireQ.ai',
            'keywords': 'contact us, HireQ, work history',
            'description': 'Contact HireQ through this page.'}
    context = {'meta': meta,'form':form, 'core_settings': core_settings,}
    return render(request, 'core/about/contact.html', context)

def faqs(request):
    meta = {'title': 'Frequently Asked Questions (FAQs) | HireSure.ai',
            'keywords': 'faq, hiresure',
            'description': 'Frequently asked questions for companies and candidates'}
    context = {'meta': meta, 'core_settings':core_settings}
    return render(request, 'core/about/faqs.html', context)

def privacy(request):
    meta = {'title': 'Privacy Policy | HireSure.ai',
            'keywords': 'privacy, hiresure, privacy policy',
            'description': 'Privacy policy of HireSure.ai'}
    context = {'meta': meta,'core_settings':core_settings}
    return render(request, 'core/about/privacy.html', context)

def terms(request):
    meta = {'title': 'Terms of Use | HireSure.ai',
            'keywords': 'terms, tnc, terms and conditions, hiresure',
            'description': 'Terms of use for HireSure.ai'}
    context = {'meta': meta, 'core_settings':core_settings}
    return render(request, 'core/about/terms.html', context)

def error_404(request, exception):
    meta = {'title':'Error 4XX! Page not found | HireSure.ai', }
    #if 'tried' in exception:
    # This causes 500 errors
    #   exception = 'The page you requested could not be fond. Please go back to the homepage.'
    context = {'name':'name', 'meta':meta, 'exception':exception, 'settings':settings}
    response =  render(request, 'core/404.html', context)
    response.status_code = 404
    return response

def error_500(request):
    meta = {'title':'Error 5XX! Server Error | HireSure.ai', }
    context = {'name':'name', 'meta':meta, 'settings':settings }
    response = render(request, 'core/500.html', context)
    response.status_code = 500
    return response