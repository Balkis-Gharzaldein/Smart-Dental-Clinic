from django.db import models
from django.conf import settings
from django.forms import ValidationError

class Doctor(models.Model):
    GENERAL_DENTISIRY= 'GENERAL'
    COSMETIC_DENTISIRY = 'COSMETIC'
    PEDIATRIC_DENTISIRY = 'PEDIATRIC'
    ORALSURGERY_DENTISIRY = 'ORALSERGURY'
    ORTHODONTICS_DENTISIRY = 'ORTHODONTICS'
    DENTISIRY_SPECIALIZAITION = [
        (GENERAL_DENTISIRY, 'General'),
        (COSMETIC_DENTISIRY, 'Cosmetic'),
        (PEDIATRIC_DENTISIRY, 'Pediatric'),
        (ORALSURGERY_DENTISIRY, 'Oral Surgery'),
        (ORTHODONTICS_DENTISIRY, 'Orthodontics'),
    ]
    phone = models.CharField(max_length=255)
    specialize=models.CharField(max_length=255,choices=DENTISIRY_SPECIALIZAITION)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='doctor')


class Patient(models.Model):
    phone = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    diseases = models.TextField(max_length= 255 , null=True,blank=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class PanoramaImage(models.Model):
    patient= models.ForeignKey(Patient , on_delete=models.CASCADE , related_name='pano_image')
    image = models.ImageField(upload_to='managment')
    image_with_contours = models.ImageField(upload_to='segmentation', null=True,blank=True)
    segmentation_colored_result_with_contours = models.ImageField(upload_to='segmentation', null=True,blank=True)
    segmentation_result = models.ImageField(upload_to='segmentation', null=True,blank=True)

class Option(models.Model):
    panorama = models.OneToOneField(PanoramaImage,on_delete=models.CASCADE, related_name='panorama_id')
    caries = models.ImageField( null=True,blank=True)
    image_analysis = models.TextField(max_length= 255 , null=True,blank=True)
    restorations = models.ImageField( null=True,blank=True)
    teeth_bunds = models.TextField(max_length= 255 , null=True,blank=True)
    teeth_section = models.ImageField( null=True,blank=True)
    wisdom_teeth = models.ImageField( null=True,blank=True)

class Reservation(models.Model):
    MORNING_PERIOD = 'MORNING'
    EVENING_PERIOD = 'EVENING'
    PERIOD_CHOICES = [
        (MORNING_PERIOD, 'Morning'),
        (EVENING_PERIOD, 'Evening'),
    ]
    MORNING_TIMES = [
        ('8:00 AM', '8:00 AM'),
        ('8:30 AM', '8:30 AM'),
        ('9:00 AM', '9:00 AM'),
        ('9:30 AM', '9:30 AM'),
        ('10:00 AM', '10:00 AM'),
        ('10:30 AM', '10:30 AM'),
    ]
    EVENING_TIMES = [
        ('5:00 PM', '5:00 PM'),
        ('5:30 PM', '5:30 PM'),
        ('6:00 PM', '6:00 PM'),
        ('6:30 PM', '6:30 PM'),
        ('7:00 PM', '7:00 PM'),
        ('7:30 PM', '7:30 PM'),
    ]
    date = models.DateField()
    period = models.CharField(max_length=255, choices=PERIOD_CHOICES)
    time = models.CharField(max_length=255)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def clean(self):
        available_times = self.get_available_times()
        if self.time not in available_times:
            raise ValidationError(('The selected time is not available.'))

    def get_available_times(self):
        if self.period == self.MORNING_PERIOD:
            available_times = set([time[0] for time in self.MORNING_TIMES])
        elif self.period == self.EVENING_PERIOD:
            available_times = set([time[0] for time in self.EVENING_TIMES])
        else:
            return []

        reserved_times = set(
            Reservation.objects.filter(date=self.date, period=self.period, doctor=self.doctor)
            .values_list('time', flat=True)
        )

        return sorted(available_times - reserved_times)

    def __str__(self):
        return f'{self.patient.user.get_full_name()} - {self.doctor.user.get_full_name()} - {self.date} at {self.time} ({self.get_period_display()})'

class Laboratory(models.Model):
    address = models.TextField(max_length= 255 , null=True,blank=True)
    phone = models.CharField(max_length=255)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='laboratory')


