from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import logout, get_user_model
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from churchaccounts.models import StudyGroup
from user_profiles.models import Profile


from .models import Room, Message
from .utils import create_room
import random
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def import_base_template():
	try:
		return settings.CHATTER_BASE_TEMPLATE
	except AttributeError as e:
		try:
			if settings.CHATTER_DEBUG == True:
				logger.info("django_chatter.views: "
				"(Optional) settings.CHATTER_BASE_TEMPLATE not found. You can "
				"set it to point to your base template in your settings file.")
		except AttributeError as e:
			logger.info("django_chatter.views: "
			"(Optional) settings.CHATTER_BASE_TEMPLATE not found. You can "
			"set it to point to your base template in your settings file.")
			logger.info("django_chatter.views: to turn off this message, set "
			"your settings.CHATTER_DEBUG to False.")
		return 'django_chatter/base.html'


class IndexView(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		rooms_list = Room.objects.filter(members=request.user).order_by('-date_modified')
		if rooms_list.exists():
			latest_room_uuid = rooms_list[0].id
			return HttpResponseRedirect(
				reverse('django_chatter:chatroom', args=[latest_room_uuid])
			)
		else:
			# create room with the user themselves
			user = get_user_model().objects.get(username=request.user)
			room_id = create_room([user])
			return HttpResponseRedirect(
				reverse('django_chatter:chatroom', args=[room_id])
			)


# This fetches a chatroom given the room ID if a user diretly wants to access the chat.
class ChatRoomView(LoginRequiredMixin, TemplateView):
	template_name = 'django_chatter/chat-window.html'

	# This gets executed whenever a room exists
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		uuid = kwargs.get('uuid')
		try:
			room = Room.objects.get(id=uuid)
			user=get_user_model().objects.get(username=self.request.user)
		except Exception as e:
			logger.exception("\n\nException in django_chatter.views.ChatRoomView:\n")
			raise Http404("Sorry! What you're looking for isn't here.")
		all_members = room.members.all()
		if user in all_members:
			latest_messages_curr_room = room.message_set.all()[:50]
			if latest_messages_curr_room.exists():
				message = latest_messages_curr_room[0]
				message.recipients.add(user)
			if all_members.count() == 1:
				room_name = "Notes to Yourself"
			elif all_members.count() == 2:
				room_name = all_members.exclude(pk=user.pk)[0]
			else:
				room_name = room.__str__()
			context['room_uuid_json'] = kwargs.get('uuid')
			context['latest_messages_curr_room'] = latest_messages_curr_room
			context['room_name'] = room_name
			context['base_template'] = import_base_template()

			# Add rooms with unread messages
			rooms_list = Room.objects.filter(members=self.request.user)\
				.order_by('-date_modified')[:10]
			rooms_with_unread = []
			# Go through each list of rooms and check if the last message was unread
			# and add each last message to the context
			for room in rooms_list:
				try:
					message = room.message_set.all().order_by('-id')[0]
				except IndexError as e:
					continue
				if self.request.user not in message.recipients.all():
					rooms_with_unread.append(room.id)
			context['rooms_list'] = rooms_list
			context['rooms_with_unread'] = rooms_with_unread

			return context
		else:
			raise Http404("Sorry! What you're looking for isn't here.")


#The following functions deal with AJAX requests
@login_required
def users_list(request):
	if (request.is_ajax()):
		data_array = []
		for user in get_user_model().objects.all():
			data_dict = {}
			data_dict['id'] = user.pk
			data_dict['text'] = user.username
			data_array.append(data_dict)
		return JsonResponse(data_array, safe=False)

@login_required
def get_chat_url(request):
	user = get_user_model().objects.get(username=request.user)
	#target_user = get_user_model().objects.get(pk=request.POST.get('target_user'))
	#target_user = get_user_model().objects.get(username="joan")
	agents = get_user_model().objects.filter(user_type=3)
	"""USe the onetoone manager to handle the reverse relationship between the user objects and the Agent object"""
	available_agents = []
	for agent in agents:
		print(agent)
		print(agent.useragent.availability)

		if agent.useragent.availability == True:
			available_agents.append(agent)
				
	#print(available_agents)	
	target_user =  	random.choice(available_agents) #get any random element from the list of available users			
	if (user == target_user):
		room_id = create_room([user]) 
	else:
		room_id = create_room([user, target_user])
		#Once a target user is active in a chatroom, set the availabilty option of the target_user to False			
	return HttpResponseRedirect(reverse('django_chatter:chatroom', args=[room_id],))
	'''
	AI-------------------------------------------------------------------
		Use the util room creation function to create room for one/two
		user(s). This can be extended in the future to add multiple users
		in a group chat.
	-------------------------------------------------------------------AI
	'''
"""
This enables users in a given group to chat, implementing a chat between multiple users"""
@login_required
def group_chat(request, group_id):#Get the seller object from the related product object
	user = get_user_model().objects.get(username=request.user)
	group = StudyGroup.objects.get(pk=group_id)#Filter the products with the given product id
	#Get all Users available in a group
	print(group.participants.all())
	participants = group.participants.all()
	#Get the group to which the user trying to connect belong
	a = Profile.objects.get(user=user)
	user_group = a.studygroup_set.get()

	p = Profile.objects.filter(studygroup=group)
	#print(p)
	
	
	#Test if the user trying to connect to the chat actually is aparticipant in that group before creating the chat
	
	for x in participants:
		print(x.user)	
		
		target_user =x.user
		
		
		# for a in participants:
		# 	if user != a.user:
		# 		print("Not allowed to participate if you have not joined yet")
		# 		return HttpResponseRedirect(reverse('churchaccounts:study-group', args=[group.id],))
	#Check if the user trying to connect to this group belongs there if not redirrect to the group page so he may join to chat
	if user_group != group:
		return HttpResponseRedirect(reverse('churchaccounts:study-group', args=[group.id],))

	elif (user == target_user):
		room_id = create_room([user]) 
	
	else:
		room_id = create_room([user, target_user])
	return HttpResponseRedirect(reverse('django_chatter:chatroom', args=[room_id],))
		#else:
			#return HttpResponseRedirect(reverse('churchaccounts:study-group', args=[group.id],))		
		# for x in participants:
		# 	print(x.user)		
		# 	target_user =x.user
		# 	#print(target_user)
		# print(target_user)	
		# #Check if a user belongs to the specified group before creating the chat
		
		# if user in participants:
		# 	if (user == target_user):
		# 		room_id = create_room([user]) 
				
		# 	else:
		# 		room_id = create_room([user, target_user])
		# 	return HttpResponseRedirect(reverse('django_chatter:chatroom', args=[room_id],))
		# 	print("Yes")
		# else:
		# 	#Return the user to the group page so he can join the group
		# 	print("Nay")		 		
		# 	return HttpResponseRedirect(reverse('churchaccounts:study-group', args=[group.id],))


# Ajax request to fetch earlier messages
@login_required
def get_messages(request, uuid):
	if request.is_ajax():
		room = Room.objects.get(id=uuid)
		if request.user in room.members.all():
			messages = room.message_set.all()
			page = request.GET.get('page')

			paginator = Paginator(messages, 20)
			try:
				selected = paginator.page(page)
			except PageNotAnInteger:
				selected = paginator.page(1)
			except EmptyPage:
				selected = []
			messages_array = []
			for message in selected:
				dict = {}
				dict['sender'] = message.sender.username
				dict['message'] = message.text
				dict['received_room_id'] = uuid
				dict['date_created'] = message.date_created.strftime("%d %b %Y %H:%M:%S %Z")
				messages_array.append(dict)

			return JsonResponse(messages_array, safe=False)

		else:
			return Http404("Sorry! We can't find what you're looking for.")
	else:
		return Http404("Sorry! We can't find what you're looking for.")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():#Verify whether the data entered is valid before saving it in the database
            new_user = form.save()#save the newly created user data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            return HttpResponseRedirect('/accounts/login/')#Provided or created for django to handle user creation and regestration
            user = authenticate(username='username', password='password')#authenticate the newly created user object 
            login(request, user)
            #return redirect(reverse('django_chatter:church_list'))

    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})    

