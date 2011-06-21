from datetime import datetime
import urllib, urllib2

from django.db import models
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

from geolocation.fields import JSONField


class GeoLocationManager(models.Manager):
    def address(self, address):
        try:
            return self.get(address=address)
        except self.model.DoesNotExist:
            pass

        address = self.model(address=address)
        address.refresh_data(save=True)
        return address


class GeoLocation(models.Model):
    created = models.DateTimeField(_('created'), default=datetime.now,
        db_index=True)
    address = models.CharField(_('address'), max_length=200, unique=True)

    _data = JSONField(editable=False, blank=True, null=True)

    formatted_address = models.TextField(_('formatted address'), blank=True)
    latitude = models.DecimalField(_('latitude'), max_digits=20, decimal_places=17)
    longitude = models.DecimalField(_('longitude'), max_digits=20, decimal_places=17)

    class Meta:
        verbose_name = _('geolocation')
        verbose_name_plural = _('geolocations')

    objects = GeoLocationManager()

    def __unicode__(self):
        return self.address

    def refresh_data(self, save=False):
        request = urllib2.Request('%s?%s' % (
            'http://maps.googleapis.com/maps/api/geocode/json',
            urllib.urlencode({
                'sensor': 'false',
                'address': self.address,
                }),
            ))

        result = urllib2.urlopen(request, timeout=2) # 2 seconds
        self._data = simplejson.load(result)

        results = self._data['results'][0] # take first result
        location = results['geometry']['location']

        self.formatted_address = results['formatted_address']
        self.latitude = location['lat']
        self.longitude = location['lng']

        if save:
            self.save()