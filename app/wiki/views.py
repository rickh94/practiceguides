from typing import Any

from django import forms
from django.db.models import Count, Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from wiki.types import HtmxHttpRequest, HtmxView

from .models import (
    Book,
    Composer,
    GoLink,
    Piece,
    PieceExercise,
    Skill,
    Spot,
    StandaloneExercise,
)

# just enough caching to allow preload to work
decorators = [
    vary_on_headers("HX-Request"),
    cache_control(max_age=60),
]


class SearchForm(forms.Form):
    q = forms.CharField(
        label="Search",
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Type to search…"}),
    )


@cache_control(max_age=60 * 5)
@vary_on_headers("HX-Request")
def index(request: HtmxHttpRequest) -> HttpResponse:
    """Render the index page."""
    piece_list = Piece.objects.order_by("-created_at")[:5]
    composer_list = Composer.objects.order_by("-created_at")[:5]
    skill_list = Skill.objects.annotate(piece_count=Count("piece")).order_by(
        "-piece_count"
    )[:10]
    book_list = Book.objects.order_by("-created_at")[:5]
    standaloneexercise_list = StandaloneExercise.objects.order_by("-created_at")[:5]
    template_name = (
        "wiki/htmx/index.html"
        if request.htmx and not request.htmx.boosted
        else "wiki/index.html"
    )
    return render(
        request,
        template_name,
        {
            "piece_list": piece_list,
            "standaloneexercise_list": standaloneexercise_list,
            "composer_list": composer_list,
            "skill_list": skill_list,
            "book_list": book_list,
            "form": SearchForm(),
        },
    )


@method_decorator(decorators, name="dispatch")
class PieceDetailView(HtmxView, generic.DetailView[Piece]):
    model = Piece

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/piece_detail.html"]
        else:
            return ["wiki/piece_detail.html"]


def piece_export(_request: HttpRequest, pk: int) -> JsonResponse:
    piece = Piece.objects.get(pk=pk)
    return JsonResponse(piece.to_dict())


@method_decorator(decorators, name="dispatch")
class PieceListView(HtmxView, generic.ListView[Piece]):
    model = Piece
    paginate_by = 20

    def get_queryset(self) -> QuerySet[Piece]:
        return Piece.objects.order_by("-created_at")

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/piece_list.html"]
        else:
            return ["wiki/piece_list.html"]


@method_decorator(decorators, name="dispatch")
class StandaloneExerciseDetailView(HtmxView, generic.DetailView[StandaloneExercise]):
    model = StandaloneExercise

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/standaloneexercise_detail.html"]
        else:
            return ["wiki/standaloneexercise_detail.html"]


@method_decorator(decorators, name="dispatch")
class StandaloneExerciseListView(HtmxView, generic.ListView[StandaloneExercise]):
    model = StandaloneExercise
    paginate_by = 20

    def get_queryset(self) -> QuerySet[StandaloneExercise]:
        return StandaloneExercise.objects.order_by("-created_at")

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/standaloneexercise_list.html"]
        else:
            return ["wiki/standaloneexercise_list.html"]


@method_decorator(decorators, name="dispatch")
class SkillDetailView(HtmxView, generic.DetailView[Skill]):
    model = Skill

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/skill_detail.html"]
        else:
            return ["wiki/skill_detail.html"]


@method_decorator(decorators, name="dispatch")
class SkillListView(HtmxView, generic.ListView[Skill]):
    model = Skill
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Skill]:
        return Skill.objects.order_by("name")

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/skill_list.html"]
        else:
            return ["wiki/skill_list.html"]


@method_decorator(decorators, name="dispatch")
class BookDetailView(HtmxView, generic.DetailView[Book]):
    model = Book

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/book_detail.html"]
        else:
            return ["wiki/book_detail.html"]


@method_decorator(decorators, name="dispatch")
class BookListView(HtmxView, generic.ListView[Book]):
    model = Book
    paginate_by = 20

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/book_list.html"]
        else:
            return ["wiki/book_list.html"]


@method_decorator(decorators, name="dispatch")
class ComposerDetailView(HtmxView, generic.DetailView[Composer]):
    model = Composer

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/composer_detail.html"]
        else:
            return ["wiki/composer_detail.html"]


@method_decorator(decorators, name="dispatch")
class ComposerListView(HtmxView, generic.ListView[Composer]):
    model = Composer
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Composer]:
        return Composer.objects.order_by("name")

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/composer_list.html"]
        else:
            return ["wiki/composer_list.html"]


@method_decorator(decorators, name="dispatch")
class SpotDetailView(HtmxView, generic.DetailView[Spot]):
    model = Spot

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/spot_detail.html"]
        else:
            return ["wiki/spot_detail.html"]

    def get_queryset(self) -> QuerySet[Spot]:
        return Spot.objects.filter(piece_id=self.kwargs["piece_id"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["piece"] = self.object.piece
        # type: ignore
        context["spot_notes_id"] = f"spot{self.object.piece.id}{self.kwargs['pk']}notes"
        return context


@method_decorator(decorators, name="dispatch")
class PieceExerciseDetailView(HtmxView, generic.DetailView[PieceExercise]):
    model = PieceExercise

    def get_queryset(self) -> QuerySet[PieceExercise]:
        # type: ignore
        return PieceExercise.objects.filter(piece_id=self.kwargs["piece_id"])

    def get_template_names(self) -> list[str]:
        if self.request.htmx and not self.request.htmx.boosted:
            return ["wiki/htmx/pieceexercise_detail.html"]
        else:
            return ["wiki/pieceexercise_detail.html"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["piece"] = self.object.piece
        # type: ignore
        context[
            "exercise_notes_id"
        ] = f"exercise{self.object.piece.id}{self.kwargs['pk']}notes"
        return context


@method_decorator(decorators, name="get")
class SearchView(HtmxView, generic.TemplateView):
    @property
    def template_name(self) -> str:
        if self.request.htmx and not self.request.htmx.boosted:
            if self.request.method == "POST":
                return "wiki/htmx/search_results.html"
            else:
                return "wiki/htmx/search_full.html"
        else:
            return "wiki/search.html"

    def get(self, request: HttpRequest, *_args: Any, **_kwargs: Any) -> HttpResponse:
        form = SearchForm()
        return render(request, self.template_name, {"form": form})

    def post(
        self, request: HtmxHttpRequest, *_args: Any, **_kwargs: Any
    ) -> HttpResponse:
        context = {}
        form = SearchForm(request.POST)
        context["form"] = form
        if form.is_valid():
            q = form.cleaned_data["q"]
            context["q"] = q
            context["piece_list"] = Piece.objects.filter(
                Q(title__icontains=q)
                | Q(skills__name__icontains=q)
                | Q(composer__name__icontains=q)
                | Q(spots__nickname__icontains=q)
            ).distinct()
            context["standaloneexercise_list"] = StandaloneExercise.objects.filter(
                Q(title__icontains=q)
                | Q(skills__name__icontains=q)
                | Q(composer__name__icontains=q)
            ).distinct()
            context["skill_list"] = Skill.objects.filter(name__icontains=q).distinct()
            context["composer_list"] = Composer.objects.filter(
                name__icontains=q
            ).distinct()
            context["book_list"] = Book.objects.filter(
                Q(title__icontains=q) | Q(composer__name__icontains=q)
            ).distinct()

        return render(request, self.template_name, context)


def not_found(request: HtmxHttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    return render(request, "404.html", status=404)


def go(_request: HtmxHttpRequest, *_args: Any, **kwargs: Any) -> HttpResponse:
    golink = GoLink.objects.get(slug=kwargs["slug"])
    return redirect(golink.endpoint)
