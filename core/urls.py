from django.urls import path, re_path

from . import views
from core.views import jobs_api
from core.views import jd_api

urlpatterns = [
    path('', views.home.index, name='index'),
    # About
    path('about/contact', views.about.contact, name='contact'),
    path('about/faqs', views.about.faqs, name='faqs'),
    path('about/privacy', views.about.privacy, name='privacy'),
    path('about/terms', views.about.terms, name='terms'),

    # User URLs
    path('user/login', views.user.user_login, name='login'),
    path('user/logout', views.user.user_logout, name='logout'),
    path('user/forgot_password', views.user.recover_password, name='forgot password'),
    path('user/change_password/<str:token>', views.user.change_password, name='change password'),
    path('user/change_password_profile', views.user.change_password_profile, name='change password_profile'),
    path('user/act_as/<str:pub_id>/<str:password>', views.user.act_as, name='act_as'),

    # Candidate URLs
    path('candidate/dashboard', views.candidate.dashboard, name='dashboard'),
    path('candidate/profile', views.candidate.profile, name='profile'),
    path('candidate/preferences', views.candidate.preferences, name='preferences'),
    

    # Profile URLs
    path('profile/view/<str:public_profile_name>', views.profile.view, name='profile_view'),
    path('p/<str:public_profile_name>', views.profile.view, name='profile_view'),

    # Jobs URL
    path('jobs/', views.jobs.job_list, name='job_list'),
    path('jobs/<str:pub_id>/apply/', views.jobs.apply, name='apply'),
    #path('jobs/<str:pub_id>/apply/?ref=<str:ref_code>', views.jobs.apply, name='apply'),
    path('jobs/<str:pub_id>/save', views.jobs.save_application, name='save_application'),
    path('jobs/<str:pub_id>', views.jobs.view_job, name='confirm_token'),
    path('<str:public_profile_name>', views.profile.view, name='profile_view'),

    path('api/job-applications/', jobs_api.JobApplicationListCreate.as_view(), name='job-application-list-create'),
    path('api/job-applications/<int:pk>/', jobs_api.JobApplicationDetail.as_view(), name='job-application-detail'),
    path('api/job_descriptions/', jd_api.job_descriptions_api, name='job_descriptions_api'),
    path('api/job_descriptions/<str:pub_id>/', jd_api.job_descriptions_api, name='job_description_detail_api'),
]