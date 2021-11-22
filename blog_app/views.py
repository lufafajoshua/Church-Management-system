from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Blog, Author, Entry, Comments
import datetime
from .forms import CommentForm, SearchForm, BlogForm, UpdateBlogForm, UpdateForm, EntryForm, RateForm, ArchiveForm
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.views.generic.dates import YearArchiveView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.dates import DayArchiveView
from user_profiles.models import Profile
from django.db.models import Q

def blogs(request):#This is for the display in the blog home page
    blogs = Blog.objects.all()
    now = datetime.datetime.now()
    today = now.date()
    day = today.day
    latest = Blog.objects.filter(pub_date__day=day)
    context = {
        'blogs': blogs,
        'latest': latest,
    }
    return render(request, 'blog_app/blogs.html', context)

def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    entries = blog.entry_set.all()
    context = {
        'blog': blog,
        'entries': entries,
    }
    return render(request, 'blog_app/blog_detail.html', context)

def entries(request):#This will retrieve all the entries associated with a blog
    entries = Entry.objects.all()#filter those with a high number of comments and ratings and display them on an entry page
    ordered_entries = Entry.objects.annotate(num_rating=Count('rating')).order_by('-rating')#Display beginning with the highest rating to the lowest ranking entry
    context = {
        'entries': entries,#This will return all the entries that have been created
        'ordered_entries': ordered_entries,#Or you can call this rating
    }
    return render(request, 'blog_app/entries.html', context)

def entry_detail(request, entry_id):#Retrieve a specific entry by id from the database
    entry = get_object_or_404(Entry, pk=entry_id)
    q = Entry.objects.annotate(no_comments = Count('comments'))
    no_of_comments = q[entry_id-1].no_comments
    """This displays the number of comments, its defined in the query above, 
    subtract 1 because the indexing of the entry is greater than the index 
    used to get the no_of_comments
    """
        # rating = q[entry_id-1].c_rating#This displays the rating of the entry
        # print(rating)
    comments = entry.comments_set.all()
    context = {
        'entry': entry,#Display an entry object 
        'comments': no_of_comments,#This displays the number of comments per entry
        #'rating': rating,#This displays the rating of the entry
        'comment': comments,#All the comments on an entry
    }  
    return render(request, 'blog_app/entry_detail.html', context)  

class BlogYearArchiveView(YearArchiveView): 
    queryset = Blog.objects.all() 
    date_field = "pub_date" 
    make_object_list = True 
    allow_future = True


class BlogMonthArchiveView(MonthArchiveView): 
    queryset = Blog.objects.all() 
    date_field = "pub_date" 
    make_object_list = True 
    allow_future = True

class BlogWeekArchiveView(WeekArchiveView): 
    queryset = Blog.objects.all() 
    date_field = "pub_date" 
    make_object_list = True 
    allow_future = True

class BlogDayArchiveView(DayArchiveView): 
    queryset = Blog.objects.all() 
    date_field = "pub_date" 
    make_object_list = True 
    allow_future = True

def delete_blog(request, blog_id):
    blog = Blog.objects.get_object_or_404(pk=blog_id)#Cosider usingbthe get_object_or_404
    if blog:
        blog.entry_set.all().delete()#The clear method is use to delete all relationships for a foreign key, Use remove() for many-to-many relationships, you can also use this to delete and create new relationships
        blog.delete()#This  will delete a blog with all its entries
        #Remove all possible relations related to the blog
        return HttpResponse("successfully Deleted Blog")
    else:
        return HttpResponse("Error deleting Blog")#Format and pass the blog name in the error message

def delete_entry(request, entry_id):#Delete the entries belonging to a blog
    entry = Entry.objects.get_object_or_404(pk=entry_id)
    if entry:
        entry.delete()
        return HttpResponse("Successfully deleted the entry")
    else:
        return HttpResponse("Failed to delete the Entry")    

def update(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    #Pass the retrieved entry object to the form object to be displayed
    if request.method == 'POST':
        form = UpdateForm(request.POST or None, instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog_app:entries', args=(entry.id,)))#pass the view with the entries

    context = {
        'form': form,
    }
    return render(request, 'blog_app/update.html', context)

def update_blog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    #Pass the retrieved entry object to the form object to be displayed
    form = UpdateBlogForm(request.POST or None, instance=blog)#page 260 in the documentation
    if form.is_valid():
        form.save()
        return redirect(reverse('blog_app:blogs'))

    context = {
        'form': form,
        'blog': blog,
    }
    return render(request, 'blog_app/update_blog.html', context)

def comment(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    profile = get_object_or_404(Profile, user=request.user)#Get the profile os the user commenting
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comments.objects.create(
                comment = form.cleaned_data['comment'],
                profile = profile,#You can only comment if you have a profile
                entry=entry
            )
            comment.save()
            entry.n_comments += 1
            entry.save()
            return HttpResponse("Successfuly Commented")
    else:
        form = CommentForm() 
    context = {
        'form': form,
        'entry': entry,
    } 
    return render(request, 'blog_app/comment.html', context)          

def add_author(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    if request.method == 'POST':
        form =AuthorForm(request.POST)
        if form.is_valid():
            author = Author.objects.create(
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email']
            )
            author.save()
            entry.authors.add(author)
            entry.save()
            return HttpResponse("Successfuly Added Author")
    else:
        form = AuthorForm() 
    context = {
        'form': form,
        'entry': entry,
    } 
    return render(request, 'blog_app/add_author.html', context)          

def create_blog(request):
    #entry = get_object_or_404(Entry, pk=entry_id)#Use this in case thier is need to add it to the 
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = Blog.objects.create(
                name = form.cleaned_data['name'],
                tagline = form.cleaned_data['tagline']
            )
            blog.save()
            return redirect(reverse('blog_app:blogs'))#Redirect to all the created blog objects in the database
    else:
        form = BlogForm() 
    context = {
        'form': form,
    } 
    return render(request, 'blog_app/create_blog.html', context)    

def create_entry(request, blog_id):#Dont forget to pass the blog id and use the entry_set.set(obj) to add the blog
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.blog = blog
            entry.save()
                # blog.entry_set.set([entry])#Set the created entry to the blog object
                # blog.save()
            return HttpResponse("Successfuly Created Entry")
    else:
        form=EntryForm()
    context = {
        'form': form,
        'blog': blog,
    }
    return render(request, 'blog_app/create_entry.html', context)    

def rate(request, entry_id):#Rate the entry with other entries in the same blog. Rate by blog
    """Supply a form with values from which a user can select to rate the entry object
    for example having form with values 1,2...n where the value selected is added to the database values of rating
    """
    entry = get_object_or_404(Entry, pk=entry_id)
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            entry.rating =+ request.POST['select']
            entry.save()
            return redirect(reverse('blog_app:entry', args=(entry.id,))) 
        # if entry:
        #     entry.rating =+ 1#Plan to use choices set in the frontend with the form and add them
        #     entry.save()
    else:
        form = RateForm()
    context = {
        'form': form,
        'entry': entry,
    } 
    return render(request, 'blog_app/rate.html', context)       

def search(request):
    form = SearchForm()
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(name__icontains=query) | Q(tagline__icontains=query)
            results= Blog.objects.filter(lookups).distinct()
            context = {
                'results': results,
                'submitbutton': submitbutton,
            }
            return render(request, 'blog_app/search.html', context)
        else:
            return render(request, 'blog_app/search.html')  
    else:
        return render(request, 'blog_app/search.html')

#Write the view to search for entries in a blog             



        

        