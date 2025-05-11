# employee/api_urls.py
from django.urls import path
from .view_api import dashboard_api, mark_done_api, attendance_api, notice_api, notice_detail_api, assign_work_api,my_work_api,work_detail_api, make_request_api

urlpatterns = [
    path('dashboard/', dashboard_api, name='dashboard_api'),
    path('mark-done/<int:wid>/', mark_done_api, name='mark_done_api'),
    path('attendance/', attendance_api, name='attendance_api'),
    path('notices/', notice_api, name='notice_api'),
    path('notices/<int:id>/', notice_detail_api, name='notice_detail_api'),
    path('assign-work/', assign_work_api, name='assign_work_api'),
    path('my-work/', my_work_api, name='my_work_api'),
    path('work-details/<int:wid>/', work_detail_api, name='work_detail_api'),
    path('make-request/', make_request_api, name='make_request_api'),

]
