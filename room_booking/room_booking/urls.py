"""room_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from reservation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.Home.as_view(), name='home'),
    path('room/new/', views.NewRoom.as_view(), name='new_room'),
    re_path(r'^room/modify/(?P<id>(\d)+)/$', views.ModifyRoom.as_view(), name='modify_room'),
    re_path(r'^room/delete/(?P<id>(\d)+)/$', views.DeleteRoom.as_view(), name='delete_room'),
    re_path(r'^room/(?P<id>(\d)+)/$', views.ShowRoom.as_view(), name='show_room'),
    path('', views.AllRooms.as_view(), name='all_rooms'),
    re_path(r'^reservation/(?P<room_id>(\d)+)/$', views.ReservationView.as_view(), name='reservation'),
    path('search/', views.SearchRoom.as_view(), name='search_room'),
]
