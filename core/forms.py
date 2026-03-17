# Django Includes
from django import forms
import core.settings as core_settings
import hq.settings as settings

from core.models import Contact,Candidate, HQUser, JobApplication


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name','is_company','email','subject','message','mobile',)
        widgets = {
            'message': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('title','gender','profile_image','city','summary', 'allow_contact','linkedin_profile','github_profile','twitter_profile')

class HQUserForm(forms.ModelForm):
    class Meta:
        model = HQUser
        fields = ('name', 'mobile')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password_repeat = forms.CharField(widget=forms.PasswordInput())

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('public_profile_enabled','public_profile_name')
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'candidate_name', 'email', 'phone_number', 'current_ctc', 'expected_ctc',
            'experience_years', 'notice_period', 'current_location', 'willing_to_locate',
            'resume', 'education', 'current_company'
        ]
        widgets = {
            'candidate_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name: John Doe',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email: john.doe@example.com',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number: 1234567890',
                'required': True
            }),
            'current_ctc': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Current CTC in Inr: 10',
                'required': True
            }),
            'expected_ctc': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Expected CTC in Inr: 15',
                'required': True
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of Experience: 5',
                'required': True
            }),
            'notice_period': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Notice Period in Days: 60',
                'required': True
            }),
            'current_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'current address: 123 Main St, City',
                'required': True
            }),
            'willing_to_locate': forms.RadioSelect(choices=JobApplication.RELOCATE_CHOICES, attrs={
                'class': 'form-control',
                'required': True
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'required': True
            }),
        }
        error_messages = {
            'candidate_name': {'required': 'This is mandatory'},
            'email': {'required': 'This is mandatory'},
            'phone_number': {'required': 'This is mandatory'},
            'current_ctc': {'required': 'This is mandatory'},
            'expected_ctc': {'required': 'This is mandatory'},
            'experience_years': {'required': 'This is mandatory'},
            'notice_period': {'required': 'This is mandatory'},
            'current_location': {'required': 'This is mandatory'},
            'willing_to_locate': {'required': 'This is mandatory'},
            'resume': {'required': 'This is mandatory'},
            'education': {'required': 'This is mandatory'},
            'current_company': {'required': 'This is mandatory'},
        }