# ADMIN PAGE URL

from django.urls import path, include
from . import views

from visualboard.api.apis import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register("info", UserViewSet)

app_name: str = "visualboard"
urlpatterns = [
    path("base/",      views.DashboardView.as_view(), name="base"),
    path("board/",     views.page_investigation_view, name="board"),
    path("api/",       include(router.urls)),
    
    path("register/",  views.AdminRegisterView.as_view(), name="register"),
    path("login/",     views.AdminLoginView.as_view(), name="login"),
    path("logout/",    views.logout_view, name="logout")
]

