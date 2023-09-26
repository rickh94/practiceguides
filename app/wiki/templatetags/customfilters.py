from django import template
from django.db.models import QuerySet
from django.forms import BoundField
from django.template.base import Node
from django.utils.functional import keep_lazy
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


# type: ignore
@register.filter_function
def order_by(queryset: QuerySet, args: str) -> QuerySet:
    parsed_args = [x.strip() for x in args.split(",")]
    return queryset.order_by(*parsed_args)


@register.tag
def linebreakless(parser, token):
    nodelist = parser.parse(("endlinebreakless",))
    parser.delete_first_token()
    return LinebreaklessNode(nodelist)


class LinebreaklessNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        strip_line_breaks = keep_lazy(str)(lambda x: x.replace("\n", " "))
        strip_extra_space = keep_lazy(str)(lambda x: " ".join(x.split()))

        return strip_extra_space(
            strip_line_breaks(self.nodelist.render(context).strip())
        )
