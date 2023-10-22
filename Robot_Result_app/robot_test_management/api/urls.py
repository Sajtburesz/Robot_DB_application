from django.urls import path
from robot_test_management.api.views import (AttributeCreateView, 
                                             AttributeEditView,
                                             AttributeListView, 
                                             CommentListCreateView, 
                                             CommentRetrieveUpdateDestroyView, 
                                             TestCaseRetreiveView, 
                                             TestRunRetreiveView, 
                                             TestRunListView, 
                                             TestRunCreateView,
                                             TestSuiteReteiveView)

urlpatterns = [
    # Create TestRun
    path('upload/', TestRunCreateView.as_view(), name='testrun_upload'),

    # Retreive Testrun
    path('teams/<int:teampk>/test-runs/',TestRunListView.as_view(), name="testrun-list"),
    path('teams/<int:teampk>/test-runs/<int:pk>/',TestRunRetreiveView.as_view(), name="testrun-instance"),

    path('teams/<int:teampk>/test-runs/<int:testrunpk>/<int:pk>/',TestSuiteReteiveView.as_view(), name="suite-instance"),

    path('teams/<int:teampk>/test-runs/<int:testrunpk>/<int:suitepk>/<int:pk>/',TestCaseRetreiveView.as_view(), name="testcase-instance"),

    # Attribute
    path('attributes/', AttributeListView.as_view(), name='attribute-list'),
    path('attributes/create/', AttributeCreateView.as_view(), name='attributes-list-create'),
    path('attributes/<int:pk>/', AttributeEditView.as_view(), name='attribute-key-edit'),

    # Comment
    path('teams/<int:teampk>/test-runs/<int:testrunpk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('teams/<int:teampk>/test-runs/<int:testrunpk>/comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
]