from api.account.models import User, UserAddress
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.core.models import BranchUser
# from api.core.serializers import CitySerializer, StateSerializer


class UserSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        exclude = ['is_superuser']
    
    def get_branch_name(self, obj):
        if obj:
            branch_list = BranchUser.objects.filter(user_id=obj.id)
            if branch_list:
                branch_user_obj = branch_list[0]
                return f"{branch_user_obj.branch.code} - {branch_user_obj.branch.name}" 
        return ""
            
    def to_representation(self, instance):
        self.fields['role'] = serializers.SlugRelatedField(read_only=True, slug_field='name')
        self.fields['created_at'] = serializers.DateTimeField(format='%d/%m/%Y')
        return super().to_representation(instance)
        
        
        
class UserDetailSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        exclude = ['is_superuser']
        
        
        
        
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()    
    
        
class LoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attr):
        data = super().validate(attr)
        response = {'status': 'SUCCESS','data': data }
        return response
    
    
class UserDataSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        exclude = ['is_superuser', 'password']
    
    def get_branch(self, obj):
        if obj:
            branch_list = BranchUser.objects.filter(user_id=obj.id)
            if branch_list:
                branch_user_obj = branch_list[0]
                return {
                        'branch_code': branch_user_obj.branch.code,
                        'branch_name':branch_user_obj.branch.name,
                        'branch_id':branch_user_obj.branch.id
                    } 
        return {}
            
    def to_representation(self, instance):
        self.fields['role'] = serializers.SlugRelatedField(read_only=True, slug_field='name')
        self.fields['created_at'] = serializers.DateTimeField(format='%d/%m/%Y')
        return super().to_representation(instance)
        
        