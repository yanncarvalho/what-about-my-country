"""Django URLs path."""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .api.views import error_404, error_500, CountryViewVersionOne

handler404 = error_404
handler500 = error_500

urlpatterns = [
    path('api/v1/country', csrf_exempt(CountryViewVersionOne.as_view()), name = 'country api v1'),
]
