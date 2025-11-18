from rest_framework import serializers
from core.serializers import UserSerializer
from .models import  Doctor , Patient , PanoramaImage , Reservation , Laboratory,Option
class DoctorSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Doctor
        fields=['id','user','phone','specialize']
    def create(self, validated_data):
        user_id=self.context['user_id']
        return Doctor.objects.create(user_id=user_id,**validated_data)
    
    
class DoctorSpecializeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = ['id','specialize', 'phone', 'user'] 

class AddPatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Patient
        fields = ['id', 'user', 'phone','age', 'diseases']

    def create(self, validated_data):
        user = self.context['request'].user
        return Patient.objects.create(user=user, **validated_data)

class PatientSuperUserSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Patient
        fields=['id','user','phone','age','diseases']
    def create(self, validated_data):
        user_id=self.context['user_id']
        return Patient.objects.create(user_id=user_id,**validated_data)

class PanoramaSuperUserImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        patient_id = self.context['patient_id']
        return PanoramaImage.objects.create(patient_id=patient_id , **validated_data)
    class Meta:
        model = PanoramaImage
        fields = ['id','image']   
class PanoramaDoctorImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        patient_id = self.context['patient_id']
        return PanoramaImage.objects.create(patient_id=patient_id , **validated_data)
    class Meta:
        model = PanoramaImage
        fields = ['id', 'image','image_with_contours','segmentation_colored_result_with_contours','segmentation_result']
        read_only_fields = ['image_with_contours','segmentation_colored_result_with_contours','segmentation_result']
        
class PanoramaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanoramaImage
        fields = ['id', 'image','image_with_contours','segmentation_colored_result_with_contours','segmentation_result']
        read_only_fields = ['image_with_contours','segmentation_colored_result_with_contours','segmentation_result']
        
        
class PanoramaImageAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id','panorama','caries' , 'image_analysis', 'restorations', 'teeth_bunds' , 'teeth_section' , 'wisdom_teeth']
        read_only_fields =['panorama','caries' , 'image_analysis', 'restorations', 'teeth_bunds' , 'teeth_section' , 'wisdom_teeth']
class Reservation1Serializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    available_times = serializers.SerializerMethodField()

    def get_available_times(self, obj):
        return obj.get_available_times()

    def validate_time(self, value):
        date = self.initial_data.get('date')
        period = self.initial_data.get('period')
        doctor_id = self.context['doctor_id']


        if period == Reservation.MORNING_PERIOD:
            all_times = set([time[0] for time in Reservation.MORNING_TIMES])
        elif period == Reservation.EVENING_PERIOD:
            all_times = set([time[0] for time in Reservation.EVENING_TIMES])
        else:
            all_times = set()

        reserved_times = set(
            Reservation.objects.filter(date=date, period=period, doctor=doctor_id)
            .values_list('time', flat=True)
        )

        available_times = sorted(all_times - reserved_times)

        if value not in available_times:
            raise serializers.ValidationError('The selected time is not available.')

        return value

    def create(self, validated_data):
        validated_data['doctor_id'] = self.context['doctor_id']
        validated_data['patient_id'] = self.context['patient_id']
        return Reservation.objects.create(**validated_data)

    class Meta:
        model = Reservation
        fields = ['id', 'doctor', 'date', 'period', 'time', 'available_times']
        
        
class Reservation2Serializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    available_times = serializers.SerializerMethodField()

    def get_available_times(self, obj):
        date = self.context.get('date')
        period = self.context.get('period')
        doctor_id = self.context.get('doctor_id')

        if not date or not period:
            return []

        if period == Reservation.MORNING_PERIOD:
            all_times = set([time[0] for time in Reservation.MORNING_TIMES])
        elif period == Reservation.EVENING_PERIOD:
            all_times = set([time[0] for time in Reservation.EVENING_TIMES])
        else:
            all_times = set()

        reserved_times = set(
            Reservation.objects.filter(doctor_id=doctor_id, date=date, period=period)
            .values_list('time', flat=True)
        )

        available_times = sorted(all_times - reserved_times)
        return available_times

    def validate(self, attrs):
        # استرجاع التاريخ والفترة
        date = attrs.get('date')
        period = attrs.get('period')
        self.context['date'] = date
        self.context['period'] = period

        available_times = self.get_available_times(None)
        selected_time = attrs.get('time')

        if selected_time not in available_times:
            raise serializers.ValidationError('The selected time is not available.')

        return attrs

    def create(self, validated_data):
        validated_data['doctor_id'] = self.context['doctor_id']
        validated_data['patient_id'] = self.context['patient_id']

        return Reservation.objects.create(**validated_data)

    class Meta:
        model = Reservation
        fields = ['id', 'doctor', 'date', 'period', 'time', 'available_times']


class LaboratorySerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Laboratory
        fields=['id','user','phone','address']
    def create(self, validated_data):
        user_id=self.context['user_id']
        return Laboratory.objects.create(user_id=user_id,**validated_data)
    
    
class ReservationSerializer(serializers.ModelSerializer):
    available_times = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'date', 'period', 'time', 'patient', 'doctor', 'available_times']

    def get_available_times(self, obj):
        return obj.get_available_times()

    def validate(self, data):
        # التحقق من أن الوقت المختار متاح بالفعل
        reservation = Reservation(
            date=data['date'],
            period=data['period'],
            time=data['time'],
            patient=data['patient'],
            doctor=data['doctor'],
        )
        reservation.clean()
        return data
    
    
class DoctorReservationTimeSerializer(serializers.ModelSerializer):
    available_times = serializers.SerializerMethodField()
    class Meta:
        model = Reservation
        fields = ['id','date', 'period', 'time','patient', 'available_times'] 
    def get_available_times(self, obj):
        # استرجاع التاريخ والفترة من السياق
        date = self.context.get('date')
        period = self.context.get('period')
        doctor_id = self.context.get('doctor_id')

        if not date or not period:
            return []

        # تحديد الأوقات بناءً على الفترة
        if period == Reservation.MORNING_PERIOD:
            all_times = set([time[0] for time in Reservation.MORNING_TIMES])
        elif period == Reservation.EVENING_PERIOD:
            all_times = set([time[0] for time in Reservation.EVENING_TIMES])
        else:
            all_times = set()

        # استرجاع الأوقات المحجوزة للطبيب المحدد
        reserved_times = set(
            Reservation.objects.filter(doctor_id=doctor_id, date=date, period=period)
            .values_list('time', flat=True)
        )

        # استبعاد الأوقات المحجوزة من الأوقات المتاحة
        available_times = sorted(all_times - reserved_times)
        return available_times

    def validate(self, attrs):
        # استرجاع التاريخ والفترة
        date = attrs.get('date')
        period = attrs.get('period')
        self.context['date'] = date
        self.context['period'] = period

        available_times = self.get_available_times(None)
        selected_time = attrs.get('time')

        if selected_time not in available_times:
            raise serializers.ValidationError('The selected time is not available.')

        return attrs

    def create(self, validated_data):
        validated_data['doctor_id'] = self.context['doctor_id']

        return Reservation.objects.create(**validated_data)

class DoctorReservationTime1Serializer(serializers.ModelSerializer):
    patient = AddPatientSerializer(read_only=True)
    available_times = serializers.SerializerMethodField()
    class Meta:
        model = Reservation
        fields = ['id','date', 'period', 'time','patient', 'available_times'] 
    def get_available_times(self, obj):

        date = self.context.get('date')
        period = self.context.get('period')
        doctor_id = self.context.get('doctor_id')

        if not date or not period:
            return []

        if period == Reservation.MORNING_PERIOD:
            all_times = set([time[0] for time in Reservation.MORNING_TIMES])
        elif period == Reservation.EVENING_PERIOD:
            all_times = set([time[0] for time in Reservation.EVENING_TIMES])
        else:
            all_times = set()

        reserved_times = set(
            Reservation.objects.filter(doctor_id=doctor_id, date=date, period=period)
            .values_list('time', flat=True)
        )


        available_times = sorted(all_times - reserved_times)
        return available_times

    def validate(self, attrs):
        date = attrs.get('date')
        period = attrs.get('period')
        self.context['date'] = date
        self.context['period'] = period

        available_times = self.get_available_times(None)
        selected_time = attrs.get('time')

        if selected_time not in available_times:
            raise serializers.ValidationError('The selected time is not available.')

        return attrs

    def create(self, validated_data):
        validated_data['doctor_id'] = self.context['doctor_id']

        return Reservation.objects.create(**validated_data)
    
    
class ReservationMyPatientSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = Patient  
        fields = ['id', 'user', 'phone', 'age', 'diseases', 'reservations']  

    def get_reservations(self, obj):
        # الحصول على جميع المواعيد لهذا المريض من الحقل `reservations` الذي تم جلبه مسبقًا
        reservations = getattr(obj, 'reservations', [])
        return [{'date': res.date, 'period': res.period, 'time': res.time} for res in reservations]
