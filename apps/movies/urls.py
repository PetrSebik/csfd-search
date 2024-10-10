from django.urls import path
from apps.movies.views import SearchView, SearchTSGView
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/search/', permanent=True)),
    path('search/', SearchView.as_view(), name='search'),
    path('search/tgs/', SearchTSGView.as_view(), name='search_tgs'),
]
