from .models import Project, Task
import django_filters

class ProjectFilter(django_filters.FilterSet):
    project = django_filters.NumberFilter(field_name='id', lookup_expr='exact')

    class Meta:
        model = Project
        fields = ['project']

class TaskFilter(django_filters.FilterSet):
    due_date = django_filters.DateFilter(field_name="due_date", lookup_expr='exact')
    completed = django_filters.BooleanFilter(field_name="completed",)
    class Meta:
        model = Task
        fields = ['due_date', 'completed']
