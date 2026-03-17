from rest_framework import generics, status
from rest_framework.response import Response
#from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from core.models import JobApplication, JobDescription, HQUser, Candidate
from core.serializers import JobApplicationSerializer

class JobApplicationListCreate(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer


    def create(self, request, *args, **kwargs):
        jd = get_object_or_404(JobDescription, pk=request.data.get('jd'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        hq_user, created = HQUser.objects.get_or_create(
            user=None,
            defaults={'name': validated_data.get('candidate_name'), 'email': validated_data.get('email')}
        )
        candidate, created = Candidate.objects.get_or_create(
            hq_user=hq_user,
            defaults={'resume': validated_data.get('resume')}
        )

        if not hq_user.email:
            hq_user.email = validated_data.get('email')
        if not hq_user.mobile:
            hq_user.mobile = validated_data.get('phone_number')
        hq_user.save()

        job_application = JobApplication(
            jd=jd,
            candidate=candidate,
            stage='APP',  # Default value
            status='APP',  # Default value
            candidate_name=validated_data.get('candidate_name'),
            resume=validated_data.get('resume'),
            expected_salary=validated_data.get('expected_salary'),
            current_salary=validated_data.get('current_salary'),
            current_location=validated_data.get('current_location'),
            notice_period=validated_data.get('notice_period'),
            willing_to_locate=validated_data.get('willing_to_relocate') == 'yes',
            phone_number=validated_data.get('phone_number'),
            email=validated_data.get('email')
        )
        job_application.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class JobApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
