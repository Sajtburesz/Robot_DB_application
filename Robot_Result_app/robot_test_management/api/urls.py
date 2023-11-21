from django.urls import path
from robot_test_management.api import views

urlpatterns = [
    # Create TestRun
    path('upload/', views.TestRunCreateView.as_view(), name='testrun_upload'),

    # Retreive Testrun nonPublic
    path('teams/<slug:teamId>/test-runs/',views.TestRunListView.as_view(), name="testrun-list"),
    path('teams/<int:teamId>/test-runs/<int:pk>/',views.TestRunRetreiveView.as_view(), name="testrun-instance"),
    path('teams/public/test-runs/<int:pk>/',views.TestRunRetreivePublicView.as_view(), name="testrun-instance-public"),

    path('teams/<slug:teamId>/test-runs/<int:testrunpk>/<int:pk>/',views.TestSuiteReteiveView.as_view(), name="suite-instance"),

    path('teams/<slug:teamId>/test-runs/<int:testrunpk>/<int:suitepk>/<int:pk>/',views.TestCaseRetreiveView.as_view(), name="testcase-instance"),

    # Attribute
    path('attributes/', views.AttributeListView.as_view(), name='attribute-list'),
    path('attributes/create/', views.AttributeCreateView.as_view(), name='attributes-list-create'),
    path('attributes/<int:pk>/', views.AttributeEditView.as_view(), name='attribute-key-edit'),

    # Comment nonPublic
    path('teams/<int:teamId>/test-runs/<int:testrunpk>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('teams/<int:teamId>/test-runs/<int:testrunpk>/comments/<int:pk>/', views.CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),

    # Statistics
    path('top-failing-testcases/<slug:teamId>/', views.TopFailingTestCasesView.as_view(), name='top-failing-tcs'),
    path('date-range/<slug:teamId>/', views.DateRangeView.as_view(), name='date-range'),
    path('treemap-data/<slug:teamId>/', views.TreemapDataView.as_view(), name='treemap-data'),
    path('timeline-data/<slug:teamId>/', views.TimelineDataView.as_view(), name='timeline-data'),
    path('duration-heatmap/<slug:teamId>/', views.TestCaseDurationHeatmapData.as_view(), name='testcase-duration-heatmap-data'),

    # Helper
    path('suite-names/<slug:teamId>/', views.SuiteNames.as_view(), name='suite-names'),

]