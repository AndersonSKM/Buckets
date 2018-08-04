from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

API_DOCS_URLS = include_docs_urls(
    title='Buckets API',
    permission_classes=(AllowAny,),
    public=True
)

urlpatterns = [
    path('api/docs/', API_DOCS_URLS),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(('core.urls', 'core'), namespace='core')),
    path('api/', include(('accounts.urls', 'accounts'), namespace='auth')),
]
