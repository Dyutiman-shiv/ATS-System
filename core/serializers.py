from rest_framework import serializers
from .models import JobApplication, Candidate, HQUser

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        extra_kwargs = {
            'stage': {'required': False},
            'status': {'required': False},
            'candidate': {'required': False},
        }

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class HQUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HQUser
        fields = '__all__'

