from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.db.models import Avg
from .models import Book
from .serializers import BookSerializer, BookCreateSerializer, BookListSerializer
import requests
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import json
from datetime import datetime

# CRUD Views using Django REST Framework
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCreateSerializer
        return BookListSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        author = self.request.query_params.get('author')
        rating = self.request.query_params.get('rating')
        
        if author:
            queryset = queryset.filter(author__icontains=author)
        if rating:
            queryset = queryset.filter(rating=rating)
            
        return queryset

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# External API Integration - Google Books API
@api_view(['GET'])
def fetch_book_info(request, title):
    """
    Fetch book information from Google Books API and optionally save to database
    """
    try:
        # Clean the title for API search
        search_query = title.replace(' ', '+')
        google_books_url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults=1"
        
        response = requests.get(google_books_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('items'):
            return Response(
                {'error': 'No books found for the given title'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        book_data = data['items'][0]['volumeInfo']
        
        # Extract relevant information
        book_info = {
            'title': book_data.get('title', ''),
            'authors': book_data.get('authors', []),
            'published_date': book_data.get('publishedDate', ''),
            'description': book_data.get('description', ''),
            'page_count': book_data.get('pageCount'),
            'thumbnail': book_data.get('imageLinks', {}).get('thumbnail', ''),
            'isbn': None
        }
        
        # Extract ISBN
        industry_identifiers = book_data.get('industryIdentifiers', [])
        for identifier in industry_identifiers:
            if identifier['type'] in ['ISBN_13', 'ISBN_10']:
                book_info['isbn'] = identifier['identifier']
                break
        
        # Option to save to database
        save_to_db = request.query_params.get('save', 'false').lower() == 'true'
        
        if save_to_db:
            try:
                # Parse date
                pub_date = None
                if book_info['published_date']:
                    try:
                        if len(book_info['published_date']) == 4:  # Year only
                            pub_date = datetime.strptime(f"{book_info['published_date']}-01-01", "%Y-%m-%d").date()
                        else:
                            pub_date = datetime.strptime(book_info['published_date'], "%Y-%m-%d").date()
                    except ValueError:
                        pass
                
                if pub_date:
                    book_instance = Book.objects.create(
                        title=book_info['title'][:200],  # Truncate to fit model
                        author=', '.join(book_info['authors'])[:100] if book_info['authors'] else 'Unknown',
                        published_date=pub_date,
                        rating=4,  # Default rating
                        isbn=book_info['isbn'],
                        description=book_info['description'],
                        page_count=book_info['page_count'],
                        thumbnail_url=book_info['thumbnail']
                    )
                    
                    book_info['saved_to_db'] = True
                    book_info['db_id'] = book_instance.id
                else:
                    book_info['save_error'] = 'Invalid or missing published date'
                    
            except Exception as e:
                book_info['save_error'] = str(e)
        
        return Response(book_info, status=status.HTTP_200_OK)
        
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': f'Failed to fetch data from Google Books API: {str(e)}'}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        return Response(
            {'error': f'An unexpected error occurred: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Data Visualization and Reporting
@api_view(['GET'])
def books_report(request):
    """
    Generate a report with book statistics and visualization
    """
    try:
        # Get rating distribution
        rating_counts = Book.objects.values('rating').annotate(
            count=Count('rating')
        ).order_by('rating')
        
        # Get additional statistics
        total_books = Book.objects.count()
        avg_rating = Book.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Get top authors
        top_authors = Book.objects.values('author').annotate(
            book_count=Count('id')
        ).order_by('-book_count')[:5]
        
        report_data = {
            'total_books': total_books,
            'average_rating': round(avg_rating, 2),
            'rating_distribution': list(rating_counts),
            'top_authors': list(top_authors),
        }
        
        return Response(report_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to generate report: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def books_chart(request):
    """
    Generate a matplotlib chart showing rating distribution
    """
    try:
        # Get rating distribution
        rating_counts = Book.objects.values('rating').annotate(
            count=Count('rating')
        ).order_by('rating')
        
        if not rating_counts:
            return HttpResponse("No data available for chart generation", 
                              content_type="text/plain", status=404)
        
        # Prepare data for plotting
        ratings = [item['rating'] for item in rating_counts]
        counts = [item['count'] for item in rating_counts]
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        sns.set_style("whitegrid")
        
        # Create bar chart
        bars = plt.bar(ratings, counts, color='steelblue', alpha=0.7)
        
        # Customize the plot
        plt.title('Distribution of Books by Rating', fontsize=16, fontweight='bold')
        plt.xlabel('Rating (1-5 stars)', fontsize=12)
        plt.ylabel('Number of Books', fontsize=12)
        plt.xticks(range(1, 6))
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert plot to image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return HttpResponse(image_png, content_type='image/png')
        
    except Exception as e:
        plt.close()  # Ensure plot is closed in case of error
        return HttpResponse(f"Error generating chart: {str(e)}", 
                          content_type="text/plain", status=500)

# Frontend Views (using Django templates)
def dashboard_view(request):
    """
    Render a simple dashboard with books and charts
    """
    books = Book.objects.all()[:10]  # Get latest 10 books
    total_books = Book.objects.count()
    
    # Get rating distribution for frontend chart
    rating_counts = Book.objects.values('rating').annotate(
        count=Count('rating')
    ).order_by('rating')
    
    context = {
        'books': books,
        'total_books': total_books,
        'rating_data': json.dumps(list(rating_counts)),
    }
    
    return render(request, 'books/dashboard.html', context)
