from django.urls import path
from api.views import ProjectView, ProjectDetailView, TaskView, TaskDetailView, TaskCompleteView

urlpatterns = [
    # projects
    path('projects/', ProjectView.as_view()),
    path('projects/<int:pk>/', ProjectDetailView.as_view()),
    
    # tasks
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),

    # special api
    path('tasks/<int:pk>/complete/', TaskDetailView.as_view()),
]
