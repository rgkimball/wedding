"""

"""

import os
from random import sample
from django.views.generic import TemplateView
from django.shortcuts import render


class SaveDateView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):

        gallery_images = os.listdir(os.path.join(os.getcwd(), 'static/img/gallery'))
        chosen = sample(gallery_images, 1)[0]

        return render(request, self.template_name, context={
            'main_image': chosen,
        })


class RSVPView(TemplateView):
    template_name = 'rsvp.html'


class PhotosView(TemplateView):
    template_name = 'photos.html'

    def get(self, request, *args, **kwargs):

        gallery_images = os.listdir(os.path.join(os.getcwd(), 'static/img/gallery'))
        shuffled = [x for x in sample(gallery_images, len(gallery_images))]

        return render(request, self.template_name, context={
            'images': shuffled,
        })


class EventsView(TemplateView):
    template_name = 'events.html'

    def get(self, request, *args, **kwargs):

        events = [
            'Welcome Cocktails',
            'Rehearsal Dinner',
            'Ceremony & Reception',
        ]

        return render(request, self.template_name, context={
            'events': events,
        })
