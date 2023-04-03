from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

Roles=(
    ('Student','Student'),
    ('Recruiter','Recruiter'),
)
Types=(
    ('file','file'),
    ('link','link'),
    ('image','image'),
)

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    role=models.CharField(choices=Roles,default='Student',max_length=15)

class Hackathon(models.Model):
    postedBy=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=255,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    bgImage=models.ImageField(upload_to="BgImage/",null=True,blank=True)
    hackathonImage=models.ImageField(upload_to="hackathonimage/",null=True,blank=True)
    submissionType=models.CharField(choices=Types,default='file',max_length=10)
    startTime=models.DateTimeField(null=True,blank=True)
    endTime=models.DateTimeField(null=True,blank=True)
    prize=models.IntegerField(null=True,blank=True)
    
    def clean(self):
        try:
            profile=Profile.objects.get(user=self.postedBy)
            if profile.role!='Recruiter':
                raise ValidationError("Only Recruiter can post a hackathon.")
        
        except:
            raise ValidationError("Only Recruiter can post a hackathon.")
        
        if self.startTime>self.endTime:
            raise ValidationError("End Time of hackathon should be after start time.")
        

class Enroll(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    hackathon=models.ForeignKey(Hackathon,on_delete=models.CASCADE)


class Submission(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    hackathon=models.ForeignKey(Hackathon,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    summary=models.TextField(null=True,blank=True)
    link=models.URLField(blank=True,null=True)
    image=models.ImageField(upload_to="ImageSubmission/",blank=True,null=True)
    file=models.FileField(upload_to="FileSubmission/",blank=True,null=True)

    def clean(self):
        num_submissions = sum(bool(field) for field in [self.link, self.file, self.image])
        if num_submissions != 1:
            raise ValidationError("Exactly one submission type must be provided.")
        hackathon_submission_type = self.hackathon.submissionType
        if (self.link and hackathon_submission_type!='link') or (self.file and hackathon_submission_type!='file') or (self.image and hackathon_submission_type!='image'):
            raise ValidationError(f"Only {hackathon_submission_type} submission is allowed in this  hackathons.")
        

