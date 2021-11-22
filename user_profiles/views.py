from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.http import HttpResponseRedirect 
from django.contrib.auth.forms import UserCreationForm
from churchaccounts.models import StudyGroup, Church


def index(request):
    return render(request, 'user_profiles/index.html')


def my_profile(request):#if a user is an adventist, then they can be associated with a church account 
    my_user_profile = Profile.objects.filter(user=request.user).first()
    church_account = Church.objects.filter(member=my_user_profile, sda=True)#associate the user_order object with the user profile. 
    groups = StudyGroup.objects.filter(participant=my_user_profile)
    # #Add the logic for the user to join a specific group
    context = {
        'my_profile': my_user_profile
    }
    return render(request, 'my_profile.html', context) 


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
            return redirect(reverse('churchaccounts:church_list'))

    else:
        form = UserCreationForm()
    return render(request, 'user_profiles/register.html', {'form': form})    

