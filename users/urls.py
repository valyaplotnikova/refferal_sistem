from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import SendAuthCode, VerifyAuthCode, ActivateInvitation, UsersViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/phone/', SendAuthCode.as_view()),
    path('auth/code/', VerifyAuthCode.as_view()),
    path('activate_invitation/', ActivateInvitation.as_view()),
    path('', include(router.urls)),
]
