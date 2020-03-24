from django.contrib import admin
from .models import Guest, Party, Event


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
        'is_child'
    )

    readonly_fields = (
        'first_name',
        'last_name',
        'email',
    )


class PartyAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'save_the_date_sent',
        'save_the_date_opened',
        'invitation_id',
        'invitation_sent',
        'invitation_opened',
        'is_invited',
        'rehearsal_dinner',
        'wedding_party',
        'is_attending',
        'comments',
    )

    list_filter = (
        'category',
        'is_invited',
        'is_attending',
        'rehearsal_dinner',
        'wedding_party',
        'invitation_opened'
    )

    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'party',
        'email',
        'is_attending',
        'is_child',
        'meal'
    )

    list_filter = (
        'is_attending',
        'is_child',
        'meal',
        'party__is_invited',
        'party__category',
        'party__rehearsal_dinner'
    )


admin.site.register(Event, EventAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
