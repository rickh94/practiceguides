from django_components import component


@component.register("piece_card")
class PieceCard(component.Component):
    template_name = "piece_card.html"

    def get_context_data(self, *_args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["piece"] = kwargs.get("piece")
        return context
