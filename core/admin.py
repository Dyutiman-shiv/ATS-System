import json
# Django Includes
from django import forms
from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from django.shortcuts import render, HttpResponse

admin.site.site_header = 'LaunchxLabs Admin'

from core.models import JobDescription, Candidate, JobApplication, ReferralSource

class ReferralLinkGenerationForm(forms.Form):
    job = forms.ModelChoiceField(queryset=JobDescription.objects.filter(is_active=True), label="Select Job", empty_label="Select a Job")
    referral_source = forms.ModelChoiceField(queryset=ReferralSource.objects.all(), label="Select Referral Source", empty_label="Select Referral Source")

class ReferralLinkGenerationAdmin(admin.ModelAdmin):
    change_list_template = "core/admin/referral_link_generation.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('generate_link/', self.admin_site.admin_view(self.generate_link), name='generate_referral_link'),
        ]
        return my_urls + urls

    def generate_link(self, request):
        if request.method == 'POST':
            form = ReferralLinkGenerationForm(request.POST)
            if form.is_valid():
                job = form.cleaned_data['job']
                referral_source = form.cleaned_data['referral_source']
                generated_link = f"http://yourdomain.com/jobs/{job.pub_id}/apply/?ref={referral_source.code}"
                return HttpResponse(generated_link)
        else:
            form = ReferralLinkGenerationForm()
        return render(request, "core/admin/referral_link_generation.html", {'form': form})

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        if request.method == 'POST':
            form = ReferralLinkGenerationForm(request.POST)
            if form.is_valid():
                job = form.cleaned_data['job']
                referral_source = form.cleaned_data['referral_source']
                generated_link = f"http://yourdomain.com/jobs/{job.pub_id}/apply/?ref={referral_source.code}"
                extra_context['generated_link'] = generated_link
        else:
            form = ReferralLinkGenerationForm()

        extra_context['form'] = form # Add the form to the context
        cl = super().changelist_view(request, extra_context=extra_context)
        return cl

admin.site.register(ReferralSource, ReferralLinkGenerationAdmin)

class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_type', 'location', 'short_experience', 'short_about', 'short_responsibilities', 'short_skills_required', 'short_qualifications', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'location')
    list_filter = ('is_active', 'location')
    ordering = ('-created_at',)

    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def short_experience(self, obj):
        return self.truncate_text(obj.experience)
    short_experience.short_description = 'Experience'

    def short_about(self, obj):
        return self.truncate_text(obj.about)
    short_about.short_description = 'About'

    def short_responsibilities(self, obj):
        return self.truncate_text(obj.responsibilities)
    short_responsibilities.short_description = 'Responsibilities'

    def short_skills_required(self, obj):
        return self.truncate_text(obj.skills_required)
    short_skills_required.short_description = 'Skills Required'

    def short_qualifications(self, obj):
        return self.truncate_text(obj.qualifications)
    short_qualifications.short_description = 'Qualifications'

    def truncate_text(self, text, length=30):
        if len(text) > length:
            return text[:length] + '...'
        return text

admin.site.register(JobDescription, JobDescriptionAdmin)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('hq_user','score', 'public_profile', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    readonly_fields = ('public_profile','pub_id','score')
    fields = ('pub_id','summary', 'public_profile')
    search_fields = ['hq_user__name']
    def has_add_permission(self, request,obj=None):
        return True
    def has_delete_permission(self, request,obj=None):
        return False
    def has_change_permission(self, request,obj=None):
        return True
    def public_profile(self,obj):
        if obj is not None:
            return mark_safe('<a href="/%s" target="_blank">profile</a>' % (obj.public_profile_name,))
        else:
            return None
    def score(self, obj):
        if obj is not None:
            prof =  json.loads(obj.profile_counts)
            if "score" in prof:
                return prof["score"]
            else:
                return None
        else:
            return None

admin.site.register(Candidate, CandidateAdmin)

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'job', 'status', 'phone_number', 'current_ctc', 'expected_ctc', 'current_location', 'notice_period', 'willing_to_locate', 'created_at', 'resume', 'referral_source', 'comments')
    list_editable = ('status',)
    list_filter = ('status', 'created_at', 'job', 'willing_to_locate')
    ordering = ('-created_at',)
    readonly_fields = ('candidate_name', 'job', 'phone_number', 'current_ctc', 'expected_ctc', 'current_location', 'notice_period', 'willing_to_locate', 'created_at', 'resume', 'referral_source', 'experience_years', 'email', 'stage', 'miner', 'candidate', 'education', 'current_company', 'jd' )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['status'].widget.attrs.pop('readonly', None)
            form.base_fields['comments'].widget.attrs.pop('readonly', None)
        return form

    def comments(self, obj):
        return self.truncate_text(obj.comments)
    comments.short_description = 'Comments'

    def truncate_text(self, text, length=30):
        if len(text) > length:
            return text[:length] + '...'
        return text

admin.site.register(JobApplication, JobApplicationAdmin)
