from django.urls import path
from robot_test_management.api.views import UploadRobotOutputView

urlpatterns = [
    path('upload/', UploadRobotOutputView.as_view(), name='upload_robot_output'),
]