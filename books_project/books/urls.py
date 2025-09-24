from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('api/books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('api/fetch-book-info/<str:title>/', views.fetch_book_info, name='fetch-book-info'),
    path('api/report/', views.books_report, name='books-report'),
    path('api/chart/', views.books_chart, name='books-chart'),
    
    # Frontend views
    path('', views.dashboard_view, name='dashboard'),
]