from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from .util import truncate_words

# TODO: custom validator that makes sure steps and spot orders are unique and sequential


class Composer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("composer_detail", kwargs={"pk": self.pk})


class Book(models.Model):
    title = models.CharField(max_length=255)
    composer = models.ForeignKey(
        Composer, on_delete=models.CASCADE, related_name="books"
    )
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})


class Recording(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to="recordings/%Y-%m-%d/", validators=[FileExtensionValidator(["mp3"])]
    )

    def __str__(self):
        return self.name


def validate_positive(value):
    if value and value <= 0:
        raise ValidationError("Must be a positive number")


class Piece(models.Model):
    title = models.CharField(max_length=255)
    composer = models.ForeignKey(
        Composer,
        on_delete=models.SET_NULL,
        related_name="pieces",
        null=True,
        blank=True,
    )
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, related_name="pieces", blank=True
    )
    description = models.TextField(null=True, blank=True)
    practice_notes = models.TextField(null=True, blank=True)
    recording = models.ForeignKey(
        "Recording", on_delete=models.SET_NULL, null=True, related_name="+", blank=True
    )
    spotify_link = models.URLField(null=True, blank=True)
    apple_music_link = models.URLField(null=True, blank=True)
    amazon_music_link = models.URLField(null=True, blank=True)
    skills = models.ManyToManyField("Skill")
    large_sections = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True, validators=[validate_positive])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.composer:
            return f"{self.title} - {self.composer.name}"
        return f"{self.title} - Unknown"

    def get_absolute_url(self):
        return reverse("piece_detail", kwargs={"pk": self.pk})

    def clean(self):
        if not self.order and not self.book:
            return
        if self.order and not self.book:
            raise ValidationError("Order is meaningless without a book")
        orders = [p.order for p in self.book.pieces.all()]
        suggested_order = max(orders) + 1
        if self.book and not self.order:
            raise ValidationError(
                f"Pieces in a book must have an order. The next available is {suggested_order}."
            )
        if self.order in orders:
            raise ValidationError(
                f"Order {self.order} is taken, you must choose another. The next available is {suggested_order}."
            )
        super().clean()


class Spot(models.Model):
    nickname = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    measures = models.CharField(max_length=255, null=True, blank=True)
    skills = models.ManyToManyField("Skill")
    abc_notation = models.TextField(null=True, blank=True)
    recording = models.ForeignKey(
        "Recording", on_delete=models.CASCADE, null=True, blank=True
    )
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="spots")

    def __str__(self):
        if self.nickname:
            return f"{self.piece.title} - {self.nickname}"
        else:
            return f"{self.piece.title} - {self.measures or self.order}"

    def get_absolute_url(self):
        return reverse("spot_detail", kwargs={"pk": self.pk, "piece_id": self.piece.id})

    @property
    def display_name(self):
        return (
            f"{self.order}. {self.nickname}"
            or f"{self.order}. {self.measures}"
            or f"{self.piece.title} - {self.order}"
        )


class Step(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name="steps")
    order = models.IntegerField()
    instructions = models.TextField()
    abc_notation = models.TextField(null=True, blank=True)
    recording = models.ForeignKey(
        "Recording", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.spot} - Step {self.order}"

    @property
    def notes_id(self):
        return f"step{self.spot.piece.id}{self.spot.id}{self.pk}notes"


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    read_more_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("skill_detail", kwargs={"pk": self.pk})


class PieceExercise(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="exercises")
    nickname = models.CharField(max_length=255, null=True, blank=True)
    skills = models.ManyToManyField("Skill")
    description = models.TextField(null=True, blank=True)
    abc_notation = models.TextField(null=True, blank=True)
    instructions = models.TextField()
    recording = models.ForeignKey(
        "Recording", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        if self.nickname:
            return f"{self.piece.title} - {self.nickname}"
        else:
            return f"{self.piece.title} - {truncate_words(self.description)}"

    @property
    def notes_id(self):
        return f"exercise-{self.piece.id}-{self.pk}-notes"

    def get_absolute_url(self):
        return reverse(
            "pieceexercise_detail", kwargs={"pk": self.pk, "piece_id": self.piece.id}
        )

    @property
    def display_name(self):
        return self.nickname or truncate_words(self.description)


class StandaloneExercise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    practice_notes = models.TextField(null=True)
    composer = models.ForeignKey(
        Composer, on_delete=models.CASCADE, related_name="standaloneexercises"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="standaloneexercises",
    )
    recording = models.ForeignKey(
        "Recording", on_delete=models.CASCADE, null=True, blank=True, related_name="+"
    )
    skills = models.ManyToManyField("Skill")
    order = models.IntegerField(null=True, blank=True, validators=[validate_positive])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        composer = self.composer.name if self.composer else "Unknown"
        book = self.book.title if self.composer else "Unknown"
        return f"{self.title} - {book} - {composer}"

    def clean(self):
        if not self.order and not self.book:
            return
        if self.order and not self.book:
            raise ValidationError("Order is meaningless without a book")
        orders = [e.order for e in self.book.standaloneexercises.all()]
        suggested_order = max(orders) + 1
        if self.book and not self.order:
            raise ValidationError(
                f"Exercises in a book must have an order. The next available is {suggested_order}."
            )
        if self.order in orders:
            raise ValidationError(
                f"Order {self.order} is taken, you must choose another. The next available is {suggested_order}."
            )
        super().clean()

    def get_absolute_url(self):
        return reverse("standaloneexercise_detail", kwargs={"pk": self.pk})
