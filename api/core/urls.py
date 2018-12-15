from django.urls import path

from core.views import HeathCheckView

urlpatterns = [
    path('health-check/', HeathCheckView.as_view(), name='health-check'),
]
