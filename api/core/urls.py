from django.conf import settings
from django.urls import path

from core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/health-check/', views.HeathCheckView.as_view(), name='health-check'),
]

if settings.DEBUG:
    urlpatterns += [
        path('api/seed/', views.SeedE2ETestsDataView.as_view(), name='seed-db'),
    ]
