from .exceptions import CustomException
from .models import CustomUser, Vendor
from .tasks import send_confirmation_mail

from rest_framework import serializers, generics, status
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response



from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login




JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "uid",
            "email",
            "first_name",
            "last_name",
            "password",
            "user_type",
            "confirmation_code",
            "is_confirmed",
            "date_joined",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
            "is_confirmed": {"read_only": True},
            "confirmation_code": {"read_only": True},
            "user_type": {"read_only": True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user



class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)





class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ("user", "shop_name", "description", "phone_number", "closed", "suspended")

        extra_kwargs = {
            "closed": {"read_only": True},
            "suspended": {"read_only": True},
        }


    def create(self, validated_data):
        
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "VENDOR"})
        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()
        

        new_user = {'first_name':user.first_name, 'email':user.email, 'confirmation_code':user.confirmation_code}
        
        
        #send_confirmation_mail.delay('Confirm Your Account', new_user)

    

    
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor
        


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
        elif not user.user_type == 'VENDOR':
            raise CustomException({'detail':"You are not authorized as a vendor "}, status_code=status.HTTP_401_UNAUTHORIZED)

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

    