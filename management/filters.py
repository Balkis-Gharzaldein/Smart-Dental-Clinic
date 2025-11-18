from django_filters.rest_framework import FilterSet

from .models import Reservation  , Doctor

class DateFilter(FilterSet):
    class Meta:
        model = Reservation
        fields = {
            'date': ['exact'],
            'period': ['exact'],
        }
class DoctorFilter(FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'specialize': ['exact'],
        }