from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserPasswordResetSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
class UserCreateViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes  = [AllowAny]
    
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        errors = serializer.verify(data=request.data)
        if serializer.is_valid() and not errors:
            serializer.save()
            request.data.pop("password"), request.data.pop("password_confirmation")
            return Response(request.data, status=status.HTTP_201_CREATED)
        errors = serializer.errors | errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserViewSet(ModelViewSet):
    
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes  = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
        
        
    def retrieve(self, request: Request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance = request.user
        instance.destroy()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class UserPasswordResetViewSet(ModelViewSet):
    # ? TODO: Implementar reset de senha de usuário 
    
    serializer_class = UserPasswordResetSerializer
    queryset = User.objects.all()
    permission_classes  = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    def update(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        errors = serializer.verify(data=request.data)
        if serializer.is_valid() and not errors:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errors = serializer.errors | errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        