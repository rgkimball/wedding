"""

"""

import os
import subprocess
from random import sample
from datetime import datetime as dt, timedelta as td

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Event, Party
from .settings import ENV, BASE_DIR, CONFIG, GUEST_SESSION_COOKIE_NAME, SESSION_COOKIE_AGE, SESSION_COOKIE_DOMAIN
from .utils import touch, TZ, set_cookie, get_client_ip


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):

        # Set homepage image randomly from gallery
        gallery_images = os.listdir(os.path.join(os.getcwd(), 'static/img/gallery'))
        chosen = sample(gallery_images, 1)[0]
        # Retrieve wedding date from DB
        wedding_date = Event.objects.filter(name__contains='Ceremony')[0].date.replace(tzinfo=TZ)
        days = (wedding_date - dt.now(tz=TZ)).days

        # Determine whether user is logged in
        name = 'Friends & Family'
        modifier = ''
        logged_in = False
        rehearsal = False

        if GUEST_SESSION_COOKIE_NAME in request.COOKIES:
            # Attempt to query for cookie id
            try:
                party = Party.objects.get(invitation_id=request.COOKIES[GUEST_SESSION_COOKIE_NAME])
            except ObjectDoesNotExist:
                party = None

            if party:
                name = party.name

                if party.first_accessed is None:
                    party.first_accessed = dt.now()

                if party.last_accessed is not None and dt.now(tz=TZ) - party.first_accessed > td(days=5):
                    # Says 'Welcome back' if they've visited before
                    modifier = ' back'

                party.last_accessed = dt.now()
                party.save()
                logged_in = True

                rehearsal = party.rehearsal_dinner

        return render(request, self.template_name, context={
            'safe_title': 'homepage',
            'main_image': chosen,
            'date': wedding_date.strftime('%B %d, %Y'),
            'days': days,

            'logged_in': logged_in,
            'rehearsal': rehearsal,
            'repeat': modifier,
            'name': name
        })


class GuestLoginView(TemplateView):
    template_name = 'basic.html'
    subtemplate_name = '_login_form.html'

    def get(self, request, *args, **kwargs):

        form = render(request, self.subtemplate_name)

        return render(request, self.template_name, context={
            'safe_title': 'login',
            'message': form,
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

        # Check for cookies
        user = None
        rehearsal = False
        wedding_party = False

        if 'user_id' in request.COOKIES:
            user = Party.objects.get(invitation_id=request.COOKIES['user_id'])
        if user is not None:
            # If they're invited to the rehearsal dinner, show details
            rehearsal = user.rehearsal_dinner
            # If any members of the party are in the wedding party, show details
            wedding_party = any(guest.wedding_party for guest in user.ordered_guests)

        filters = {}
        if not rehearsal:
            filters['rehearsal_only'] = False
        if not wedding_party:
            filters['wedding_party_only'] = False

        events = Event.objects.filter(**filters).order_by('date')

        return render(request, self.template_name, context={
            'safe_title': 'events',
            'events': events,
        })


class RegistryView(TemplateView):
    template_name = 'registry.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, context={
            'safe_title': 'registry',
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
        if request_task and hasattr(self, request_task):
            fn = getattr(self, request_task)
            r = fn(request, key=request_key)
        return r

    def login(self, request, **kwargs):

        party = None
        msg = ''
        # Search for the party by code
        try:
            party = Party.objects.get(invitation_id=request.GET['party_code'])
            msg = '<p>Thanks for verifying! Now that we know you\'re on the list, we\'ve tailored the site ' \
                  'specifically for you, check it out!</p> '
        except ObjectDoesNotExist:
            # That didn't work, search by name now
            try:
                party = Party.objects.get(name=request.GET['party_code'])
                msg = f'<p>Thanks for verifying! Now that we know you\'re on the list, we\'ve tailored the site ' \
                      f'specifically for you! Also, from now on you can also use your secret code to ' \
                      f'sign in instead. The code to manage your party is below: <div class="secret-code">' \
                      f'{party.invitation_id}</div></p> '
            except ObjectDoesNotExist:
                pass

        if party is not None:
            # Log their visit
            if party.first_accessed is None:
                party.first_accessed = dt.now()
            party.last_accessed = dt.now()
            party.save()

            if party.email_verfied is False:
                # See if we can get some updated contact info from the guest.
                if len(party.guest_emails) == 0:
                    msg += '<p>While we have you here, we noticed we don\'t have up-to-date emails for you. If you ' \
                           'would like to share an address or two, we can keep you up to date if any of our plans ' \
                           'change. If you don\'t want to be on the list, feel free to start looking around ' \
                           'instead!</p> '
                else:
                    msg += '<p>While we have you here, would you mind verifying that we have the right contact info ' \
                           'for you? We would love to be able to update you along the way if any of our plans change.' \
                           ' If everything looks good, feel free to start looking around instead!</p> '
                msg += render(
                    request, '_guest_emails.html',
                    context={'guests': party.guest_name_and_email}
                ).content.decode('utf-8')

        else:
            debug_info = [
                dt.now(tz=TZ).strftime('%c'),
                get_client_ip(request),
                str(request.GET),
            ]
            with open(os.path.join(BASE_DIR, 'failed_lookups.txt'), 'a+') as fo:
                fo.write('|'.join(debug_info))

            msg = '<p>We couldn\'t find your name in our address book! Please try again, and don\'t forget to ' \
                  'include any punctuation from your card. </p> '
            msg += render(request, '_form.html').content.decode('utf-8')
            msg += "<p><img class=\"framed-photo centered\" src=\"/static/img/savedateenv.jpg\" /></p>"
            msg += "If you're unable to get in, <a href=\"mailto:hello@kathrynandrob.com\">let us know</a> and we " \
                   "will fix it!</a> "

        resp = render(request, self.template_name, context={
            'safe_title': 'misc',
            'message': msg,
        })

        # Most important part, set the session cookie...
        if party is not None:
            expires = dt.strftime(dt.utcnow() + td(seconds=SESSION_COOKIE_AGE), "%a, %d-%b-%Y %H:%M:%S GMT")
            resp.set_cookie(
                GUEST_SESSION_COOKIE_NAME,
                party.invitation_id,
                max_age=SESSION_COOKIE_AGE,
                expires=expires,
            )

        return resp

    def refresh_git(self, request, key=None, **kwargs):

        if key != CONFIG.get('API_KEY', None):
            return False

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
                r = output
        else:
            r = 'Local environment, no need to refresh.'

        return render(request, self.template_name, context={
            'message': r,
        })
