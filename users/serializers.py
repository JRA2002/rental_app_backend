from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from .models import ProfileUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ProfileUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProfileUser
        fields = ('user_id', 'user', 'name', 'phone', 'DNI')

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    DNI = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'name', 'phone', 'DNI')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # Create profile
        profile_data = {
            'name': validated_data.get('name', ''),
            'phone': validated_data.get('phone', ''),
            'DNI': validated_data.get('DNI', '')
        }
        ProfileUser.objects.create(user=user, **profile_data)
        
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        try:
            token['name'] = user.profile.name
        except:
            token['name'] = ""
        return token
