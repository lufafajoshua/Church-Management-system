from django.contrib import admin
from .models import Blog, Author, Entry, Comments

admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Entry)
admin.site.register(Comments)
