from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'userviewset', UserViewSet, basename='user')
urlpatterns=[
    path('',include(router.urls)),
    path('register/',RegisterAPI.as_view()),
    path('login/',LoginAPI.as_view()),

    # path('user/',index),
    # path('users/',user),
    # path('users/<int:id>/',user)
    path('login/',login),
    path('user-api/',UserAPI.as_view()),

]