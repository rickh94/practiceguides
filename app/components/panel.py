from django_components import component


@component.register("panel")
class Panel(component.Component):
    template_name = "panel.html"

    def get_context_data(self, *_args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = kwargs.get("id")
        return context
