from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .utils.verifier import Verifier
import string


        
class UserSerializer(ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirmation', 'first_name', 'last_name')
    
    def create(self, validated_data):
        user = User(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    @staticmethod
    def verify(data: dict):
        verifier = Verifier()
        if not data.get("password_confirmation"):
            verifier.add("password_confirmation", "This field is required.")
        if data.get("password") != data.get("password_confirmation"):
            verifier.add("password_match", "Password does not match.")
        if User.objects.filter(username=data.get("username")).exists():
            verifier.add("username", "Username already exists.")
        return verifier.errors
    
    
class UserPasswordResetSerializer(ModelSerializer):

    old_password = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password_confirmation')
    
    @staticmethod
    def verify(data: dict):
        verifier = Verifier()
        if not data.get("password_confirmation"):
            verifier.add("password_confirmation", "This field is required.")
        if not data.get("old_password"):
            verifier.add("old_password", "This field is required.")
        if data.get("password") != data.get("password_confirmation"):
            verifier.add("password_match", "Password does not match.")
        if data.get("password") == data.get("old_password"):
            verifier.add("password_conflict", "New password cannot be the same.")
        return verifier.errors