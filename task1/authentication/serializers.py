from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

# serializer for login user
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    dob = serializers.DateField(read_only = True)
    phone = serializers.CharField(max_length=10,read_only = True)
    address = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


    def validate(self, data):
        
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
                raise serializers.ValidationError(
                    'An email address is required to log in.'
                )
        if password is None:
                raise serializers.ValidationError(
                    'A password is required to log in.'
                )

        user = authenticate(username=email, password=password)
        if user is None:
                raise serializers.ValidationError(
                    'A user with this email and password was not found.'
                )
                
        return {
                'email': user.email,
                'username': user.username,
                'token': user.token,
                'dob':user.dob,
                'phone':user.phone,
                'address':user.address
            }


# serializer for registration of new user
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'address', 'token','dob','phone']

    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token','address','dob','phone')

        read_only_fields = ('token',)
            


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

            