from django_components import component


@component.register("book_card")
class BookCard(component.Component):
    template_name = "book_card.html"

    def get_context_data(self, *_args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = kwargs.get("book")
        context["icon"] = kwargs.get("icon", True)
        context["abbreviated"] = kwargs.get("abbreviated", False)
        return context
