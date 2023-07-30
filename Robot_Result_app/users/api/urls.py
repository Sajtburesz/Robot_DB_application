from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.api import views as uv

router = DefaultRouter()
router.register(r"profile",uv.UserViewSet,basename='current-user')


urlpatterns = [
    path("", include(router.urls)), 

    path("avatar/",
         uv.AvatarUpdateView.as_view(),
         name="avatar"),

]