from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    # standard writing in rest_framework: point a variable to class
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    # use renderer_classes to show api on chrome etc.
    # DEFAULT_RENDERER_CLASSES can change default renderer in settings
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
