from django.urls import path, include
from rest_framework_nested import routers
from . import views

# Main router for top-level resources
router = routers.DefaultRouter()

# Register User and Doctor viewsets
router.register('user', views.CreateUserViewSet, basename='user')
router.register('alldoctor', views.AllDoctorViewSet, basename='alldoctor')
router.register('allpatient', views.AllPatientViewSet, basename='allpatient')
router.register('patient', views.AddPatientViewSet, basename='patient')
router.register('panoramapatient', views.PanoramaPatientImageViewSet, basename='panoramapatient')
router.register('reservations', views.ReservationListCreateAPIView, basename='reservations')
router.register('allreservations', views.ReservationForSelectedDoctor, basename='allreservations')
router.register('mypatients', views.ReservationMyPatientViewSet, basename='mypatients')
router.register('doctorreservation', views.ReservationDoctorViewSet, basename='doctorreservation')
router.register('alllaboratory', views.AllLaboratoryViewSet, basename='alllaboratory')


# Nested router for users
user_router = routers.NestedDefaultRouter(router, 'user', lookup='user')
user_router.register('doctor', views.DoctorViewSet, basename='user-doctor')
user_router.register('laboratory', views.LaboratoryViewSet, basename='user-laboratory')
user_router.register('patient', views.PatientSuperUserViewSet, basename='user-patient')

patientSuperUser_router = routers.NestedDefaultRouter(user_router, 'patient', lookup='patient')
patientSuperUser_router.register('panorama', views.PanoramaSuperUserImageViewSet, basename='patient-panorama')

patientDoctor_router = routers.NestedDefaultRouter(router, 'allpatient', lookup='allpatient')
patientDoctor_router.register('panoramaImage', views.PanoramaDoctorImageViewSet, basename='allpatient-panoramaImage')

patient_router = routers.NestedDefaultRouter(router, 'panoramapatient', lookup='panoramapatient')
patient_router.register('restoration', views.PanoramaRestorationViewSet, basename='restoration-panoramapatient')
patient_router.register('caries', views.PanoramaCarriesViewSet, basename='caries-panoramapatient')
patient_router.register('section', views.PanoramaSectionViewSet, basename='section-panoramapatient')
patient_router.register('analysis', views.PanoramaAnalysisViewSet, basename='analysis-panoramapatient')
patient_router.register('bunds', views.PanoramaBundsViewSet, basename='bunds-panoramapatient')
patient_router.register('wisdom', views.PanoramaWisdomViewSet, basename='wisdom-panoramapatient')

doctoraddpanorama = routers.NestedDefaultRouter(patientDoctor_router, 'panoramaImage', lookup='panoramaImage')
doctoraddpanorama.register('dr_analysis', views.DoctorAnalysisPanoramaImage, basename='dr_analysis-panoramaImage')

reservation_router = routers.NestedDefaultRouter(router, 'allpatient', lookup='allpatient')
reservation_router.register('reservation', views.ReservationViewSet, basename='allpatient-reservation')

patientreservation_router = routers.NestedDefaultRouter(router, 'reservations', lookup='doctor')
patientreservation_router.register('patientreservation', views.PatientReservationViewSet, basename='doctor-patientreservation')

urlpatterns = (router.urls + user_router.urls +doctoraddpanorama.urls+ patient_router.urls + patientSuperUser_router.urls+ patientDoctor_router.urls+ reservation_router.urls + patientreservation_router.urls )



