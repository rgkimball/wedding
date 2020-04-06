from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Guest, Party, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    fields = (
        'name',
        'date',
        'description',
        'location',
        'attire',
        'transportation',
        'parking',
        'other_info',
        'wedding_party_only',
        'rehearsal_only',
        'no_children',
    )


class GuestInline(admin.TabularInline):

    model = Guest

    fields = (
        'first_name',
        'last_name',
        'email',
        'is_attending',
        'meal',
        'is_child',
        'wedding_party',
    )

    readonly_fields = (
        'first_name',
        'last_name',
        'email',
    )


class PartyResource(resources.ModelResource):

    class Meta:
        model = Party
        # Fields used as PK's to determine whether to update existing or add new records
        import_id_fields = ('name', )


@admin.register(Party)
class PartyAdmin(ImportExportModelAdmin):

    list_display = (
        'name',
        'category',
        'is_invited',
        'invitation_id',
        'first_accessed',
        'last_accessed',
        'rehearsal_dinner',
        'is_attending',
        'comments',
    )

    list_filter = (
        'category',
        'is_invited',
        'is_attending',
        'rehearsal_dinner',
        'last_accessed',
    )

    inlines = [GuestInline]
    resource_class = PartyResource


class GuestResource(resources.ModelResource):

    class Meta:
        model = Guest
        # Fields used as PK's to determine whether to update existing or add new records
        import_id_fields = ('party', 'first_name', 'last_name', )

    @staticmethod
    def _get_party_by_name(name):
        try:
            party = Party.objects.get(name=name)
        except:
            party = Party.objects.filter(name=name)

            if not len(party):
                return None
            else:
                party = party[0]

        return party

    def before_import_row(self, row, **kwargs):

        # Need to intercept party address names and replace with ids, or create a party on the fly.
        # No value checking here because we shouldn't be importing guests without a party
        party = self._get_party_by_name(row['party'])

        if party is None:
            Party.objects.create(
                name=row['party'],
                category='Uncategorized',
            )
            # Get newly created party
            party = self._get_party_by_name(row['party'])

        # Replace party string name with party id
        row['party'] = party.id

        return row


@admin.register(Guest)
class GuestAdmin(ImportExportModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'party',
        'email',
        'wedding_party',
        'is_attending',
        'is_child',
        'meal',
    )

    list_filter = (
        'is_attending',
        'meal',
        'wedding_party',
        'party__is_invited',
        'party__category',
        'party__rehearsal_dinner',
        'is_child',
    )

    resource_class = GuestResource
