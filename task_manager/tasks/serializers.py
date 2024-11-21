from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User

class ProjectSerializer (serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Project
        fields = '__all__'

    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'