from typing import Dict, Any
from django_components import component  # type: ignore


@component.register("card")
class Card(component.Component):
    template_name = "card/card.html"

    # def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
    #     return {
    #         "args": args,
    #         "kwargs": kwargs,
    #     }
