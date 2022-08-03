from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .api.views import error_404, error_500, CountryView


handler404 = error_404
handler500 = error_500

urlpatterns = [

    path('api/country',  csrf_exempt(CountryView.as_view()), name = 'countryapi'),
]



