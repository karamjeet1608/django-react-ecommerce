from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser

from .serializers import UserSerializer, AuthTokenSerializer
from user.models import User


class CreateUserView(generics.CreateAPIView):
    """create a new user """

    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'is_admin': user.is_admin,
            'email': user.email,
            'name' : user.name
        })

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user

class AdminUsersAPIs(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,IsAdminUser,)
    
    def get(self, request,pk =None, format=None):
        if pk is not None:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def delete(self, request,pk):
        userinfo = User.objects.get(id=pk)
        userinfo.delete()
        return Response('User was deleted')
    
class UserAPIs(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self,request,pk=None, format=None):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    
    def put(self,request,pk=None, format=None):
        
        user = request.user
    
        # user = User.objects.get(id=pk)
        data = request.data
        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        user.save()
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

       

    
