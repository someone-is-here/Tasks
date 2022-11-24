from django.contrib import admin

from StationControlApp.models import Station, Indication


class StationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "state", "time_create", "time_broken", "x_position", "y_position", "z_position")
    list_display_links = ("id", "title",)
    search_field = ("title",)
    list_filter = ("state", "time_create", "time_broken")


class IndicationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "axis", "distance")
    list_filter = ("user", "axis", "distance")
    list_editable = ("axis", "distance")


admin.site.register(Station, StationAdmin)
admin.site.register(Indication, IndicationAdmin)

