from django import forms
from .models import Entry, Blog, Author, Comments 
from django.forms import ModelForm
from django.forms import ModelChoiceField, ModelMultipleChoiceField

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':'6', 'id':'form-comment', 'name':'form-comment', 'placeholder':'Comment Here...'})) 

class BlogForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'form-name', 'name':'form-name', 'placeholder':'Name..'}))    
    tagline = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':'6', 'id':'form-comment', 'name':'form-tagline', 'placeholder':'Tagline'})) 

class SearchForm(forms.Form):
    choices = (('Blog', 'Blog'), ('Entry', 'Entry'))
    select = forms.CharField(widget=forms.Select(choices=choices))
    search_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'form-name', 'name':'form-name', 'placeholder':'Search Here...'}))

class UpdateForm(forms.Form):#This will be used to update the Entry object selected
    class Meta:
        model = Entry
        fields = ['headline', 'body_text', 'pub_date', 'mod_date']
        #You can define the fields to exclude incase of errors


class UpdateBlogForm(ModelForm):#This will be used to update the Entry object selected
    class Meta:
        model = Blog
        fields = ['name', 'tagline']
        #You can define the fields to exclude incase of errors


class ArchiveForm(forms.Form):
    choices = (('year', 'year'), ('month', 'month'), ('day', 'day'))
    select = forms.CharField(widget=forms.Select(choices=choices))
    search_text = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
        # year = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
        # month = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
        # day = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
        

class RateForm(forms.Form):
    choices = ((0, 'never'), (5, 'somehow'), (10, 'helpfull'))#These values determine the rate with which the blog entry was helpfull
    select = forms.CharField(widget=forms.Select(choices=choices))

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['blog','headline', 'body_text', 'pub_date', 'mod_date']
        exclude = ['blog', 'authors']

        labels = {
            'headline': 'Headline',
            'body_text': 'Body_text',
            'pub_date': 'Publication Date',
            'mod_date': 'Modification Date',
        }

    author_object = Author.objects.all()
    authors = forms.ModelMultipleChoiceField(queryset=author_object, required=False)

    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            if initial == 'authors':
                initial['authors'] = [t.pk for t in kwargs['instance'].authors_set.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        # Get the unsaved Church instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the church with many-to-many fields
            lst = ['authors']#This ia alist for the set manytomanyfields
            for i in lst:
                if i == 'authors':
                    instance.authors.clear()
                    for authors in self.cleaned_data['authors']:
                        instance.authors.add(authors)              

        self.save_m2m = save_m2m
        if commit:
            instance.save()
            self.save_m2m()

        return instance