from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from .models import Doctor , Patient , PanoramaImage , Reservation ,Laboratory,Option
from core.models import User
from core.serializers import UserCreateSerializer , SimpleUserCreateSerializer 
from .serializer import DoctorSerializer,ReservationMyPatientSerializer,DoctorReservationTime1Serializer, DoctorReservationTimeSerializer ,DoctorSpecializeSerializer , AddPatientSerializer, PatientSuperUserSerializer , PanoramaImageSerializer ,PanoramaDoctorImageSerializer , PanoramaSuperUserImageSerializer ,ReservationSerializer,Reservation1Serializer,Reservation2Serializer, LaboratorySerializer,PanoramaImageAnalysisSerializer
from .permission import IsSuperUser , IsDoctor
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend 
from .filters import DateFilter  ,DoctorFilter
from rest_framework.permissions import IsAuthenticated 
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import os
import subprocess
import requests
from rest_framework import status
from src import main , teeth_section , restorations , caries , teeth_section , image_analysis , teeth_bunds ,wisdom_teeth
from django.core.files import File
from django.conf import settings
import os
from django.db.models import Prefetch

# viewset for create user by super user
class CreateUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SimpleUserCreateSerializer
    permission_classes=[IsAuthenticated]
    
# viewset for make user a doctor 
class DoctorViewSet(ModelViewSet):  
    serializer_class = DoctorSerializer
    permission_classes=[IsAuthenticated,IsSuperUser]

    def get_queryset(self):
        user_id = self.kwargs.get('user_pk')
        return Doctor.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        return {'user_id': self.kwargs['user_pk']}
    
# viewset return all doctors
class AllDoctorViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):  
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    permission_classes=[IsAuthenticated,IsSuperUser]

class AllLaboratoryViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):  
    serializer_class = LaboratorySerializer
    queryset = Laboratory.objects.all()
    permission_classes=[IsAuthenticated,IsSuperUser]

# viewset for make user a patient by your self
class AddPatientViewSet(ModelViewSet):  
    serializer_class = AddPatientSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)
    
# viewset for make user a patient by super user
class PatientSuperUserViewSet(ModelViewSet):  
    serializer_class = PatientSuperUserSerializer
    permission_classes=[IsAuthenticated,IsSuperUser]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_pk')
        return Patient.objects.filter(user_id=user_id)

    def get_serializer_context(self):
        return {'user_id': self.kwargs['user_pk']}

# viewset for return all patient for super user , doctor , Laboratory
class AllPatientViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):  
    serializer_class = PatientSuperUserSerializer
    queryset = Patient.objects.all()
    permission_classes=[IsAuthenticated,IsDoctor]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    
# viewset super user add panaorama image for patient
class PanoramaSuperUserImageViewSet(ModelViewSet):
    serializer_class = PanoramaSuperUserImageSerializer
    permission_classes=[IsAuthenticated,IsSuperUser]
    def get_serializer_context(self):
        return {'patient_id':self.kwargs['patient_pk']}
    def get_queryset(self):
        return PanoramaImage.objects.filter(patient_id=self.kwargs['patient_pk'])

# viewset doctor and laboratory add panaorama image for patient
class PanoramaDoctorImageViewSet(ModelViewSet):
    serializer_class = PanoramaDoctorImageSerializer
    permission_classes=[IsAuthenticated,IsDoctor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['patient_id'] = self.kwargs['allpatient_pk']
        return context
    def get_queryset(self):
        return PanoramaImage.objects.filter(patient_id=self.kwargs['allpatient_pk'])
    
    def perform_create(self, serializer):
        patient = get_object_or_404(Patient, id=self.kwargs['allpatient_pk'])
        panorama_image = serializer.save(patient=patient)
        image_path = panorama_image.image.path  # Get the path of the image from your model instance

        # Call the model analysis function
        image_with_contours_path, segmentation_colored_result_with_contours_path, segmentation_result_path = main.model_analysis(image_path)

        # Open and save the image_with_contours file
        with open(image_with_contours_path, 'rb') as f:
            panorama_image.image_with_contours.save(os.path.basename(image_with_contours_path), File(f), save=False)

        # Open and save the segmentation_colored_result_with_contours file
        with open(segmentation_colored_result_with_contours_path, 'rb') as f:
            panorama_image.segmentation_colored_result_with_contours.save(os.path.basename(segmentation_colored_result_with_contours_path), File(f), save=False)

        # Open and save the segmentation_result file
        with open(segmentation_result_path, 'rb') as f:
            panorama_image.segmentation_result.save(os.path.basename(segmentation_result_path), File(f), save=False)

        panorama_image.save()

# viewset patient add panaorama image 
class PanoramaPatientImageViewSet(ModelViewSet):
    serializer_class = PanoramaImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = get_object_or_404(Patient, user=self.request.user)
        return PanoramaImage.objects.filter(patient=patient).all()

    def perform_create(self, serializer):
        patient = get_object_or_404(Patient, user=self.request.user)
        panorama_image = serializer.save(patient=patient)
        image_path = panorama_image.image.path  # Get the path of the image from your model instance

        # Call the model analysis function
        image_with_contours_path, segmentation_colored_result_with_contours_path, segmentation_result_path = main.model_analysis(image_path)

        # Open and save the image_with_contours file
        with open(image_with_contours_path, 'rb') as f:
            panorama_image.image_with_contours.save(os.path.basename(image_with_contours_path), File(f), save=False)

        # Open and save the segmentation_colored_result_with_contours file
        with open(segmentation_colored_result_with_contours_path, 'rb') as f:
            panorama_image.segmentation_colored_result_with_contours.save(os.path.basename(segmentation_colored_result_with_contours_path), File(f), save=False)

        # Open and save the segmentation_result file
        with open(segmentation_result_path, 'rb') as f:
            panorama_image.segmentation_result.save(os.path.basename(segmentation_result_path), File(f), save=False)

        panorama_image.save()
class ReservationViewSet(ModelViewSet):
    serializer_class = Reservation1Serializer
    permission_classes = [IsAuthenticated, IsDoctor]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = DateFilter

    def get_queryset(self):
        return Reservation.objects.filter(patient_id=self.kwargs['allpatient_pk'], doctor=self.request.user.doctor.id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['doctor_id'] = self.request.user.doctor.id  
        context['patient_id'] = self.kwargs['allpatient_pk']
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # استرجاع التاريخ والفترة من الفلترة
        date = request.query_params.get('date')
        period = request.query_params.get('period')
        doctor = self.request.user.doctor.id 
        
        # إذا تم تحديد الفترة
        if period == Reservation.MORNING_PERIOD:
            all_times = set([time[0] for time in Reservation.MORNING_TIMES])
        elif period == Reservation.EVENING_PERIOD:
            all_times = set([time[0] for time in Reservation.EVENING_TIMES])
        else:
            all_times = set()

        # استرجاع الأوقات المحجوزة
        reserved_times = set(
            Reservation.objects.filter(date=date, period=period , doctor=doctor)
            .values_list('time', flat=True)
        )

        # استبعاد الأوقات المحجوزة من الأوقات الكلية
        available_times = sorted(all_times - reserved_times)

        return Response({
            'available_times': available_times
        })
        

class LaboratoryViewSet(ModelViewSet):  
    serializer_class = LaboratorySerializer
    permission_classes=[IsAuthenticated,IsSuperUser]

    def get_queryset(self):
        user_id = self.kwargs.get('user_pk')
        return Laboratory.objects.filter(user_id=user_id)
    def get_serializer_context(self):
        return {'user_id': self.kwargs['user_pk']}
    

class ReservationListCreateAPIView(ListModelMixin,GenericViewSet):
    serializer_class=DoctorSpecializeSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = DoctorFilter
    def get_queryset(self):
        specialize = self.request.query_params.get('specialize')
        return Doctor.objects.filter(specialize=specialize)
        
        

class PatientReservationViewSet(ModelViewSet):
    serializer_class = Reservation2Serializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = DateFilter

    def get_queryset(self):
        return Reservation.objects.filter(doctor_id=self.kwargs['doctor_pk'], patient=self.request.user.patient)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['doctor_id'] = self.kwargs['doctor_pk']
        context['patient_id'] = self.request.user.patient.id
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())


        date = request.query_params.get('date')
        period = request.query_params.get('period')

        if period == Reservation.MORNING_PERIOD:
            all_times = set([time[0] for time in Reservation.MORNING_TIMES])
        elif period == Reservation.EVENING_PERIOD:
            all_times = set([time[0] for time in Reservation.EVENING_TIMES])
        else:
            all_times = set()


        reserved_times = set(
            Reservation.objects.filter(doctor_id=self.kwargs['doctor_pk'], date=date, period=period)
            .values_list('time', flat=True)
        )

        available_times = sorted(all_times - reserved_times)

        return Response({
            'available_times': available_times
        })
        

class ReservationForSelectedDoctor(ModelViewSet):
    serializer_class=DoctorReservationTime1Serializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = DateFilter
    def get_queryset(self):
        # specialize = self.request.query_params.get('specialize')
        return Reservation.objects.filter(doctor=self.request.user.doctor.id).all()
    
    
# **************************************************************
class ReservationMyPatientViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ReservationMyPatientSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        queryset = Patient.objects.filter(
            reservation__doctor=self.request.user.doctor
        ).distinct().prefetch_related(
            Prefetch(
                'reservation_set',
                queryset=Reservation.objects.filter(doctor=self.request.user.doctor),
                to_attr='reservations'
            )
        )
        return queryset

class ReservationDoctorViewSet(ModelViewSet):
    serializer_class = DoctorReservationTimeSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = DateFilter

    def get_queryset(self):
        return Reservation.objects.filter( doctor=self.request.user.doctor.id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['doctor_id'] = self.request.user.doctor.id  
        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        

        date = request.query_params.get('date')
        period = request.query_params.get('period')
        doctor = self.request.user.doctor.id 
        

        if period == Reservation.MORNING_PERIOD:
            all_times = set([time[0] for time in Reservation.MORNING_TIMES])
        elif period == Reservation.EVENING_PERIOD:
            all_times = set([time[0] for time in Reservation.EVENING_TIMES])
        else:
            all_times = set()

        reserved_times = set(
            Reservation.objects.filter(date=date, period=period , doctor=doctor)
            .values_list('time', flat=True)
        )
        available_times = sorted(all_times - reserved_times)

        return Response({
            'available_times': available_times
        })



# *********************************************************************
    

class PanoramaRestorationViewSet(ModelViewSet):
    serializer_class = PanoramaImageAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = get_object_or_404(Patient, user=self.request.user)
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])
        return Option.objects.filter(panorama=panorama_image)

    def perform_create(self, serializer):
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])

        option, created = Option.objects.get_or_create(panorama=panorama_image)

        image_with_contours_path = panorama_image.image_with_contours.path
        
        output_image_path = os.path.join('C:/New folder (2)/Dental_Clinc/media/analysis', f'restorations_{panorama_image.id}.jpg')
        
        restorations.highlight_restorations_on_base_image(image_with_contours_path, output_image_path)

        with open(output_image_path, 'rb') as f:
            option.restorations.save(os.path.basename(output_image_path), File(f), save=False)

        option.save()



class PanoramaCarriesViewSet(ModelViewSet):
    serializer_class = PanoramaImageAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = get_object_or_404(Patient, user=self.request.user)
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])
        return Option.objects.filter(panorama=panorama_image)

    def perform_create(self, serializer):
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])

        option, created = Option.objects.get_or_create(panorama=panorama_image)

        image_with_contours_path = panorama_image.image_with_contours.path
        
        output_image_path = os.path.join('C:/New folder (2)/Dental_Clinc/media/analysis', f'caries_{panorama_image.id}.jpg')
        
        caries.highlight_caries_on_base_image(image_with_contours_path, output_image_path)

        with open(output_image_path, 'rb') as f:
            option.caries.save(os.path.basename(output_image_path), File(f), save=False)

        option.save()
        
        
class PanoramaSectionViewSet(ModelViewSet):
    serializer_class = PanoramaImageAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = get_object_or_404(Patient, user=self.request.user)
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])
        return Option.objects.filter(panorama=panorama_image)

    def perform_create(self, serializer):
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])

        option, created = Option.objects.get_or_create(panorama=panorama_image)

        image_with_contours_path = panorama_image.image_with_contours.path
        segmentation_result_path = panorama_image.segmentation_result.path
        
        output_image_path = os.path.join('C:/New folder (2)/Dental_Clinc/media/analysis', f'section_{panorama_image.id}.jpg')
        
        teeth_section.Teeth_Section_with_Rectangles(image_with_contours_path,segmentation_result_path, output_image_path)


        with open(output_image_path, 'rb') as f:
            option.teeth_section.save(os.path.basename(output_image_path), File(f), save=False)

        option.save()        
        
class PanoramaWisdomViewSet(ModelViewSet):
    serializer_class = PanoramaImageAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = get_object_or_404(Patient, user=self.request.user)
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])
        return Option.objects.filter(panorama=panorama_image)

    def perform_create(self, serializer):
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])

        option, created = Option.objects.get_or_create(panorama=panorama_image)

        image_with_contours_path = panorama_image.image_with_contours.path
        segmentation_result_path = panorama_image.segmentation_result.path
        
        output_image_path = os.path.join('C:/New folder (2)/Dental_Clinc/media/analysis', f'wisdom_{panorama_image.id}.jpg')
        
        wisdom_teeth.Wisdom_Teeth(image_with_contours_path,output_image_path)

        with open(output_image_path, 'rb') as f:
            option.wisdom_teeth.save(os.path.basename(output_image_path), File(f), save=False)

        option.save()        


class PanoramaAnalysisViewSet(ModelViewSet):
    serializer_class = PanoramaImageAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient = get_object_or_404(Patient, user=self.request.user)
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])
        return Option.objects.filter(panorama=panorama_image)

    def perform_create(self, serializer):
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])

        option, created = Option.objects.get_or_create(panorama=panorama_image)

        image_with_contours_path = panorama_image.image_with_contours.path

        analysis_result = image_analysis.analysis(image_with_contours_path)
        option.image_analysis = analysis_result 
        option.save()
        
class PanoramaBundsViewSet(ModelViewSet):
    serializer_class = PanoramaImageAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # patient = get_object_or_404(Patient, user=self.request.user)
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])
        return Option.objects.filter(panorama=panorama_image).all()

    def perform_create(self, serializer):
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramapatient_pk'])

        option, created = Option.objects.get_or_create(panorama=panorama_image)

        image_with_contours_path = panorama_image.image_with_contours.path

        bunds_result = teeth_bunds.Dental_Bunds(image_with_contours_path)

        option.teeth_bunds = bunds_result 
        option.save()
        

class DoctorAnalysisPanoramaImage(ModelViewSet):
    serializer_class = PanoramaImageAnalysisSerializer
    permission_classes = [IsAuthenticated,IsDoctor]

    def get_queryset(self):
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramaImage_pk'])
        return Option.objects.filter(panorama=panorama_image)

    def perform_create(self, serializer):
        panorama_image = get_object_or_404(PanoramaImage, id=self.kwargs['panoramaImage_pk'])

        option, created = Option.objects.get_or_create(panorama=panorama_image)
        image_with_contours_path = panorama_image.image_with_contours.path
        segmentation_result_path = panorama_image.segmentation_result.path

        output_image_path = os.path.join('C:/New folder (2)/Dental_Clinc/media/analysis', f'restorations_{panorama_image.id}.jpg')
        restorations.highlight_restorations_on_base_image(image_with_contours_path, output_image_path)
        with open(output_image_path, 'rb') as f:
            option.restorations.save(os.path.basename(output_image_path), File(f), save=False)
        
        output_image_path = os.path.join('C:/New folder (2)/Dental_Clinc/media/analysis', f'caries_{panorama_image.id}.jpg')
        caries.highlight_caries_on_base_image(image_with_contours_path, output_image_path)
        with open(output_image_path, 'rb') as f:
            option.caries.save(os.path.basename(output_image_path), File(f), save=False)
        
        
        output_image_path = os.path.join('C:/New folder (2)/Dental_Clinc/media/analysis', f'section_{panorama_image.id}.jpg')
        teeth_section.Teeth_Section_with_Rectangles(image_with_contours_path,segmentation_result_path, output_image_path)
        with open(output_image_path, 'rb') as f:
            option.teeth_section.save(os.path.basename(output_image_path), File(f), save=False)
        
        
        output_image_path4 = os.path.join('C:/New folder (2)/Dental_Clinc/media/analysis', f'wisdom_{panorama_image.id}.jpg')
        wisdom_teeth.Wisdom_Teeth(image_with_contours_path,output_image_path)
        with open(output_image_path, 'rb') as f:
            option.wisdom_teeth.save(os.path.basename(output_image_path), File(f), save=False)
        
        bunds_result = teeth_bunds.Dental_Bunds(image_with_contours_path)
        analysis_result = image_analysis.analysis(image_with_contours_path)

        option.teeth_bunds = bunds_result 
        option.image_analysis = analysis_result 

        option.save()
