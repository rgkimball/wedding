"""

"""

import os
from random import sample
import pytz
from datetime import datetime as dt

from django.views.generic import TemplateView
from django.shortcuts import render

from .models import Event
from .settings import TIME_ZONE

tz = pytz.timezone(TIME_ZONE)


class SaveDateView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):

        gallery_images = os.listdir(os.path.join(os.getcwd(), 'static/img/gallery'))
        chosen = sample(gallery_images, 1)[0]
        wedding_date = Event.objects.filter(name__contains='Ceremony')[0].date.replace(tzinfo=tz)
        days = (wedding_date - dt.now(tz=tz)).days

        return render(request, self.template_name, context={
            'safe_title': 'homepage',
            'main_image': chosen,
            'date': wedding_date.strftime('%B %d, %Y'),
            'days': days,
        })


class RSVPView(TemplateView):
    template_name = 'rsvp.html'


class TravelView(TemplateView):
    template_name = 'travel.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, context={
            'safe_title': 'travel',
        })


class WeddingPartyView(TemplateView):
    template_name = 'party.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, context={
            'safe_title': 'party',
        })


class PhotosView(TemplateView):
    template_name = 'photos.html'

    def get(self, request, *args, **kwargs):

        gallery_images = os.listdir(os.path.join(os.getcwd(), 'static/img/gallery'))
        shuffled = [x for x in sample(gallery_images, len(gallery_images))]

        return render(request, self.template_name, context={
            'safe_title': 'photos',
            'images': shuffled,
        })


class EventsView(TemplateView):
    template_name = 'events.html'

    def get(self, request, *args, **kwargs):

        events = Event.objects.all().order_by('date')

        return render(request, self.template_name, context={
            'safe_title': 'events',
            'events': events,
        })
