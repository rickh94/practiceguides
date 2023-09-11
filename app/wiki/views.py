from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Book, Composer, Piece, Skill


def index(request: HttpRequest) -> HttpResponse:
    """Render the index page."""
    piece_list = Piece.objects.order_by("-created_at")[:5]
    composer_list = Composer.objects.order_by("-created_at")[:5]
    skill_list = Skill.objects.annotate(piece_count=Count("piece")).order_by(
        "-piece_count"
    )[:10]
    book_list = Book.objects.order_by("-created_at")[:5]
    return render(
        request,
        "wiki/index.html",
        {
            "piece_list": piece_list,
            "composer_list": composer_list,
            "skill_list": skill_list,
            "book_list": book_list,
        },
    )


class PieceDetailView(generic.DetailView[Piece]):
    model = Piece


class PieceListView(generic.ListView[Piece]):
    model = Piece


class SkillDetailView(generic.DetailView[Skill]):
    model = Skill


class SkillListView(generic.ListView[Skill]):
    model = Skill


class BookDetailView(generic.DetailView[Book]):
    model = Book


class BookListView(generic.ListView[Book]):
    model = Book


class ComposerDetailView(generic.DetailView[Composer]):
    model = Composer


class ComposerListView(generic.ListView[Composer]):
    model = Composer
