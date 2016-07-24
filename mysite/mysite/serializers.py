from rest_framework import serializers
from rest_framework_extras.serializers import HyperlinkedModelSerializer, FormMixin

from mysite.models import Manufacturer, Car
from mysite.admin import ManufacturerAdminForm



class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        #fields = ('id', 'title', 'code', 'linenos', 'language', 'style')


class ManufacturerSerializer(FormMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Manufacturer
        form = ManufacturerAdminForm

    def validate_year(self, value):
        if value < 2010:
            raise serializers.ValidationError("Serializer says year must be after 2010")
        return value
