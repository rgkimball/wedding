"""

"""

import os
import subprocess
from random import sample
from datetime import datetime as dt

from django.views.generic import TemplateView
from django.shortcuts import render

from .models import Event
from .settings import ENV, BASE_DIR, CONFIG
from .utils import touch, TZ


class SaveDateView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):

        gallery_images = os.listdir(os.path.join(os.getcwd(), 'static/img/gallery'))
        chosen = sample(gallery_images, 1)[0]
        wedding_date = Event.objects.filter(name__contains='Ceremony')[0].date.replace(tzinfo=TZ)
        days = (wedding_date - dt.now(tz=TZ)).days

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


def page_not_found(request, exception):
    template_name = 'basic.html'

    return render(
        request,
        template_name,
        context={'message': 'Sorry, we can\'t find that page! Try using one of the links above instead.'}
    )


class API(TemplateView):
    template_name = 'basic.html'

    def get(self, request, *args, **kwargs):

        request_key = request.GET.get('key', '')
        request_task = request.GET.get('task', '')

        r = None

        if request_key != CONFIG.get('API_KEY', None):
            r = 'Invalid Key'
        else:
            if request_task and hasattr(self, request_task):
                fn = getattr(self, request_task)
                r = fn()

        return render(request, self.template_name, context ={
            'message': str(r)
        })

    def refresh_git(self):

        if ENV in ('test', 'prod'):

            proc = subprocess.Popen(["git", "pull"], cwd=BASE_DIR, stdout=subprocess.PIPE)
            output = proc.communicate()[0].decode('utf-8')

            if output == 'Already up to date.':
                return output
            else:
                proc = subprocess.Popen(["git", "checkout -f develop"], cwd=BASE_DIR, stdout=subprocess.PIPE)
                output = proc.communicate()[0].decode('utf-8')
                wsgi_file = '/var/www/rgk_pythonanywhere_com_wsgi.py'
                # touch file to trigger pythonanywhere to reload the app
                touch(wsgi_file)
                return output
        else:
            return 'Local environment, no need to refresh.'
