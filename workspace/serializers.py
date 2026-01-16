from rest_framework import serializers
from .models import Project, Task
from datetime import date, timedelta

class TaskSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField()
    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Project
        fields = '__all__'

    

    