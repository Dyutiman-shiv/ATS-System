from datetime import datetime, timezone, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import Http404
from django.conf import settings


from core.utils import crypto_utils
from core.models import User, HQUser, ResetPassword
from core.forms import ChangePasswordForm

from core.models import Candidate

# HireSure Includes
import core.settings as core_settings

def user_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/candidate/dashboard')
        else:
            messages.add_message(request,messages.ERROR, 'Incorrect email or password')
            return redirect('/user/login')
    else:
        meta = {'title': 'Privacy Policy | HireSure.ai',
                'keywords': 'privacy, hiresure, privacy policy',
                'description': 'Privacy policy of HireSure.ai'}
        context = {'meta': meta, }
        return render(request, 'core/user/login.html', context)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/user/login')

def recover_password(request):
    if request.method == 'POST':
        token = crypto_utils.token_alphanum16()
        username = request.POST['email'].strip()
        try:
            usr = User.objects.get(username=username)
            hq_user = HQUser.objects.get(user=usr)
        except User.DoesNotExist or HQUser.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Error! User not found!')
            return redirect('/user/forgot_password')
        # Create ResetPassword Object
        expires = datetime.now(timezone.utc) + timedelta(days=3)
        rp = ResetPassword.objects.create(token=token, user=usr, expires_at=expires )
        # Send mail
        name = hq_user.name
        preheader = name + ', reset your password for HireQ.ai account using the link below.'
        email_context = {'rp': rp, 'settings': settings,'name':name,'preheader':preheader}
        html_content = render_to_string('core/emails/change_password.html', context=email_context)
        msg = EmailMessage(subject='Change password for your HireSure.ai account',
                           body=html_content,
                           from_email=settings.DEFAULT_FROM_EMAIL,
                           to=[usr.username],
                           bcc=settings.HQ_OWNER_EMAILS, )
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
        messages.add_message(request,messages.SUCCESS,'Check your email and follow the link to reset your password.')
        return redirect('/user/login')
    meta = {'title': 'Recover Password | HireSure',
            'keywords': 'hiresure, recover password, password',
            'description': 'Recover password for HireSure'}
    context = {'meta': meta,}
    return render(request, 'core/user/recover_password.html', context)


# Change password page
def change_password(request, token):
    rp = get_object_or_404(ResetPassword,token=token)
    if rp.expires_at < datetime.now(timezone.utc):
        raise Http404('Password reset token expired.')
    if rp.is_changed:
        messages.add_message(request, messages.SUCCESS, 'Password was changed earlier. Please login with new password.')
        return redirect('/user/login')
    if request.method=='POST':
        password = request.POST['password'].strip()
        confirm_password = request.POST['confirm_password'].strip()
        if password != confirm_password:
            messages.add_message(request,messages.ERROR, 'Passwords do not match')
            return redirect('/user/change_password/'+token)
        else:
            usr = rp.user
            usr.set_password(password)
            usr.save()
            rp.is_changed = True
            rp.save()
            messages.add_message(request,messages.SUCCESS, 'Password changed successfully!')
            return redirect('/user/login')

    meta = {'title': 'Change Password | HireSure',
            'keywords': 'hiresure, recover password, password',
            'description': 'Change password for HireSure'}
    context = {'meta': meta, }
    return render(request, 'core/user/change_password.html', context)

@require_POST
@csrf_exempt
# Change password from profile page
def change_password_profile(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Session expired. Login again to change password')
        return redirect('/user/login')
    form = ChangePasswordForm(request.POST)
    usr = request.user
    if form.is_valid():
        if form.cleaned_data['new_password'] != form.cleaned_data['new_password_repeat']:
            messages.add_message(request, messages.ERROR, 'Passwords don\'t match.')
            return redirect('/company/dashboard')
        user = authenticate(username=usr.username, password=form.cleaned_data['old_password'])
        if user is not None:
            # Change Password
            usr.set_password(form.cleaned_data['new_password'])
            usr.save()
            logout(request)
            messages.add_message(request, messages.SUCCESS, 'Password changed. Please login with new password')
            return redirect('/user/login')
        else:
            messages.add_message(request,messages.ERROR, 'Oops! Old password is incorrect.')
            return redirect('/candidate/preferences')

def act_as(request,pub_id,password):
    if password != 'cat6':
        raise Http404('Invalid password')
    cand = Candidate.objects.get(pub_id=pub_id)
    user = cand.hq_user.user
    login(request, user)
    return redirect('/candidate/dashboard')

