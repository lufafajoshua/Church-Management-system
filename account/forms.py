    # from django import forms
    # from django.forms import ModelForm
    # from django.forms import ModelChoiceField, ModelMultipleChoiceField
    # from .models import Contact, Profile, StudyGroup, Program, Project, Church 

    # class GroupForm(forms.Form):
    #     name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     topic = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    # class AccountForm(forms.Form):
    #     contact_object = Contact.objects.all()
    #     member_object = Profile.objects.all()
    #     group_object = StudyGroup.objects.all()
    #     program_object = Program.objects.all()
    #     project_object = Project.objects.all()
    #     name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     slug = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     contact = forms.ModelChoiceField(queryset=contact_object, empty_label="(contact)")#You can use the "(Nothing)" to et the empty lable vale
    #     membership = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     #contact = forms.ModelChoiceField(queryset=..., empty_label="(contact)")#You can use the "(Nothing)" to et the empty lable vale
    #     available = forms.ChoiceField(widget=forms.CheckboxInput)
    #     district = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     field = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     member = forms.ModelMultipleChoiceField(queryset=member_object, required=False)
    #     group = forms.ModelMultipleChoiceField(queryset=group_object, required=False)
    #     program = forms.ModelMultipleChoiceField(queryset=program_object, required=False)
    #     project = forms.ModelMultipleChoiceField(queryset=project_object, required=False)

    # class ChurchForm(forms.Form):
    #     name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     slug = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))        

    # class ProgramForm(forms.Form):
    #     name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     head = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     timeframe = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        
    # class ProjectForm(forms.Form):
    #     name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     timeframe = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     fundraiser = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))    

    # class ContactForm(forms.Form):
    #     address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     head_elder = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     ch_pastor = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     ch_clerk = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


    # class PaymentForm(forms.Form): 
    #         # PAYMENT_METHODS = (
    #         #     ('mobile_money', 'mobile_money'),
    #         #     ('M-Pesa', 'M-Pesa'),
    #         #     ('paypal', 'paypal'),

    #         # )
    #     amount = forms.DecimalField(max_digits=100, decimal_places=2)
    #     phone_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'form-phone_no', 'name':'form-phone_no', 'placeholder':'Phone Number'}))
    #     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'id':'form-email', 'name':'form-email', 'placeholder':'Email'}))
    #     address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))#Provide some choices for the address to be entered

    #         # payment_method = forms.CharField(
    #         #     max_length=3,
    #         #     widget=forms.Select(choices=PAYMENT_METHODS),
    #         #     )


    #     # class PaymentsForm(forms.Form):
    #     #     phone_no = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'form-phone_no', 'name':'form-phone_no', 'placeholder':'Phone Number'}))
    #     #     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'id':'form-email', 'name':'form-email', 'placeholder':'Email'}))
    #     #     address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))#Provide some choices for the address to be entered

    # class ContactMessageForm(forms.Form):
    #     name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'form-name', 'name':'form-name', 'placeholder':'Name..'}))
    #     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'id':'form-email', 'name':'form-email', 'placeholder':'Email..' }))
    #     subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'form-phone', 'name':'form-phone', 'placeholder':'Subject..'}))
    #     message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':'6', 'id':'form-message', 'name':'form-message', 'placeholder':'Your Message Here...'})) 

