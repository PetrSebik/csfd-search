from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import F
from django.db.models import Q
from django.views.generic import ListView

from .forms import SearchForm
from .models import Movie, Unaccent


class SearchView(ListView):
    template_name = 'search_results.html'
    form_class = SearchForm
    success_url = '/search/'
    queryset = Movie.objects.prefetch_related('actors').all()
    context_object_name = "movies"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = (queryset.annotate(
                movie_name_unaccent=Unaccent(F('name')),
                actor_name_unaccent=Unaccent(F('actors__name')))
                        .filter(Q(movie_name_unaccent__icontains=query) |
                                Q(actor_name_unaccent__icontains=query))
                        .distinct('id'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(initial=self.request.GET or None)
        return context


class SearchTSGView(ListView):
    template_name = 'search_results_tgs.html'
    form_class = SearchForm
    success_url = '/search/tgs/'
    queryset = Movie.objects.prefetch_related('actors').all()
    context_object_name = "movies"
    TGS = 0.3

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = (queryset.annotate(
                movie_similarity=TrigramSimilarity(Unaccent(F('name')), query),
                actor_similarity=TrigramSimilarity(Unaccent(F('actors__name')), query))
                        .filter(Q(movie_similarity__gt=self.TGS) | Q(actor_similarity__gt=self.TGS))
                        .annotate(total_similarity=F('movie_similarity') + F('actor_similarity'))
                        .order_by('id', '-total_similarity')
                        .distinct('id'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(initial=self.request.GET or None)
        return context
