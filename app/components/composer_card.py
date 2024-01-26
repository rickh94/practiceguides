from django_components import component


@component.register("composer_card")
class ComposerCard(component.Component):
    template_name = "composer_card.html"

    def get_context_data(self, *_args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["composer"] = kwargs.get("composer")
        return context
