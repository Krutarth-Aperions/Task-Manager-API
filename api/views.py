from workspace.serializers import ProjectSerializer, TaskSerializer
from workspace.models import Project, Task
from workspace.permissions import IsSuperAdmin, IsOwner, IsYourTask
from workspace.filters import DueDateFilter, ProjectFilter

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# ------------------------------------------------------------------- Projects
class ProjectView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_class = ProjectFilter
    filterset_fields = ['project']
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'pk'

# ------------------------------------------------------------------- Tasks
class TaskView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsOwner, IsYourTask,]
    filterset_class = DueDateFilter
    filterset_fields = ['completed', 'due_date']
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
    
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsYourTask]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'

    def patch(self, request, pk):
        task = self.get_object()
        if task.completed == True:
            return Response({"status": "Already Completed."})
        else: 
            task.completed = True
        task.save()
        return Response({"status": "Completed."})
    
class TaskCompleteView(APIView):
    permission_classes = [IsAuthenticated, IsYourTask]
    serializer = TaskSerializer

    def patch(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.completed == True:
            return Response({"status": "Already Completed."})
        else: 
            task.completed = True
        task.save()
        return Response({"status": "Completed."})
