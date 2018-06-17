from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework import routers

API_DOCS_TITLE = 'Buckets API'

urlpatterns = [
    path('api/docs/', include_docs_urls(title=API_DOCS_TITLE, public=True)),
    path('api/', include(('accounts.urls', 'accounts'), namespace='auth')),
]
