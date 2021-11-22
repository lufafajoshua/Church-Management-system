from django.shortcuts import render, redirect, get_object_or_404
from .models import Church, StudyGroup, Project, Program, Contact, ContactMessage, Announcement, News, Event, Transaction
from user_profiles.models import Profile
from django.urls import reverse
from .forms import GroupForm, AccountForm, ContactForm, ChurchForm, ProgramForm, ProjectForm, PaymentForm, ContactMessageForm
from django.http import HttpResponse
import datetime
#import http.client, urllib.request, urllib.parse, urllib.error, base64, json, uuid

import http.client, urllib.request, urllib.parse, urllib.error, base64, json, uuid
from base64 import b64encode
from django.contrib.auth.decorators import login_required

def create_account(request):#Thisis the admin method to create an account 
    if request.method == 'POST':
        form = ChurchForm(request.POST)
        if form.is_valid():
            account = Church.objects.create(
                name = form.cleaned_data['name'],
                slug = form.cleaned_data['slug'],
                location = form.cleaned_data['location']
            )
            account.save() 
            return HttpResponse("Successfuly created account")
    else:
        form = ChurchForm() 
        #Can optionally pass a context object 
    context = {
        'form': form
    }     
    return render(request, 'account/createaccount.html', context)

#This will be changed to using a one to one field with the church object
def create_contact(request, church_id):
    church = get_object_or_404(Church, pk=church_id)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = Contact.objects.create(
                church = church,
                address = form.cleaned_data['address'],
                head_elder = form.cleaned_data['head_elder'],
                ch_pastor = form.cleaned_data['ch_pastor'],
                ch_clerk = form.cleaned_data['ch_clerk'],
                email = form.cleaned_data['email'],
            ) 
            contact.save()
            return HttpResponse("Successfully created contact")
        
def create_program(request, church_id):
    church = get_object_or_404(Church, pk=church_id)
    if request.method == 'POST': 
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = Program.objects.create(
                church = church,
                name=form.cleaned_data['name'],
                head=form.cleaned_data['head'],
                timeframe=form.cleaned_data['timeframe']
                )
            program.save() 
            return HttpResponse("successfully Added program")
    else:
        form = ProgramForm()  

    context = {
        'form': form,
        'church': church
    }         
    return render(request, 'account/createprogram.html', context) 

def create_project(request, church_id):
    church = get_object_or_404(Church, pk=church_id)
    if request.method == 'POST': 
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(
                church = church,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                timeframe=form.cleaned_data['timeframe'],
                Fundraiser=form.cleaned_data['fundraiser']
 
                )
            project.save() 
            return HttpResponse("successfully Added project")
    else:
        form = ProjectForm()  

    context = {
        'form': form,
        'church': church
    }         
    return render(request, 'account/createproject.html', context) 

def study_group(request, id):
    participants = get_object_or_404(Profile, user=request.user)
    study_group = get_object_or_404(StudyGroup, id=id)
    context = {
        'group': study_group
    }
    return render(request, 'account/study-group.html', context)
    
def create_group(request, church_id):
    #account to create the group
    church = get_object_or_404(Church, pk=church_id)#Get the church object creating the group buy its id and the automatically add the created group to its groups
    if request.method == 'POST': 
        form = GroupForm(request.POST)
        if form.is_valid():
            group = StudyGroup.objects.create(
                church = church,
                name=form.cleaned_data['name'],
                topic=form.cleaned_data['topic']
                )
            group.save() 
            return HttpResponse("successfully created group")
    else:
        form = GroupForm()  

    context = {
        'form': form,
        'church': church
    }         
    return render(request, 'account/creategroup.html', context) 

def join_group(request, group_id):
    participant = get_object_or_404(Profile, user=request.user)
    group = StudyGroup.objects.filter(pk=group_id)
    #group = StudyGroup.objects.get_or_create(pk=group_id)
    if group.exists():   
        group[0].participants.add(participant)#Result from the filter statement
        group[0].save()
    return redirect(reverse('churchaccounts:list'))

def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project':project
    }
    return render(request, 'account/project.html', context)

def church_account(request, church_id, **kwargs):#Display the church account object/separate these into two 
    church_account = get_object_or_404(Church, pk=church_id)#this displays a specific church account
    #church_list = Church.objects.all()# this displays all the created church objects
    contact = church_account.contact_set.all()#Get the Contact objects associated with a church account
    programs = church_account.program_set.all()
    group = church_account.studygroup_set.all()
    project = church_account.project_set.all()
    context = {
        'church': church_account, 
        'contact': contact,
        'group': group,
        'project': project,
        'program': programs, 
    }
    return render(request, 'account/church_account.html', context)#create a folder named church in the templates folder to hold the church_account.html

def church_list(request):#Use this to display all the general information
   
    church_list = Church.objects.all()# this displays all the created church objects
    context = {   
        'church_list': church_list,
        
    }
    return render(request, 'account/church_list.html', context)

def support(request, project_id):#Let this be accessed by a project through an id 
    #church_account = get_object_or_404(Church, pk=church_id)#Plan on how to get the church object being supported 
    project = get_object_or_404(Project, pk=project_id)#This is the project that a user intends to support from
    if request.method == 'POST': 
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']#Get the amount from the user directly
            #provide code for various methods of payment with the choices set in the forntend

            current_amount = project.amount#Get the currently stored amout which is 0 by default
            new_amount = amount + current_amount#Add the amount set by the user in the form to the current amount
            current_amount = new_amount#Set the current amount to the new total
            #Retutn to the transaction page showing the details of the transaction

    else:
        form = PaymentForm()

    context = {
        'form': form,
        'project': project,

    }
    return render(request, 'account/payment.html', context)


def get_auth_token(): 
    api_user = 'de2aea87-fdd1-432a-8d21-7e488fb1ee49'
    api_key = '002c242c2aa047b7926c3d86dbf1b9a5' 
    api_user_and_key  = api_user+':'+api_key
    api_user_and_key_bytes = base64.b64encode(api_user_and_key.encode()).decode()

    headers = {
        # Request headers
        'Authorization': "Basic "+api_user_and_key_bytes,
        #'Authorization': 'Basic' +api_user_and_key_bytes,
        
            # 'X-Callback-Url': '',
            # 'X-Reference-Id': '6cb5711b-5d29-4053-aaa1-516ec394f044',
        #'X-Target-Environment': 'oauth2',
        #'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'bda4d094a1d840d4a709a4a4359b9b02',
    }
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')#replace with ericssonbasicapi2.azure-api.net when having a new connection
        conn.request("POST", "/collection/token/?%s" % params, "{body}", headers)
        response = conn.getresponse()
        print(response.status)
        print(response.reason)
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}]".format(e))  

#@login_required()
def make_payment(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    #total_amount = existing_order.get_cart_total()    
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSMjU2In0.eyJjbGllbnRJZCI6ImRlMmFlYTg3LWZkZDEtNDMyYS04ZDIxLTdlNDg4ZmIxZWU0OSIsImV4cGlyZXMiOiIyMDIwLTEyLTA2VDEyOjE5OjMzLjMyMiIsInNlc3Npb25JZCI6IjdjOTMxZDQwLTIwNGMtNDBhOC04MTc3LTBiNWQzOWIxZTFjZiJ9.gFcaix1mKcmXsGv-pj4Q84SePqBVetvBWWRhFVt89KvdCRsFyBePsewCXwy4BziEmcVIUJXQHINfgmUMOCQUUXRaQwFzhPSqMjjHH8vVE6__7AIinJ0zCuF3tEMLjwh6MAYB9pJKciNFbg3KEXTuo1HFeLcT3okSr0CmHg1mrFYgp3zTUfG-_Wk4Ij4877YCr1TVa8Uze11JKEgsdO2o1w1CXf8vqAU86-_oJQgCwRxGNMD-kv9rNYnrmnytHOx2agUMz738mc29Qxi0NT3346q7h7g46E47rd8K7LtLiL8xFvD2SD3LzHun56uCO0-xe4RUQzawzQpgnsLyM9NVNA"
    #token = get_auth_token()#Try using the function with internet to check whether its working
    reference_id = str(uuid.uuid4())

    form = PaymentForm(request.POST)
   
    if form.is_valid():
        phone = form.cleaned_data['phone_no']
        amount = form.cleaned_data['amount']
        headers = {
            # Request headers
            'Authorization': 'Bearer '+token,
            #'X-Callback-Url': 'https://winnershield.com',#Point to the transaction urls so to create the transaction information
            'X-Reference-Id': reference_id,
            'X-Target-Environment': 'sandbox',
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': 'bda4d094a1d840d4a709a4a4359b9b02',
        }

        params = urllib.parse.urlencode({
        })

        body = json.dumps({
        "amount": str(amount),#Turn this to string in case of errors
        "currency": "EUR",
        "externalId": "12345",
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": phone,#Get this from the frontend
        },
        "payerMessage": "Successfully Paid",
        "payeeNote": "Hello Successfull"
        })

        try:
            conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
            conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            print(response.status)
            conn.close()

            if response.status == 202:#Check for what returns a successful payment
                #return redirect(reverse('shopping_cart:payment_done', args=(existing_order.id,)))#Try using the token and see the results
                return redirect(reverse('churchaccounts:update_transaction', args=(project.id,)))#args=(existing_order.id,) 
        except Exception as e:
            print("[Errno {0}]".format(e))
        finally:
            print("Transaction in Progress")    
    context = {
        'project': project,
        'form': form,
        
    }    
    return render(request, 'account/mtnmomo.html', context)    

def delete_account(request, church_id):#leave this to the admin only and not to the users
    church = Church.objects.filter(pk=church_id)#select the church object by id and delete if exists
    if church.exists():
        church[0].delete()
        #return message displaying successfully deleted the church object redirect to the home page
    return redirect(reverse('create_account'))  #redirect to the create church account page once an account has been deleyed by the user   

def support_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)#This is the project being supported, though if not needed in the chekout remove it from the process
    profile = get_object_or_404(Profile, user=request.user)#Get the user that is supporting this project 
    #Implement a payments API at this point or a checkout method
    #The amount is provided by the user in the form and also sent along with the call to update transaction records
    if request.method == 'POST': 
        form = PaymentForm(request.POST)
        if form.is_valid():#As you are implementing the Checkout process providing the amount
            amount = form.cleaned_data['amount']
    context = {
        'project': project,
    }
    return render(request, 'account/support.html')

def update_transaction(request, project_id, amount):
    project = get_object_or_404(Project, pk=project_id)#This is the project being supported
    profile = get_object_or_404(Profile, user=request.user)

    transaction = Transaction(profile=request.user.profile,
                        project_id=project.id,
                        amount=amount,#GEt the amount from the frontend
                        success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()
    return redirect(reverse('churchaccounts:list'))

def create_contact_message(request):#Create the contact form and submit the data to the backend for processing
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact = ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            contact.save()
            return redirect('churchaccounts:list')#Redirect back to the account and not the list
    else:
        form = ContactMessageForm() 
    context = {
        'form': form,
        #'contact': contact,#You may not want to display a contact message
    }           
    return render(request, 'account/contactmessage.html', context)

def announcements(request):
    all_announcements = Announcement.objects.all()
    context = {
        'announcements': all_announcements,
    }
    return render(request, 'account/announcements.html', context)

def announcement_detail(request, id):
    announcement = get_object_or_404(Announcement, pk=id)
    context = {
        'announcement': announcement,
    }
    return render(request, 'account/announcement_detail.html', context)

def news(request):
    all_news = News.objects.all()
    #Get the latest newly created news
    now = datetime.datetime.now()
    today = now.date()
    day = today.day
    latest = News.objects.filter(pub_date__day=day)
    context = {
        'news': all_news,
        'latest': latest
    }
    return render(request, 'account/news.html', context)

def news_detail(request, id):
    news = get_object_or_404(News, pk=id)
    context = {
        'news': news,
    }
    return render(request, 'account/news_detail.html', context)

def events(request):
    all_events = Event.objects.all()
    #Get the latest newly created news
    now = datetime.datetime.now()
    today = now.date()
    day = today.day
    latest = Event.objects.filter(pub_date__day=day)#Get those that have just been added or created
    context = {
        'events': all_events,
        'latest': latest
    }
    return render(request, 'account/events.html', context)

def event_detail(request, id):
    event = get_object_or_404(Event, pk=id)
    context = {
        'event': event,
    }
    return render(request, 'account/event_detail.html', context)


