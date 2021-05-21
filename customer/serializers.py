from vendor.exceptions import CustomException
from vendor.models import CustomUser
from vendor.tasks import send_confirmation_mail
from vendor.serializers import UserSerializer, UserLoginSerializer


from rest_framework import serializers, generics, status
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response



from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from .models import Customer


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ("user", "address", "city", "state", "phone_number")


    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "CUSTOMER"})
        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()
        send_confirmation_mail().delay('Confirm Your Account', user, 'mail.html')
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class ConfirmAccountSerializer(serializers.Serializer):
    confirmation_code = serializers.IntegerField(required=True)


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise CustomException({'detail':'User account does not exist'})

    
            
        if not user.is_confirmed:
            raise CustomException({'detail':'User account has not been confirmed'})
        elif not user.user_type == 'CUSTOMER':
            raise CustomException({'detail':"You are not authorized as a customer"}, status_code=status.HTTP_401_UNAUTHORIZED)

        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, user)

        '''
        except User.DoesNotExist:
            raise CustomException({'detail':'User account does not exist'})
        '''
        
        return {
            'email':user.email,
            'token': jwt_token
        }

    