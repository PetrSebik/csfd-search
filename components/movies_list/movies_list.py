from django_components import component


@component.register("movies_list")
class MoviesList(component.Component):
    template_name = "movies_list/movies_list.html"

