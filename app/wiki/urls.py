from django.conf import settings
from django.urls import path

from . import views

debug_patterns = [
    path("404/", views.not_found, name="404"),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("pieces/<int:pk>", views.PieceDetailView.as_view(), name="piece_detail"),
    path("pieces/<int:pk>/export", views.piece_export, name="piece_export"),
    path("pieces", views.PieceListView.as_view(), name="piece_list"),
    # path(
    #     "etudes/<int:pk>",
    #     views.StandaloneExerciseDetailView.as_view(),
    #     name="standaloneexercise_detail",
    # ),
    # path(
    #     "etudes",
    #     views.StandaloneExerciseListView.as_view(),
    #     name="standaloneexercise_list",
    # ),
    # path("skills/<int:pk>", views.SkillDetailView.as_view(), name="skill_detail"),
    # path("skills", views.SkillListView.as_view(), name="skill_list"),
    path("books/<int:pk>", views.BookDetailView.as_view(), name="book_detail"),
    path("books", views.BookListView.as_view(), name="book_list"),
    path(
        "composers/<int:pk>", views.ComposerDetailView.as_view(), name="composer_detail"
    ),
    path("composers", views.ComposerListView.as_view(), name="composer_list"),
    path(
        "pieces/<int:piece_id>/spots/<int:pk>",
        views.SpotDetailView.as_view(),
        name="spot_detail",
    ),
    path(
        "pieces/<int:piece_id>/exercises/<int:pk>",
        views.PieceExerciseDetailView.as_view(),
        name="pieceexercise_detail",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
    path("go/<slug:slug>", views.go, name="go"),
]

if settings.DEBUG:
    urlpatterns += debug_patterns
