from django.urls import path
from apps.movies.views import SearchView, SearchTSGView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('search/tgs/', SearchTSGView.as_view(), name='search_tgs'),
]
