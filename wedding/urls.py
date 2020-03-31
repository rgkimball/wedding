"""wedding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.urls import path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wedding import views


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', views.SaveDateView.as_view()),
    path(r'photos/', views.PhotosView.as_view()),
    path(r'events/', views.EventsView.as_view()),
    path(r'travel/', views.TravelView.as_view()),
    path(r'party/', views.WeddingPartyView.as_view()),
    # path(r'rsvp/', views.SaveDateView, name='rsvp'),
]

urlpatterns += staticfiles_urlpatterns()
