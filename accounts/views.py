from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.utils.decorators import method_decorator
from .serializers import *
from . import models
from hashlib import sha1
from rest_framework.response import Response
from helpers.api_helper import *
from helpers.enum_helper import *
from helpers.authentication_helper import *
from helpers.auth_helper import *
# Create your views here.
class Registration(APIView):
    @swagger_auto_schema(request_body=CredentialSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                models.User.objects.get(email=email)
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_EXISTS), status=status.HTTP_400_BAD_REQUEST)
            except:
                user=models.User.objects.create(email=email,password=sha1(password.encode()).hexdigest())
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_REGISTRATION))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    @swagger_auto_schema(request_body=CredentialSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                user=models.User.objects.get(email=email)
                auth=AuthenticationHelper(user.id)
                auth_response = auth.authentication(user,password)
                if(not auth_response):
                    return Response(api_response(ResponseType.FAILED, API_Messages.INCORRECT_PASSWORD), status=status.HTTP_400_BAD_REQUEST)
                access_token = auth.generate_access_token()
                data = {
                    'user': user.id,
                    'email': user.email,
                    'access_token': access_token
                    }
                
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGIN,data))
            except:
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_DOESNOT_EXIST))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    @method_decorator(login_required())
    def post(self, request):
        try:
            token = request.headers['Authorization'].split(" ")[-1]
            models.TokenBlackList.objects.create(token=token)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGOUT))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)
