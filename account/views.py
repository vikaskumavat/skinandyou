from datetime import datetime
import io
import os
from django.shortcuts import render

from django.urls import include, path
from api.account.utils import download_image
from api.core.models import Patient
from api.core.serializers import BranchUserSerializer, PatientDetailSerializer, PatientSerializer, UserProfileSerializer, UserRawDataSerializer
from skin_and_you import settings

from rest_framework_simplejwt import views as jwt_views
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework_simplejwt import views as jwt_views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from api.account.models import User, UserAddress
from api.account.serializers import LoginSerializer, UserDataSerializer, UserDetailSerializer, UserSerializer
from api.core.serializers import UserAddressSerializer

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.hashers import make_password

from rest_framework import filters

import csv

from rest_framework_simplejwt.backends import TokenBackend

from django.views.generic.base import TemplateView
from rest_framework.decorators import action
from rest_framework import pagination

class SSLTempView(TemplateView):
    template_name = 'account/index.html'


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False, is_staff=True).order_by("-created_at")
    serializer_class = UserSerializer
    # pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['role__name', 'name', 'email', 'gender', 'mobile']
    
    def list(self, request, *args, **kwargs):
        pagination.PageNumberPagination.page_size = request.GET.get('count_per_page', 10)
        if not request.GET.get("paginate"):
            self.pagination_class = None
            
        
        user_type = request.GET.get("user_type", 1)
        if int(user_type) == 2:
            self.serializer_class = PatientSerializer
            self.queryset = Patient.objects.select_related("user").order_by("-created_at")
        else:
            if request.GET.get("branch_id"):
                self.queryset = self.get_queryset().filter(branch_users__branch__id=request.GET.get("branch_id"))            
                    
        
        response = super().list(request, *args, **kwargs)
        return Response(status=response.status_code, data={'status': 'SUCCESS', 'data': response.data })
    
    
    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        user_type = request.GET.get("user_type", 1)
        
        request.data['password'] = make_password("no_password")
        if int(user_type) == 2:
            request.data['password'] = make_password("no_password")
            
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == 201:
            data = response.data
            if request.data['address']:
                request.data['user'] = data['id']
                serializer_obj = UserAddressSerializer(data=request.data)
                if serializer_obj.is_valid():
                    serializer_obj.save()
                else:
                    print("Serializer Error == ", serializer_obj.errors)
                    
            if int(user_type) == 2:
                request.data['patient'] = data['id']
                request.data['user'] = data['id']
                patient_serializer_obj = PatientSerializer(data=request.data)
                if patient_serializer_obj.is_valid():
                    patient_serializer_obj.save()
                else:
                    print("Patient Creation Failed ", patient_serializer_obj.errors)
            else:                
                if request.data['branch']:
                    branch_user = {'user': data['id'],'branch': request.data['branch'],'created_by_id': request.user.id}
                    serializer_obj = BranchUserSerializer(data=branch_user)
                    if serializer_obj.is_valid():
                        serializer_obj.save()
                    else:
                        print("Serializer Error == ", serializer_obj.errors)
                
        return response
    
    
    def partial_update(self, request, *args, **kwargs):
        request.data._mutable = True
        response = super().partial_update(request, *args, **kwargs)
        
        if response.status_code == 200:
            data = response.data
            if request.data['address']:
                request.data['user'] = data['id']
                
                address_list = UserAddress.objects.filter(user_id=data['id'])
                address_list.delete()
                
                serializer_obj = UserAddressSerializer(data=request.data)
                if serializer_obj.is_valid():
                    serializer_obj.save()
                else:
                    print("Serializer Error == ", serializer_obj.errors)
                    
            if request.data['branch']:
                branch_user = {'user': data['id'],'branch': request.data['branch'],'created_by_id': request.user.id}
                serializer_obj = BranchUserSerializer(data=branch_user)
                if serializer_obj.is_valid():
                    serializer_obj.save()
                else:
                    print("Serializer Error == ", serializer_obj.errors)
                
        return response
    
    
    @action(detail=False,methods=['POST'])
    def change_password(self, request, *args, **kwargs):
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user_id = kwargs.get("pk")

        user_obj = User.objects.get(id=user_id)
        
        if new_password != confirm_password:
            data = {
                'status': 'FAILED',
                'data': {'detail': "New password mismatched with confirm password"}
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

        user_obj.set_password(raw_password=new_password)
        user_obj.save()
        
        user_obj.is_active = True
        user_obj.save()
        
        data = {
            'status': 'SUCCESS',
            'data': {'detail': "Password successfully changed"}
        }
        return Response(status=status.HTTP_200_OK, data=data)
    
    
    
    def retrieve(self, request, *args, **kwargs):        
        if request.GET.get("convert") == "fk":            
            if request.GET.get("form") == "1":
                self.serializer_class = UserRawDataSerializer
                self.serializer_class.context = {'isUserAddressSerializer': 0}
            else:
                self.serializer_class = UserProfileSerializer
                self.serializer_class.context = {'isUserAddressSerializer': 1}

            
        user_type = request.GET.get("user_type", 1)
        if int(user_type) == 2:
            self.serializer_class = PatientDetailSerializer
            self.serializer_class.context = {'isUserAddressSerializer': 1}
            self.queryset = Patient.objects.select_related("user")
        
        response = super().retrieve(request, *args, **kwargs)
        return Response(status=response.status_code, data={'status': 'SUCCESS', 'data': response.data })
               
            
class LoginAPIView(jwt_views.TokenObtainPairView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        print("request.data ", request.data.get('password'))
        
        password = make_password(request.data.get('password'))
        print("Ppassword ", password)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            response = {'status': 'FAILED', 'data': {'error': e.args[0]} }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            response = {'status': 'FAILED', 'data': {'error': e.args[0]} }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['data']['access']
        valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
        user_id = valid_data.get('user_id')
        if user_id:
            user_list = User.objects.filter(id=user_id)
            if user_list:
                user_data = UserDataSerializer(user_list[0]).data
                serializer.validated_data['data']['user_data'] = user_data
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    
class ProfileViewset(APIView):
    
    def get(self, request, *args, **kwargs):        
        user_obj = User.objects.prefetch_related('user_address_detail').get(id=request.user.id)    
        return Response(status=200, data={'status': 'SUCCESS', 'data': UserProfileSerializer(user_obj).data })
        
    
class ChangePasswordAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user_obj = User.objects.get(id=request.user.id)
        if not user_obj.check_password(raw_password=password):
            data = {
                'status': 'Failed',
                'data': {'detail': "Incorrect your current password"}
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

        if new_password != confirm_password:
            data = {
                'status': 'FAILED',
                'data': {'detail': "New password mismatched with confirm password"}
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)

        user_obj.set_password(raw_password=new_password)
        user_obj.save()
        data = {
            'status': 'SUCCESS',
            'data': {'detail': "Password successfully changed"}
        }
        return Response(status=status.HTTP_200_OK, data=data)
    
    
class UserUploadByCSVAPIView(APIView):   
    permission_classes = [AllowAny] 
    def post(self, request, *args, **kwargs):
        predefined_columns = ['Name','Email', 'Password', 'Date Of Birth', 'Date Of Joining', 'Gender', 'Designation','Picture']
        
        with io.TextIOWrapper(request.FILES["file"], encoding="utf-8", newline='\n') as text_file:
            rows = csv.DictReader(text_file, delimiter=',')
            rows = list(rows)
            errors = []
            message  = 'File processed successfully'
            if rows:
                csv_colums = rows[0].keys()
                missing_columns = [k for k in predefined_columns if not k in csv_colums]
                if missing_columns:
                    response = {
                        'status': 'FAILED',
                        'data': {'error': 'Please add missing columns in CSV file','missing_columns': ', '.join(missing_columns)}
                    }
                    return Response(status=200, data=response)
                                                              
                for row in rows:
                    picture = row.get('Picture')
                    name = row.get('Name')
                    email = row.get('Email')
                    password = row.get('Password')
                    date_of_birth = row.get('Date Of Birth')
                    date_of_joining = row.get('Date Of Joining')
                    gender = row.get('Gender')
                    designation = row.get('Designation')
                    
                    date_of_joining = datetime.strptime(date_of_joining, "%d-%m-%Y").strftime("%Y-%m-%d")
                    date_of_birth = datetime.strptime(date_of_birth, "%d-%m-%Y").strftime("%Y-%m-%d")
                    
                    data = {
                        'name': name,
                        'email': email,
                        'password': make_password(password),
                        'designation': designation,
                        'date_of_birth': date_of_birth,
                        'date_of_joining': date_of_joining,
                        'gender': gender, 
                    }

                    serializer_obj = UserSerializer(data=data)
                    if serializer_obj.is_valid():
                        obj = serializer_obj.save()
                        obj.picture = download_image(picture)
                        obj.save()
                    else:
                        error = {'email': email,'message': serializer_obj.errors}
                        errors.append(error)
                        message = 'File processed successfully with below erros. kindly check and upload again'
                        
                response = {'status': 'SUCCESS', 'data': {'message': message}}        
                if errors:
                    response['data']['errors'] = errors
        
        
        return Response(status=200, data=response)
    
    
class PatientViewset(viewsets.ModelViewSet):
    queryset = Patient.objects.filter().order_by("-created_at")
    serializer_class = PatientSerializer
    # pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = [ "user__name","user__mobile","user__email","user__gender"]
    
    
    def list(self, request, *args, **kwargs):
        pagination.PageNumberPagination.page_size = request.GET.get('count_per_page', 10)
        if not request.GET.get("paginate"):
            self.pagination_class = None
        response = super().list(request, *args, **kwargs)
        return Response(status=response.status_code, data={'status': 'SUCCESS', 'data': response.data })
    
    
    
    def partial_update(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['updated_by'] = request.user.id        
        response = super().partial_update(request, *args, **kwargs)        
        if response.status_code == 200:
            data = response.data
            user_list = User.objects.filter(id=data['user']['id'])
            if user_list:
                user_obj = user_list[0]
                user_serializer_obj = UserDetailSerializer(user_obj, data=request.data, partial=True)
                
                if user_serializer_obj.is_valid():
                    user_serializer_obj.save()
                else:
                    print("Serializer Error == ", user_serializer_obj.errors)
            
            print(request.data['address'])
            if request.data['address']:                
                address_list = UserAddress.objects.filter(user_id=data['user']['id'])
                if address_list:
                    address_list.delete()
                
                request.data['created_by'] = request.user.id
                request.data['user'] = data['user']['id']

                serializer_obj = UserAddressSerializer(data=request.data)
                if serializer_obj.is_valid():
                    serializer_obj.save()
                else:
                    print("Serializer Error == ", serializer_obj.errors)
        return response
    
    def retrieve(self, request, *args, **kwargs):    
        self.serializer_class = PatientDetailSerializer    
        self.serializer_class.context = {'isUserAddressSerializer': 0}
        response = super().retrieve(request, *args, **kwargs)
        return Response(status=response.status_code, data={'status': 'SUCCESS', 'data': response.data})