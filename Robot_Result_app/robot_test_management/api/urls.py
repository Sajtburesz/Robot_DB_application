from django.urls import path
from robot_test_management.api import views

urlpatterns = [
    # Create TestRun
    path('upload/', views.TestRunCreateView.as_view(), name='testrun_upload'),

    # Retreive Testrun nonPublic
    path('teams/<int:teampk>/test-runs/',views.TestRunListView.as_view(), name="testrun-list"),
    path('teams/<int:teampk>/test-runs/<int:pk>/',views.TestRunRetreiveView.as_view(), name="testrun-instance"),

    path('teams/<int:teampk>/test-runs/<int:testrunpk>/<int:pk>/',views.TestSuiteReteiveView.as_view(), name="suite-instance"),

    path('teams/<int:teampk>/test-runs/<int:testrunpk>/<int:suitepk>/<int:pk>/',views.TestCaseRetreiveView.as_view(), name="testcase-instance"),

    # Retreive Testrun Public
    path('teams/public/test-runs/',views.PublicTestRunListView.as_view(), name="testrun-list"),
    path('teams/public/test-runs/<int:pk>/',views.PublicTestRunRetreiveView.as_view(), name="testrun-instance"),

    path('teams/public/test-runs/<int:testrunpk>/<int:pk>/',views.PublicTestSuiteReteiveView.as_view(), name="suite-instance"),

    path('teams/public/test-runs/<int:testrunpk>/<int:suitepk>/<int:pk>/',views.PublicTestCaseRetreiveView.as_view(), name="testcase-instance"),

    # Attribute
    path('attributes/', views.AttributeListView.as_view(), name='attribute-list'),
    path('attributes/create/', views.AttributeCreateView.as_view(), name='attributes-list-create'),
    path('attributes/<int:pk>/', views.AttributeEditView.as_view(), name='attribute-key-edit'),

    # Comment nonPublic
    path('teams/<int:teampk>/test-runs/<int:testrunpk>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('teams/<int:teampk>/test-runs/<int:testrunpk>/comments/<int:pk>/', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),

    # Statistics
    path('top-failing-testcases/<int:teampk>/', views.TopFailingTestCasesView.as_view())

]