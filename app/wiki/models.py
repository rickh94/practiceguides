from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Composer(models.Model):
    name = models.CharField(max_length=255)
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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})


class Recording(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to="recordings", validators=[FileExtensionValidator(["mp3"])]
    )

    def __str__(self):
        return self.name


class Piece(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    practice_notes = models.TextField(null=True, blank=True)
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
    recording = models.ForeignKey(
        "Recording", on_delete=models.SET_NULL, null=True, related_name="+", blank=True
    )
    large_sections = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField("Skill")
    order = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.composer.name}"

    def get_absolute_url(self):
        return reverse("piece_detail", kwargs={"pk": self.pk})


class Spot(models.Model):
    recording = models.ForeignKey(
        "Recording", on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    piece = models.ForeignKey(
        Piece, on_delete=models.CASCADE, related_name="spots")
    measures = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    abc_notation = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField("Skill")

    def __str__(self):
        return f"{self.piece.title} - {self.measures or self.order}"


class Step(models.Model):
    order = models.IntegerField()
    abc_notation = models.TextField(null=True)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    instructions = models.TextField()
    recording = models.ForeignKey(
        "Recording", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.spot} - Step {self.order}"


class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("skill_detail", kwargs={"pk": self.pk})


class PieceExercise(models.Model):
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    skills = models.ManyToManyField("Skill")
    description = models.TextField(null=True, blank=True)
    abc_notation = models.TextField(null=True, blank=True)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.piece.title} - {self.description}"


class StandaloneExercise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    practice_notes = models.TextField(null=True)
    recording = models.ForeignKey(
        "Recording", on_delete=models.CASCADE, null=True)
    composer = models.ForeignKey(
        Composer, on_delete=models.CASCADE, related_name="exercises"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=True, related_name="exercises"
    )
    recording = models.ForeignKey(
        "Recording", on_delete=models.CASCADE, null=True, related_name="+"
    )
    skills = models.ManyToManyField("Skill")
    order = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.book} - {self.composer}"
