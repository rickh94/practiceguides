from django_components import component


@component.register("skill_card")
class SkillCard(component.Component):
    template_name = "skill_card.html"

    def get_context_data(self, *_args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["skill"] = kwargs.get("skill")
        context["small"] = kwargs.get("small", False)
        return context
