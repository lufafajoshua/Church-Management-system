from django.urls import path, include
from . import views
from blog_app.views import BlogWeekArchiveView, BlogMonthArchiveView, BlogYearArchiveView, BlogDayArchiveView

app_name = 'blog_app'
urlpatterns = [
    path('blogs', views.blogs, name='blogs'),
    path('blog/<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('entries', views.entries, name='entries'),
    path('entry_detail/<int:entry_id>', views.entry_detail, name='entry_detail'),
    path('<int:year>/<str:month>/<int:day>/', BlogDayArchiveView.as_view(), name="archive_day"),
    path('<int:year>/<int:month>/', BlogMonthArchiveView.as_view(month_format='%m'), name="archive_month"), 
    path('<int:year>/', BlogYearArchiveView.as_view(), name="year_archive"),
    path('comment/<int:entry_id>', views.comment, name='comment'),
    path('delete/<int:blog_id>', views.delete_blog, name='delete'),
    path('update/<int:entry_id>', views.update, name='update'),
    path('update-blog/<int:blog_id>', views.update_blog, name='update_blog'),
    path('add_author', views.add_author, name='add_author'),
    path('create-blog', views.create_blog, name='create_blog'),
    path('create-entry/<int:blog_id>', views.create_entry, name='create_entry'),#This will be referenced in the blog page
    path('rate/<int:entry_id>', views.rate, name='rate'),
    path('search', views.search, name='search'),
]
