from django_components import component


@component.register("search_form")
class SearchForm(component.Component):
    template_name = "search_form/search_form.html"

