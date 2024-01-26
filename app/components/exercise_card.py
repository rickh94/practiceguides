from django_components import component


@component.register("exercise_card")
class ExerciseCard(component.Component):
    template_name = "exercise_card.html"

    def get_context_data(self, *_args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exercise"] = kwargs.get("exercise")
        return context
