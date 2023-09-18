from typing import Any

from django import forms
from django.db.models import Count, Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import (
    Book,
    Composer,
    Piece,
    PieceExercise,
    Skill,
    Spot,
    StandaloneExercise,
)


class SearchForm(forms.Form):
    q = forms.CharField(label="Search", max_length=255)


def index(request: HttpRequest) -> HttpResponse:
    """Render the index page."""
    piece_list = Piece.objects.order_by("-created_at")[:5]
    composer_list = Composer.objects.order_by("-created_at")[:5]
    skill_list = Skill.objects.annotate(piece_count=Count("piece")).order_by(
        "-piece_count"
    )[:10]
    book_list = Book.objects.order_by("-created_at")[:5]
    standaloneexercise_list = StandaloneExercise.objects.order_by("-created_at")[:5]
    return render(
        request,
        "wiki/index.html",
        {
            "piece_list": piece_list,
            "standaloneexercise_list": standaloneexercise_list,
            "composer_list": composer_list,
            "skill_list": skill_list,
            "book_list": book_list,
            "form": SearchForm(),
        },
    )


class PieceDetailView(generic.DetailView[Piece]):
    model = Piece


class PieceListView(generic.ListView[Piece]):
    model = Piece
    paginate_by = 20


class StandaloneExerciseDetailView(generic.DetailView[StandaloneExercise]):
    model = StandaloneExercise


class StandaloneExerciseListView(generic.ListView[StandaloneExercise]):
    model = StandaloneExercise
    paginate_by = 20


class SkillDetailView(generic.DetailView[Skill]):
    model = Skill


class SkillListView(generic.ListView[Skill]):
    model = Skill
    paginate_by = 50


class BookDetailView(generic.DetailView[Book]):
    model = Book


class BookListView(generic.ListView[Book]):
    model = Book


class ComposerDetailView(generic.DetailView[Composer]):
    model = Composer


class ComposerListView(generic.ListView[Composer]):
    model = Composer


class SpotDetailView(generic.DetailView[Spot]):
    model = Spot

    def get_queryset(self) -> QuerySet[Spot]:
        # type: ignore
        return Spot.objects.filter(piece_id=self.kwargs["piece_id"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["piece"] = self.object.piece
        # type: ignore
        context["steps"] = self.object.steps.order_by("order")
        context[
            "spot_notes_id"
        ] = f"spot-{self.object.piece.id}-{self.kwargs['pk']}-notes"
        return context


class SpotListView(generic.ListView[Spot]):
    model = Spot

    def get_queryset(self) -> QuerySet[Spot]:
        # type: ignore
        return Spot.objects.filter(piece_id=self.kwargs["piece_id"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["piece"] = Piece.objects.get(pk=self.kwargs["piece_id"])
        return context


class PieceExerciseDetailView(generic.DetailView[PieceExercise]):
    model = PieceExercise

    def get_queryset(self) -> QuerySet[PieceExercise]:
        # type: ignore
        return PieceExercise.objects.filter(piece_id=self.kwargs["piece_id"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["piece"] = self.object.piece
        # type: ignore
        context[
            "exercise_notes_id"
        ] = f"spot-{self.object.piece.id}-{self.kwargs['pk']}-notes"
        return context


class PieceExerciseListView(generic.ListView[PieceExercise]):
    model = PieceExercise

    def get_queryset(self) -> QuerySet[PieceExercise]:
        # type: ignore
        return PieceExercise.objects.filter(piece_id=self.kwargs["piece_id"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["piece"] = Piece.objects.get(pk=self.kwargs["piece_id"])
        return context


class SearchView(generic.TemplateView):
    template = "wiki/search.html"

    def get(self, request: HttpRequest, *_args: Any, **_kwargs: Any) -> HttpResponse:
        form = SearchForm()
        return render(request, self.template, {"form": form})

    def post(self, request: HttpRequest, *_args: Any, **_kwargs: Any) -> HttpResponse:
        context = {}
        form = SearchForm(request.POST)
        context["form"] = form
        if form.is_valid():
            q = form.cleaned_data["q"]
            context["piece_list"] = Piece.objects.filter(
                Q(title__icontains=q)
                | Q(skills__name__icontains=q)
                | Q(composer__name__icontains=q)
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

        return render(request, self.template, context)
