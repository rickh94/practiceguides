from django_components import component


@component.register("main")
class Main(component.Component):
    template_name = "main.html"
