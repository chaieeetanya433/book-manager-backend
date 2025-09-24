from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def is_recent(self):
        return self.published_date >= date(2020, 1, 1)