from django.shortcuts import render
from django.urls import include, path
from django.views.decorators.cache import never_cache
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

API_DOCS_URLS = include_docs_urls(
    title='API Documentation',
    permission_classes=(AllowAny,),
    public=True
)


@never_cache
def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('', index, name='index'),
    path('api/docs/', API_DOCS_URLS),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(('core.urls', 'core'), namespace='core')),
    path('api/', include(('accounts.urls', 'accounts'), namespace='accounts')),
]
