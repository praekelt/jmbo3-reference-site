from rest_framework import generics, viewsets

from mysite.models import Car, Manufacturer
from mysite.serializers import CarSerializer

from mysite.serializers import ManufacturerSerializer


'''
class CarList(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
'''

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    #form = ManufacturerAdminForm
