from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from accounts import views

router = DefaultRouter()
router.register('users', views.UserViewSet, base_name='users')

urlpatterns = [
    path('token/', obtain_jwt_token, name='obtain-token')
]

urlpatterns += router.urls
