from django_components import component


@component.register("actors_list")
class ActorsList(component.Component):
    template_name = "actors_list/actors_list.html"

