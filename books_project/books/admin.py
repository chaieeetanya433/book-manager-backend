from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'rating', 'published_date', 'created_at']
    list_filter = ['rating', 'published_date', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    list_per_page = 25
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'published_date', 'rating')
        }),
        ('Additional Details', {
            'fields': ('isbn', 'description', 'page_count', 'thumbnail_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']