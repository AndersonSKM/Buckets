from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

API_DOCS_URLS = include_docs_urls(
    title='API Documentation',
    permission_classes=(AllowAny,),
    public=True
)


urlpatterns = [
    path('', include(('core.urls', 'core'), namespace='core')),
    path('api/docs/', API_DOCS_URLS),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/', include(('djoser.urls.jwt', 'djoser'), namespace='auth')),
    path('api/accounts/', include(('djoser.urls', 'djoser'), namespace='accounts')),
]
