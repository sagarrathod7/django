from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# from .renderers import UserRenderers

# Create your views here.

#  Creating tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegisterationsView(APIView):
    # renderer_classes = [UserRenderers] # Use for json render Custom class
    def post(self, request, format= None):
        serializers = UserRegisterationSerializers(data= request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg': 'Resgirtion SuccessFully....'},status=status.HTTP_201_CREATED)
    
    
class UserLoginView(APIView):
    def post(self, request, format= None):
        serializers = UserLoginSerializers(data= request.data)
        serializers.is_valid(raise_exception=True)
        email = serializers.data.get('email')
        password = serializers.data.get('password')
        user = authenticate(email=email, password= password)
        if user is not None:
            token = get_tokens_for_user(user)               
            return Response({'token':token,'msg': 'Login SuccessFully....'},status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non-field_errors':['Email Or Password Is Not Match']}},status=status.HTTP_404_NOT_FOUND)
    


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format= None):
        serializers = UserProfileSerializers(request.user)
        return Response(serializers.data, status=status.HTTP_200_OK)
        
        

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format= None):
        serializers = UserChangePasswordSerializers(data= request.data, context={'user':request.user})
        serializers.is_valid(raise_exception=True)
        return Response({'msg':'Password Change Successfully'}, status=status.HTTP_200_OK)
        
        
class SendPasswordRestEmailView(APIView):
    def post(self, request, format= None):
        serializers = SendPasswordRestEmailSerializers(data= request.data)
        serializers.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send Please chack your email'}, status=status.HTTP_200_OK)
        
           
           
class RestPasswordConfirmView(APIView):
    def post(self, request,uid, token, format= None):
        serializers = UserRestPasswordSerializers(data=request.data, context={'uid':uid, 'token':token})
        serializers.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
            