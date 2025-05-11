from rest_framework import serializers
from .models import Employee

from rest_framework import serializers
from .models import Employee, Attendance, Notice, workAssignments

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

class WorkAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = workAssignments
        fields = '__all__'
# serializers.py
from .models import Requests

# serializers.py
from rest_framework import serializers
from .models import Requests


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = [ 'requesterId', 'requestMessage', 'requestDate', 'destinationEmployeeId']

    # Optional: Customize foreign key fields if needed
    requesterId = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    destinationEmployeeId = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
