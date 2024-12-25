from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serilizers import *

class RegisterAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("User created")
        return Response(serializer.errors)
        
class LoginAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        user=authenticate(username=serializer.data['username'],email=serializer.data['email'],password=serializer.data['password'])
        if not user:
            return Response("Invalid credentials")
        token=Token.objects.get_or_create(user=user)
        return Response({'message':serializer.data['username'],'token':str(token)})
        


@api_view(['GET','POST'])
def index(request):
    if request.method=='POST':
        user={
            'Username':'Mano',
            'Password':1234
        }
        data=request.data
        print(data['user'])
        return Response("posted")
    
    elif request.method=='GET':
        print(request.GET.get('search'))
        return Response('Got the data')
    

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def user(request):
    if request.method=='GET':
        UO=Users.objects.all()
        serializer=UserSerializer(UO,many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        data=request.data
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method=='PUT':
        data=request.data
        UO=Users.objects.get(id=data['id'])
        serializer=UserSerializer(UO,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method=='PATCH':
        data=request.data
        UO=Users.objects.get(id=data['id'])
        serializer=UserSerializer(UO,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    else:
        data=request.data
        UO=Users.objects.get(id=data['id'])
        UO.delete()
        return Response("User deleted")


#This api view is use to validate the posted data
@api_view(['POST'])
def login(request):
    data=request.data
    serializer=LoginSerializer(data=data)
    if serializer.is_valid():
        data=serializer.validated_data
        return Response("validated")
    return Response(serializer.errors)

class UserAPI(APIView):
    permission_classes=[IsAuthenticated]
    #IsAuthenticated is a built-in permission class in DRF that ensures that only authenticated users can access the API endpoint.
    authentication_classes=[TokenAuthentication]
    #TokenAuthentication is a built-in authentication class in DRF that authenticates users based on a token.
    def get(self,request):
        print(request.user) #By using this we can see which user is logged in
        UO=Users.objects.all()
        serializer=UserSerializer(UO,many=True)
        return Response(serializer.data)
        
    
    def post(self,request):
        data=request.data
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Data stored in DB")
        return Response("Invalid serializer")
        
    
    def put(self,request):
        data=request.data
        UO=Users.objects.get(id=data['id'])
        serializer=UserSerializer(UO,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("Updated-PUT method")
        return Response("Invalid serializer")

    
    def patch(self,request):
        data=request.data
        UO=Users.objects.get(id=data['id'])
        serializer=UserSerializer(UO,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Updated-PATCH method")
        return Response("Invalid serializer")
    
    def delete(self,request):
        data=request.data
        UO=Users.objects.get(id=data['id'])
        UO.delete()
        return Response("User deleted")

#By using viewsets we can easily do the CRUD operations with two lines of code.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset=Users.objects.all()

    #list method is used to search particular data
    def list(self,request):
        search=request.GET.get("search")
        queryset=self.queryset
        if search:
            queryset=queryset.filter(name__startswith=search)
        serializer=UserSerializer(queryset,many=True)
        return Response({"data":serializer.data})