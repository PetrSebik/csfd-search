from django.urls import path
from apps.movies.views import SearchView, MovieView, ActorView
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/search/', permanent=True)),
    path('search/', SearchView.as_view(), name='search'),
    path('movie/<int:pk>/', MovieView.as_view(), name='movie_view'),
    path('actor/<int:pk>/', ActorView.as_view(), name='actor_view'),
]
