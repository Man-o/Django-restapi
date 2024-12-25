from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already exists")
            
        if data['email']: 
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email already exists")
        return data

    #If above method is valid it will return some data based on that we need to create new user  
    def create(self,validated_data): #validated_data is valid data thats come from validate method
        user=User.objects.create(username=validated_data["username"],email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return validated_data



class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Designation
        fields=['job']

class UserSerializer(serializers.ModelSerializer):
    # job=DesignationSerializer()
    # exp=serializers.SerializerMethodField()
    class Meta:
        model=Users
        fields='__all__'
        # depth=1 -->It will take all the values from foriegn_key table.
    
    #Whenever we use SerializerMethodField() in method we need to give that serializer name after 'get_'.
    def get_exp(self,obj):
        return 3
    
    def validate(self, data):
        if data['age']<18:
            raise serializers.ValidationError('Age Should be above 18')
        return data

#For validation       
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField(max_length=8)
        
            