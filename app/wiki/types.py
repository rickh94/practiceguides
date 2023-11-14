from django.http import HttpRequest
from django.views import generic
from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


class HtmxView(generic.View):
    request: HtmxHttpRequest
