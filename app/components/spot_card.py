from django_components import component


@component.register("spot_card")
class SpotCard(component.Component):
    template_name = "spot_card.html"

    def get_context_data(self, *_args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spot"] = kwargs.get("spot")
        context["hx"] = kwargs.get("hx", True)
        return context
