from django.db import models
from user_profiles.models import Profile

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name 

class Blog(models.Model):#Plan to implement the dates when they were created#
    name = models.CharField(max_length=128)
    tagline = models.TextField()
    pub_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)#One blog has many entries
    CHOICES = []
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()#Specify autonow =True or false
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField(default=0)#count the number of comments by each comment made to a post
    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ["-pub_date"]#Display them by the descending order frol last created to 
        #get_latest_by = "pub_date"
        verbose_name = "Entry"
        verbose_name_plural = "Entries"

    def __str__(self):
        return self.headline

#A comment belongs to one profile and a profile has many comments
class Comments(models.Model):#Associate eact comment to an entry, acomment belongs to one and only one profile and a profile has many comments 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)#The profile of the user adding the somment to the entry
    comment =models.TextField()#This is the body of the comment
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)#AN entry has many comments, many comments belong to one entry

    class Meta:
    
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
   
    def __str__(self):
        return self.comment
