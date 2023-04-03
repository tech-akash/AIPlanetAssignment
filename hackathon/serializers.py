from rest_framework import serializers

from .models import *

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hackathon
        fields='__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Submission
        fields='__all__'
