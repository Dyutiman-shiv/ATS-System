from datetime import date

from django.db import models
from django.contrib.auth.models import User


# HireSure Includes
import core.settings as core_settings
from core.utils import crypto_utils

# Create your models here.
class ResetPassword(models.Model):
    token = models.CharField(unique=True, max_length=core_settings.FIELD_LENGTHS['pub_id'])
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    expires_at = models.DateTimeField()
    is_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'core_reset_password'

class Contact(models.Model):
    name = models.CharField(max_length=core_settings.FIELD_LENGTHS['name'])
    is_company = models.BooleanField(default=False)
    mobile = models.CharField(max_length=core_settings.FIELD_LENGTHS['mobile'])
    subject = models.CharField(max_length=128)
    email = models.EmailField()
    message = models.CharField(max_length=core_settings.FIELD_LENGTHS['long_comment'])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class HQUser(models.Model):
    user = models.OneToOneField(User,unique=True, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=core_settings.FIELD_LENGTHS['name'])
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=core_settings.FIELD_LENGTHS['mobile'])
    country = models.CharField(max_length=4, default='IN', choices=core_settings.COUNTRY_CODES_REGISTER)
    user_type = models.CharField(max_length=16, default='CAND', choices=core_settings.USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    def first_name(self):
        return self.name.split(' ')[0]
    class Meta:
        db_table = 'core_hq_user'

class Candidate(models.Model):
    pub_id = models.CharField(unique=True,default=crypto_utils.token_alphanum8, max_length=core_settings.FIELD_LENGTHS['pub_id'], editable=False)
    hq_user = models.ForeignKey(HQUser, on_delete=models.PROTECT)
    profile_image = models.FileField(null=True, blank=True, upload_to='profile_images/')
    thumbnail_url = models.URLField(default='https://res.cloudinary.com/hiresure/image/upload/v1580884239/k9boew6yg0fsvzv0.jpg')
    title = models.CharField(max_length=64)
    gender = models.CharField(default='O', max_length=16, choices=core_settings.GENDER_CHOICES)
    dob = models.DateField(null=True, blank=True)
    summary = models.CharField(null=True, max_length=1024)
    city = models.CharField(null=True, max_length=64)
    resume = models.FileField(null=True, blank=True, upload_to='resumes/')
    profile_counts = models.CharField(default= '{"jobs": 0, "skills": 0, "edus": 0, "certs": 0, "score": 0}',max_length=1024, )
    allow_contact = models.BooleanField(default=True)
    public_profile_enabled = models.BooleanField(default=True)
    public_profile_name = models.CharField(unique=True, default=crypto_utils.token_alphanum8, max_length=core_settings.FIELD_LENGTHS['pub_id'] )
    linkedin_profile = models.CharField(null=True, blank=True, max_length=128)
    github_profile = models.CharField(null=True, blank=True, max_length=128)
    twitter_profile = models.CharField(null=True, blank=True, max_length=128)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.hq_user.name

class JobDescription(models.Model):
    pub_id = models.CharField(default=crypto_utils.token_alphanum8, null=True, blank=True, max_length=16)
    title = models.CharField(max_length=256)
    job_type = models.CharField(max_length=128, default='Full Time')  # Added field for job type
    location = models.CharField(max_length=128)
    experience = models.CharField(max_length=128, null=True)  # Added field for experience
    about = models.TextField()  # Changed to TextField for longer content
    responsibilities = models.TextField(null=True)  # Changed to TextField for longer content
    skills_required = models.TextField()  # Changed to TextField for longer content
    qualifications = models.TextField(null=True)  # Changed to TextField for longer content
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "core_job_description"

class Miner(models.Model):
    pub_id = models.CharField(unique=True, default=crypto_utils.token_alphanum8, max_length=core_settings.FIELD_LENGTHS['pub_id'], editable=False)
    hq_user = models.ForeignKey(HQUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MinerJDMap(models.Model):
    miner = models.ForeignKey(Miner, on_delete=models.PROTECT)
    jd = models.ForeignKey(JobDescription, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'core_miner_jd_map'

class ReferralSource(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="e.g., LinkedIn, Indeed, Company Website")
    code = models.CharField(max_length=50, unique=True, help_text="A short, unique code for the URL parameter. e.g., linkedin, indeed, website", primary_key=True)

    def __str__(self):
        return self.name
    
class JobApplication(models.Model):

    RELOCATE_CHOICES = [
        ('no', 'No'),
        ('undecided', 'Undecided'),
        ('yes', 'Yes'),
    ]
    
    jd = models.ForeignKey(JobDescription, on_delete=models.PROTECT)
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT)
    miner = models.ForeignKey(Miner, null=True, blank=True, on_delete=models.PROTECT)
    stage = models.CharField(max_length=32, choices=core_settings.JOB_APPLICATION_STAGE)
    status = models.CharField(max_length=32, choices=core_settings.JOB_APPLICATION_STATUS)
    job = models.CharField(max_length=256, null=True)  # New field for job title
    candidate_name = models.CharField(max_length=256, null=True)  # New field for candidate name
    resume = models.FileField(upload_to='resumes/', null=True)  # New field for resume upload
    expected_ctc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Expected CTC(LPA)")
    current_ctc = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Current CTC(LPA)")  # New field for expected salary
    current_location = models.CharField(max_length=256, null=True, verbose_name="Current location(City)")
    notice_period = models.CharField(max_length=256, null=True)
    willing_to_locate = models.CharField(max_length=32, choices=RELOCATE_CHOICES, default='undecided')
    experience_years = models.IntegerField(null=True, blank=True, verbose_name="Years Of Experience")  # New field for experience years
    referral_source = models.ForeignKey(ReferralSource, on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to ReferralSource
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # New field for phone number
    email = models.EmailField(null=True, blank=True)  # New field for email
    education = models.CharField(max_length=256, null=True, blank=True)  # New field for education
    comments = models.TextField(null=True, blank=True)  # New field for comments
    current_company = models.CharField(max_length=256, null=True, blank=True)  # New field for current company
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Populate job and candidate_name from related models
        if not self.job:
            self.job = self.jd.title
        if not self.candidate_name:
            self.candidate_name = self.candidate.hq_user.name

        # Update related models with data from JobApplication
        candidate = self.candidate
        hq_user = candidate.hq_user

        if not hq_user.email:
            hq_user.email = self.email
        if not hq_user.mobile:
            hq_user.mobile = self.phone_number
        if not candidate.resume:
            candidate.resume = self.resume

        hq_user.save()
        candidate.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.candidate.hq_user.name} - {self.jd.title}"

    class Meta:
        db_table = "core_job_application"









