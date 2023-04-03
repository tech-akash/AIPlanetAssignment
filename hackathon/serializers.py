from rest_framework import serializers

from .models import *

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hackathon
        fields='__all__'
    
    def create(self, validated_data):
        instance = Submission(**validated_data)
        instance.full_clean()
        instance.save()
        return instance


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Submission
        fields='__all__'
    
    def create(self, validated_data):
        instance = Submission(**validated_data)
        instance.full_clean()
        instance.save()
        return instance
