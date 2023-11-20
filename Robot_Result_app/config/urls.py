"""
URL configuration for Robot_Result_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from django_registration.backends.one_step.views import RegistrationView

from users.forms import UserForm
from core.views import IndexTemplateView

from django.contrib.auth.views import LoginView, LogoutView
from users.api.views import GetSelfUsernameView,ManageAdminRightsAPIView,ResetPasswordView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    # TODO: Only include usrs/set_password!!
    path("auth/", include("djoser.urls.authtoken")),
    
    path('auth/users/me/', GetSelfUsernameView.as_view(), name='logged-in-user-username'),
    path(
        "accounts/register/",
        RegistrationView.as_view(
            form_class=UserForm,
            success_url="/",
        ),
        name="django_registration_register",
    ),

    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),

    path("api/v1/", include("users.api.urls")),
    path("api/v1/", include("robot_test_management.api.urls")),
    path("api/v1/", include("teams.api.urls")),

    # admin
    path('admin/reset-password/',ResetPasswordView.as_view(),name='reset-password-of-user'),
    path('admin/manage-admin/',ManageAdminRightsAPIView.as_view(),name='manage-admin-users'),

    # doc
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Keep it as last url entry
    re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point"),
]

from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
