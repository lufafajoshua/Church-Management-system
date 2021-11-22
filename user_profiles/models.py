from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
#from blog_app.models import Comment

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sda = models.BooleanField(default=True)#If the user is an sda, then load the church account where he belongs or else they can use accounts for other churches 
    #comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    #Get all the comments a user has made via a reverse relationship ie comment_set

    def __str__(self):
        return self.user.username#first_name#return a more readable format of this profile object


def post_save_user_profile(sender, instance, created, **kwargs):
    user_profile, created = Profile.objects.get_or_create(user=instance) 
    user_profile.save()
post_save.connect(post_save_user_profile, sender=settings.AUTH_USER_MODEL) #the first argument defines the reciever function while the second defines the sender   

