from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
class GoogleLogin(SocialLoginView):
    authentication_classes = [] # disable authentication
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/login"
    client_class = OAuth2Client


@api_view(['GET'])
def AllHackathons(request,*args, **kwargs):
    Hackobj=Hackathon.objects.all()
    serializer=HackathonSerializer(Hackobj,many=True)
    return Response({'status':200,'payload':serializer.data})


@api_view(['GET'])
def RegisterHackathon(request,pk,*args, **kwargs):
    try:
        Hackobj=Hackathon.objects.get(id=pk)
        Enroll.objects.create(hackathon=Hackobj,user=request.user)
        return Response({'status':'Done'})
    except:
        return Response({'status':'error'})
    

@api_view(['POST'])
def CreateHackthon(request,*args, **kwargs):
    serializer=HackathonSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(postedBy=request.user)
        except:
            return Response({'status':400,'error':'User is not Recruiter'})
    else:
        return Response({'status':400,'error':serializer.error_messages})
    
    return Response({'status':200,'payload':'done'})



# @csrf_protect(False)
# @csrf_exempt
@api_view(['POST'])
def MakeSubmission(request,pk,*args, **kwargs):
    # csrf_secret = request.COOKIES.get(settings.CSRF_COOKIE_NAME)
    HackObj=Hackathon.objects.get(id=pk)
    serializer=SubmissionSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(user=request.user,hackathon=HackObj)
        except:
            return Response({'status':400,'error':serializer.error_messages})
    else:
        return Response({'status':400,'error':serializer.error_messages})
    
    return Response({'status':200,'payload':'done'})
        

@api_view(['GET'])
def GetEnrolledHackathon(request,*args, **kwargs):
    enrollments=Enroll.objects.filter(user=request.user)
    hackathons = [enrollment.hackathon for enrollment in enrollments]
    serializer=HackathonSerializer(hackathons,many=True)
    return Response({'status':200,'payload':serializer.data})


@api_view(['GET'])
def GetSubmission(request,pk,*args, **kwargs):
    HackObj=Hackathon.objects.get(id=pk)
    obj=Submission.objects.get(hackathon=HackObj)
    serializers=SubmissionSerializer(obj,many=False)
    return Response({'status':200,'payload':serializers.data})









