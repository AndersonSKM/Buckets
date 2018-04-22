from django.urls import include, path

urlpatterns = [
    path(
        'api/v1/auth/',
        include(('accounts.urls', 'accounts'), namespace='api')
    ),
]
