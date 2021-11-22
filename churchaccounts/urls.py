from django.urls import path, include
from . import views

app_name = 'churchaccounts'
urlpatterns =[
    path('church-list', views.church_list, name='list'),
    path('study-group/<int:id>', views.study_group, name='study-group'),
    path('join-group/<int:group_id>', views.join_group, name='join_group'),
    path('project/<int:project_id>', views.project, name='project'),
    path('account/<int:church_id>', views.church_account, name='display_account'),
    path('create-account', views.create_account, name='create_account'),
    path('create-group/<int:church_id>', views.create_group, name='create_group'),
    path('delete-account/<int:church_id>', views.delete_account, name='delete'),#Ensure that u use the church_id in the views
    path('create-program/<int:church_id>', views.create_program, name='create_program'),
    path('create-contact/<int:church_id>', views.create_contact, name='create_contact'),
    path('create-contact-message', views.create_contact_message, name='create_contact_message'),
    path('create-project/<int:church_id>', views.create_project, name='create_project'),
    path('make-payment/<int:project_id>', views.make_payment, name='make_payment'),
    path('update-transaction', views.update_transaction, name='update_transaction'),
    path('announcements', views.announcements, name='announcements'),
    path('announcement_detail/<int:id>', views.announcement_detail, name='announcement_detail'),
    path('events', views.events, name='events'),
    path('event-detail/<int:id>', views.event_detail, name='event_detail'),
    path('news', views.news, name='news'),
    path('news_detail/<int:id>', views.news_detail, name='news_detail'),
]
