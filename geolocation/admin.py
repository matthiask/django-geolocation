from django.contrib import admin

from geolocation.models import GeoLocation


admin.site.register(
    GeoLocation,
    list_display=(
        'address', 'formatted_address', 'created', 'latitude', 'longitude'),
    search_fields=('address', 'formatted_address'),
)
