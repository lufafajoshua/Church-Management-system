    # from django.db import models
    # from user_profiles.models import Profile

    # class Church(models.Model):
    #     name = models.CharField(max_length=200, db_index=True)
    #     slug = models.SlugField(max_length=150, db_index=True)
    #     location = models.CharField(max_length=200, db_index=True)
    #     #image = models.ImageField(upload_to='church')#Dont forget to add the church image later after installing pillow
    #     class Meta:
    #         verbose_name = "church"
    #         verbose_name_plural = "churches"
    #         indexes = [
    #             models.Index(fields=['id', 'slug'])
    #         ]

    #     def __str__(self):
    #         return self.name

    # class StudyGroup(models.Model):  
    #     church = models.ForeignKey(Church, on_delete=models.CASCADE)#One church has many study groups   
    #     name = models.CharField(max_length=150)
    #     topic = models.CharField(max_length=200)
    #     #slug = models.SlugField(max_length=150, db_index=True, unique=True)
    #     participants = models.ManyToManyField(Profile, blank=True)

    #         # class Meta:
    #         #     indexes = [
    #         #         models.Index(fields=['id', 'slug'])
    #         #     ]
    #     def __str__(self):
    #         return self.name

    # class Project(models.Model):     
    #     church = models.ForeignKey(Church, on_delete=models.CASCADE)#One church has many study groups
    #     name = models.CharField(max_length=250)  
    #     description = models.TextField(max_length=1000)#description of the project
    #     timeframe = models.CharField(max_length=150)#Time expected forr the completetion of the project
    #     Fundraiser = models.TextField(max_length=500)
    #     amount = models.DecimalField(max_digits=65, decimal_places=2, default=0)#Money collected online to support a project

    #     def __str__(self):
    #         return self.name

    # class Program(models.Model): 
    #     church = models.ForeignKey(Church, on_delete=models.CASCADE)#One church has many study groups   
    #     name = models.CharField(max_length=150)#Name of the program belonging to a particular church
    #     head = models.CharField(max_length=150)#Name of the one spearheading the program
    #     timeframe = models.CharField(max_length=200, db_index=True)#Hwhen is the program expecte to start or when its is to end, specify start-date and end-date

    #     def __str__(self):
    #         return self.name

    # class Contact(models.Model):
    #     church = models.ForeignKey(Church, on_delete=models.CASCADE)#One church has many study groups
    #     address = models.CharField(max_length=250)
    #     head_elder = models.CharField(max_length=200)#telephone contact for the church
    #     ch_pastor = models.CharField(max_length=200)#telephone contact for the church or resident pastor
    #     ch_clerk = models.CharField(max_length=200)#contact for the church clerk
    #     email = models.EmailField()
        
    #     def __str__(self):
    #         return self.address

    # class Transaction(models.Model):
    #     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #     # token = models.CharField(max_length=120)
    #     project_id = models.CharField(max_length=120)#Consider using the project object and not its id
    #     amount = models.DecimalField(max_digits=65, decimal_places=2)
    #     success = models.BooleanField(default=True)
    #     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    #     def __str__(self):
    #         return self.project_id

    #     class Meta:
    #         ordering = ['-timestamp'] 

    # class ContactMessage(models.Model):
    #     #church = models.ForeignKey(Church, on_delete=models.CASCADE)#One church has many contact messages
    #     name = models.CharField(max_length=200)
    #     email = models.EmailField()
    #     subject = models.CharField(max_length=200)
    #     message = models.TextField()
    #     class Meta:
    #         verbose_name = "contactMessage"
    #         verbose_name_plural = "contactmessages"

    #     def __str__(self):
    #         return self.name

    # class Event(models.Model):
    #     name = models.CharField(max_length=200)
    #     description = models.CharField(max_length=200)
    #     detail = models.TextField(max_length=1000)#description of the event
    #     image = models.ImageField(upload_to='church')#
    #     #event_date = models.DateTimeField()#The date that the event is to take place
    #     pub_date = models.DateTimeField(auto_now_add=True)#The date and time the event is to take place

    #     def __str__(self):
    #         return self.name

    # class News(models.Model):
    #     headline = models.CharField(max_length=200)
    #     body_text = models.TextField(max_length=1000)
    #     image = models.ImageField(upload_to='church')
    #     pub_date = models.DateTimeField(auto_now_add=True)
    #     author = models.CharField(max_length=200)

    #     class Meta:
    #         verbose_name = "News"
    #         verbose_name_plural = "News"

    #     def __str__(self):
    #         return self.headline

    # class Announcement(models.Model):
    #     title = models.CharField(max_length=200)
    #     description = models.TextField(max_length=1000)
    #     pub_date = models.DateTimeField(auto_now_add=True)

    #     def __str__(self):
    #         return self.title


