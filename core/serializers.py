from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer , UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    access_token = serializers.SerializerMethodField()
    def get_access_token(self, instance):
        refresh = RefreshToken.for_user(instance)
        return str(refresh.access_token)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name','access_token']

class SimpleUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name','is_staff']
        
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model=User
        fields=['id','username','email','first_name','last_name']        

class SimpleUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model=User
        fields=['id','username']        
        
class AllUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model=User
        fields=['id','username','email','first_name','last_name','is_staff']        
        