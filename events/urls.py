from django.urls import path, include
from . import views


app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<slug>/', views.event_detail, name='event'),
    path('event/add/', views.event_add, name='event_add'),
]
