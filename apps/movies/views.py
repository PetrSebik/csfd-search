from django.views.generic import ListView, DetailView

from .forms import SearchForm
from .models import Movie, Actor
from .utils import remove_accents


class SearchView(ListView):
    template_name = 'search_results.html'
    form_class = SearchForm
    success_url = '/search/'
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        context = super().get_context_data(**kwargs)
        if query:
            normalized_query = remove_accents(query)
            context['movies'] = Movie.objects.filter(name__icontains=normalized_query).all()
            context['actors'] = Actor.objects.filter(name__icontains=normalized_query).all()
        context['search_form'] = SearchForm(initial=self.request.GET or None)
        return context


class MovieView(DetailView):
    template_name = "movie_detail.html"
    queryset = Movie.objects.prefetch_related('actors').all()


class ActorView(DetailView):
    template_name = "actor_detail.html"
    queryset = Actor.objects.prefetch_related('movies').all()

