# employee/api_views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from employee.models import workAssignments
from employee.models import Employee, Attendance, Notice
from employee.serializers import EmployeeSerializer,AttendanceSerializer, NoticeSerializer, WorkAssignmentsSerializer, RequestSerializer


from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    current_id = request.user.username

    if current_id == "123123":  # директор
        query = request.GET.get('q', '')
        if query:
            employees = Employee.objects.filter(
                Q(firstName__icontains=query) |
                Q(lastName__icontains=query) |
                Q(middleName__icontains=query) |
                Q(designation__icontains=query)
            )
        else:
            employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response({'employees': serializer.data})

    else:
        try:
            employee = Employee.objects.get(eID=current_id)
            serializer = EmployeeSerializer(employee)
            return Response({'employee': serializer.data})
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_done_api(request, wid):
    work = get_object_or_404(workAssignments, id=wid)

    if work.taskerId.eID == request.user.username:
        work.isDone = True
        work.save()
        return Response({"message": "Marked as done."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "You cannot mark this task."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_api(request):
    attendance_records = Attendance.objects.filter(eId=request.user.username)
    serializer = AttendanceSerializer(attendance_records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notice_api(request):
    notices = Notice.objects.all()
    serializer = NoticeSerializer(notices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notice_detail_api(request, id):
    notice = get_object_or_404(Notice, Id=id)  # `Id` with capital I as per your original model field
    serializer = NoticeSerializer(notice)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_work_api(request):
    data = request.data.copy()
    data['assignerId'] = request.user.username

    if data.get('taskerId') == request.user.username:
        return Response({'error': 'You cannot assign work to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = WorkAssignmentsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Work assigned successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_work_api(request):
    work = workAssignments.objects.filter(taskerId=request.user.username)
    serializer = WorkAssignmentsSerializer(work, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def work_detail_api(request, wid):
    work = get_object_or_404(workAssignments, id=wid)

    # Optional: Ensure only assigned user or assigner can access
    if request.user.username not in [work.taskerId, work.assignerId]:
        return Response({'error': 'Not authorized to view this task.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = WorkAssignmentsSerializer(work)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_request_api(request):
    data = request.data.copy()
    data['requesterId'] = request.user.username  # Set the requesterId from the logged-in user

    current_requester_id = data.get('destinationEmployeeId')
    current_user_id = request.user.username

    if current_requester_id == current_user_id:
        return Response({'error': 'Invalid ID Selected. You cannot request yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Request Submitted Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Form is invalid. Please check your inputs.', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)