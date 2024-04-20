from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

# Registerations Class
class UserRegisterationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style= {'input_type':'password'}, write_only= True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'passwoed': {'write_only' : True}
        }
    
    # Validate Data
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password And Confirm Password doesn't match")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
# Login Class
class UserLoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length= 255)
    class Meta:
        model = User
        fields = ['email', 'password']
        
        
class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']
        
        
class UserChangePasswordSerializers(serializers.Serializer):
    password = serializers.CharField(max_length=255,style= {'input_type':'password'}, write_only= True)
    password2 = serializers.CharField(max_length=255,style= {'input_type':'password'}, write_only= True)
    class Meta:
        fields = ['password', 'password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password And Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs
        
class SendPasswordRestEmailSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
        
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email= email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print("UID...",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            # print("TOKEN...", token)
            link = 'http://localhost:3000/api/password_rest/'+uid+'/'+token
            # print("LINK...",link)
            # Send Email
            body = 'Click Following Link to Reset Ypur Password '+link 
            data = {
                'subject' : 'Reset Your Password',
                'body' : body,
                'to_email': user.email
            }
            Util.send_mail(data=data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a register User')
        
        
class UserRestPasswordSerializers(serializers.Serializer):
    password = serializers.CharField(max_length=255,style= {'input_type':'password'}, write_only= True)
    password2 = serializers.CharField(max_length=255,style= {'input_type':'password'}, write_only= True)
    class Meta:
        fields = ['password', 'password2']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
        
            if password != password2:
                raise serializers.ValidationError("Password And Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is Not valid or Expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is Not valid or Expired")
            
            
    
        