from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Project, Task

class TaskSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField()
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Task
        fields = ['id', 'title', 'details', 'due_date', 'completed', 'flag', 'created_at', 'project', 'created_by']

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Project
        fields = ['id', 'name', 'owner', 'description', 'created_at', 'members']
        read_only_fields = ['owner', 'created_at']

class CustomToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['username'] = user.username
        return token
