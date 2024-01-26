from django_components import component


@component.register("panel_header")
class PanelHeader(component.Component):
    template_name = "panel_header.html"

    def get_context_data(self, *_args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = kwargs.get("id")
        return context
