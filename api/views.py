from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from workspace.serializers import ProjectSerializer, TaskSerializer, CustomToken
from workspace.models import Project, Task
from workspace.permissions import IsSuperAdmin, IsOwnerOrMember, IsYourTask
from workspace.filters import DueDateFilter, ProjectFilter

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
# ------------------------------------------------------------------- Projects
class ProjectView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMember]
    filterset_class = ProjectFilter
    filterset_fields = ['project']
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user))
    
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrMember]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'pk'

# ------------------------------------------------------------------- Tasks
class TaskView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsYourTask]
    filterset_class = DueDateFilter
    filterset_fields = ['completed', 'due_date']
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(Q(project__members=self.request.user) | Q(project__owner=self.request.user))
    
    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        user = self.request.user

        if not (
            user.is_superuser or
            project.owner == user or
            user in project.members.all()
        ):
            raise PermissionDenied({"error": "You cannot add task to this project"})

        serializer.save()
    
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsYourTask]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'
    
class TaskCompleteView(APIView):
    permission_classes = [IsAuthenticated, IsYourTask]
    serializer = TaskSerializer

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        self.check_object_permissions(request, task)
        if task.completed == True:
            return Response({"status": "Already Completed."})
        else: 
            task.completed = True
        task.save()
        return Response({"status": "Completed."})

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomToken