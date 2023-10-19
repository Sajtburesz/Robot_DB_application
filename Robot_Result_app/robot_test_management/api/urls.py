from django.urls import path
from robot_test_management.api.views import AttributeEditView,AttributeListView, TestRunListView, TestRunUploadView

urlpatterns = [
    path('upload/', TestRunUploadView.as_view(), name='testrun_upload'),
    path('test-runs/',TestRunListView.as_view(), name="testrun-list"),
    path('attributes/', AttributeListView.as_view(), name='attributes_list_create'),
    path('attributes/<int:pk>/', AttributeEditView.as_view(), name='attribute_key_edit'),
]