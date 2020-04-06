"""

"""

from django.db import models
from django.contrib.sitemaps import Sitemap
from .utils import _random_uuid, MEALS, objdict


class Event(models.Model):
    """
    Event descriptions for use on the live site.
    """
    name = models.TextField()
    date = models.DateTimeField()
    description = models.TextField()
    location = models.TextField(null=True, default=None, blank=True)
    attire = models.TextField(null=True, default=None, blank=True)
    transportation = models.TextField(null=True, default=None, blank=True)
    parking = models.TextField(null=True, default=None, blank=True)
    other_info = models.TextField(null=True, default=None, blank=True)
    wedding_party_only = models.NullBooleanField(default=False)
    rehearsal_only = models.NullBooleanField(default=False)
    no_children = models.NullBooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name)


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    category = models.CharField(max_length=20, null=True, blank=True)
    first_accessed = models.DateTimeField(null=True, blank=True, default=None)
    last_accessed = models.DateTimeField(null=True, blank=True, default=None)
    invitation_id = models.CharField(max_length=32, db_index=True, default=_random_uuid, unique=True)
    is_invited = models.BooleanField(default=False)
    rehearsal_dinner = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)
    email_verfied = models.NullBooleanField(default=False)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('category', '-is_invited', 'name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('is_child', 'pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return list(filter(None, self.guest_set.values_list('email', flat=True)))

    @property
    def guest_name_and_email(self):
        res = list(filter(None, self.guest_set.values('first_name', 'last_name', 'email')))
        return [objdict(v) for v in res]

    def get_by_invitation(self, invitation_id):
        return self.objects.get(invitation_id=invitation_id)


class Guest(models.Model):
    """
    A single guest
    """
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.NullBooleanField(default=None)
    wedding_party = models.BooleanField(default=False)
    meal = models.CharField(max_length=20, choices=MEALS, null=True, blank=True)
    is_child = models.BooleanField(default=False)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1

    def items(self):
        return

    def lastmod(self):
        return