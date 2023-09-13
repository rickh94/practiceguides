from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pieces/<int:pk>", views.PieceDetailView.as_view(), name="piece_detail"),
    path("pieces", views.PieceListView.as_view(), name="piece_list"),
    path("skills/<int:pk>", views.SkillDetailView.as_view(), name="skill_detail"),
    path("skills", views.SkillListView.as_view(), name="skill_list"),
    path("books/<int:pk>", views.BookDetailView.as_view(), name="book_detail"),
    path("books", views.BookListView.as_view(), name="book_list"),
    path(
        "composers/<int:pk>", views.ComposerDetailView.as_view(), name="composer_detail"
    ),
    path("composers", views.ComposerListView.as_view(), name="composer_list"),
    path("pieces/<int:piece_id>/spots",
         views.SpotListView.as_view(), name="spot_list"),
    path(
        "pieces/<int:piece_id>/spots/<int:pk>",
        views.SpotDetailView.as_view(),
        name="spot_detail",
    ),
]
