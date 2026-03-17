from datetime import datetime, timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth.models import User

# HireSure Includes
import core.settings as core_settings

from core.models import Register, HQUser, Candidate
from core.forms import RegisterForm

def start(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            try:
                HQUser.objects.get(email=reg.email)
                messages.add_message(request, messages.ERROR, 'User exists!<br/> <small> You can reset password or choose a different email.</small>', )
                return redirect('/register/start')
            except HQUser.DoesNotExist:
                reg.password = make_password(reg.password)
                reg.email = reg.email.lower()
                reg.name = reg.name.title()
                reg.save()
                # Send mail
                context = {'reg': reg, 'settings': settings, 'name': reg.name, 'core_settings': core_settings}
                html_content = render_to_string('core/emails/registration.html', context=context)
                send_mail(
                    subject='Registration on HireQ.ai',
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reg.email],
                    html_message=html_content,
                    fail_silently=False,
                )
                messages.add_message(request, messages.SUCCESS, 'We have sent a verification link to your email. Please verify your email to proceed.')
                return redirect('/register/start')
    else:
        if 'email' in request.GET:
            form = RegisterForm(initial={'email': request.GET['email']})
        else:
            form = RegisterForm()
    meta = {'title': 'Privacy Policy | HireSure.ai',
            'keywords': 'privacy, hiresure, privacy policy',
            'description': 'Privacy policy of HireSure.ai'}
    context = {'meta': meta, 'form': form}
    return render(request, 'core/register/start.html', context)


"""def start(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create an object
            reg = form.save(commit=False)
            try:
                HQUser.objects.get(email=reg.email)
                # User exists. Throw an error
                messages.add_message(request, messages.ERROR, 'User exists!<br/> <small> You can reset password or choose a different email.</small>', )
                return redirect('/register/start')
            except HQUser.DoesNotExist:
                reg.password = make_password(reg.password)
                reg.email = reg.email.lower()
                reg.name = reg.name.title()
                reg.save()
                # Send mail
                context = {'reg': reg, 'settings':settings, 'name':reg.name, 'core_setings':core_settings }
                html_content = render_to_string('core/emails/registration.html', context=context)
                print(html_content)
                msg = EmailMessage(subject='Registration on HireQ.ai',
                                   body=html_content,
                                   from_email=settings.DEFAULT_FROM_EMAIL,
                                   to=[reg.email],
                                #    bcc=settings.HQ_OWNER_EMAILS, 
                )
                msg.content_subtype = "html"
                msg.send(fail_silently=True)
                messages.add_message(request, messages.SUCCESS, 'We have sent a verification link to your email. Please verify your email to proceed.')
                return redirect('/register/start')
    else:
        if 'email' in request.GET:
            form = RegisterForm(initial={'email':request.GET['email']})
        else:
            form = RegisterForm()
    meta = {'title': 'Privacy Policy | HireSure.ai',
            'keywords': 'privacy, hiresure, privacy policy',
            'description': 'Privacy policy of HireSure.ai'}
    context = {'meta': meta, 'form':form}
    return render(request, 'core/register/start.html', context)"""


"""def confirm_token(request,pub_id,token):
    reg = Register.objects.get(pub_id=pub_id)
    if reg.token != token:
        raise Http404('Invalid token')
    else:
        if reg.email_verified:
            messages.add_message(request, messages.SUCCESS, 'Account is active. Please login')
            return redirect('/user/login')
        elif (datetime.now(timezone.utc) - reg.created_at).days > core_settings.REG_EXPIRY_DAYS:
            # The link is expired. Given message and take to the registration page
            messages.add_message(request, messages.ERROR, 'The link is expired. Please register again')
            return redirect('/register/start')
        else:
            # Create a user
            try:
                usr = User.objects.get(username=reg.email)
                return redirect('/user/login')
            except User.DoesNotExist:
                usr = User.objects.create(username=reg.email, email=reg.email, password=reg.password)
            # Create a HQ User
            hq_user = HQUser.objects.create(user=usr, name=reg.name, email=reg.email, mobile=reg.mobile, country=reg.country)
            # Create a candidate
            cand = Candidate.objects.create(hq_user=hq_user)
            reg.email_verified = True
            reg.verified_at = datetime.now(timezone.utc)
            messages.add_message(request, messages.SUCCESS, 'Email is verified. Please login and create profile')
            return redirect('/user/login')"""

def confirm_token(request, pub_id, token):
    try:
        reg = Register.objects.get(pub_id=pub_id)
        if reg.token != token:
            raise Http404('Invalid token')
        else:
            if reg.email_verified:
                messages.add_message(request, messages.SUCCESS, 'Account is active. Please login')
                return redirect('/user/login')
            elif (datetime.now(timezone.utc) - reg.created_at).days > core_settings.REG_EXPIRY_DAYS:
                messages.add_message(request, messages.ERROR, 'The link is expired. Please register again')
                return redirect('/register/start')
            else:
                usr, created = User.objects.get_or_create(username=reg.email, defaults={'email': reg.email, 'password': reg.password})
                hq_user, created = HQUser.objects.get_or_create(user=usr, defaults={'name': reg.name, 'email': reg.email, 'mobile': reg.mobile, 'country': reg.country})
                
                # Ensure the template_id is set correctly
                default_template = core_settings.DEFAULT_TEMPLATE_ID  # Replace with your default template ID
                cand, created = Candidate.objects.get_or_create(hq_user=hq_user, defaults={'template_id': default_template})
                
                reg.email_verified = True
                reg.verified_at = datetime.now(timezone.utc)
                reg.save()
                
                messages.add_message(request, messages.SUCCESS, 'Email is verified. Please login and create profile')
                return redirect('/user/login')
    except Register.DoesNotExist:
        raise Http404('Invalid registration')
    except Exception as e:
        messages.add_message(request, messages.ERROR, f'An error occurred: {str(e)}')
        return redirect('/register/start')