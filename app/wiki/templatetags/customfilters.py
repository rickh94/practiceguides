from django import template
from django.forms import BoundField
from django.utils.safestring import SafeString

register = template.Library()


@register.filter(name="addclass")
def addclass(value: BoundField, arg: str) -> SafeString:
    return value.as_widget(attrs={"class": arg})


@register.filter(name="icon_from_word")
def icon_from_word(value: str) -> str | None:
    if c := value[0]:
        return c.upper()
    return None
