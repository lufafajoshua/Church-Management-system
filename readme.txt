superuser details = username = josue
email = josh@gmail.com
password = churchonline

consult page 125 in django docs for more on annotations

paypal details 
Igangasda123 = password

P.O.Box 157 post office number

Mtn developer account details
email = lufafajosh@gmail.com
password = jerosha1998

https://github.com/aseem-hegshetye/Video_call_and_chat_in_Django

This is an application to help church organisations to implement and reach their congregations better via the web
It is built upon django-version == 2.2
This is not a complete project with much to handle in fully integrating the chat functionality \
and organising the various views to the pages where they belong for example creating a custom admin page to handle functionalities\
like adding data to church profiles, etc
TODOs 
A better frontend for easier manipulation by users.

from churchaccounts.models import StudyGroup
>>> a = StudyGroup.objects.get(id=1)
>>> a.name
'Sabbath  School'
>>> a.participants.all()
<QuerySet [<Profile: Profile object (2)>]>
s = Profile.objects.get(user_id=2)
s.studygroup_set.get()#set this to a variable which you will compare with the retrieved group object so that a user is only allowed to chat in a group if he belongs there
