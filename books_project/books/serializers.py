from rest_framework import serializers
from .models import Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    is_recent = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_recent')

    def validate_published_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return value

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class BookCreateSerializer(BookSerializer):
    """Serializer for creating books with required fields only"""
    class Meta(BookSerializer.Meta):
        fields = ['title', 'author', 'published_date', 'rating', 'isbn', 'description']

class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing books"""
    is_recent = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'rating', 'published_date', 'is_recent']
