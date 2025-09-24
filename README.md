# 📚 Django Books CRUD API + React (Vite) Frontend

![App Cover](./cover.webp)

A full-stack application built with **Django + PostgreSQL** (backend) and **React (Vite + Tailwind)** (frontend).  
It demonstrates REST API design, database operations, third-party API integration, and a modern dashboard interface.

---

## 🚀 Features

### Backend (Django + PostgreSQL)
- **Complete CRUD Operations** - Create, Read, Update, Delete books via REST APIs  
- **PostgreSQL Integration** - Full database support with migrations  
- **Google Books API Integration** - Fetch book data from external APIs  
- **Analytics & Reporting** - Statistics endpoints + rating distribution chart (PNG)  
- **Django Admin Panel** - Manage data easily  
- **Docker Support** - Easy containerization and deployment  

### Frontend (React + Vite + Tailwind)
- **Modern UI** with TailwindCSS and Framer Motion animations  
- **Dashboard** with stats cards, rating distribution charts (Recharts), and top authors  
- **Google Books Search** with debounce + add to collection directly  
- **Books Collection Management** - List, add, edit, delete with confirmation modal  
- **React Query** for data fetching & cache management  
- **Responsive Layout** with Sidebar + Navbar  

---

## 🛠️ Tech Stack

- **Backend**: Django 4.2 + Django REST Framework  
- **Database**: PostgreSQL (Local or Supabase)  
- **Frontend**: React 19 + Vite 7 + TailwindCSS 4  
- **State/Data**: React Query 5  
- **Animations**: Framer Motion  
- **Icons**: Lucide React  
- **Charts**: Recharts  
- **API Integration**: Google Books API  

---

## 📋 Requirements

- Python 3.8+  
- PostgreSQL 12+ (or Supabase)  
- Node.js 18+  
- npm / pnpm / yarn  

---

## ⚡ Quick Start

### 1. Clone & Setup

```bash
# Clone the project
git clone <repository-url>
cd books_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

#### Option A: Local PostgreSQL
```bash
# Install PostgreSQL and create database
createdb books_db
```

#### Option B: Supabase (Cloud)
1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Copy database credentials from Settings > Database

#### Option C: Docker (Easiest)
```bash
docker-compose up -d db
```

### 3. Environment Configuration

Create `.env` file in project root:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Local PostgreSQL)
DB_NAME=books_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Database (Supabase)
# DB_NAME=postgres
# DB_USER=postgres.your-ref
# DB_PASSWORD=your-supabase-password
# DB_HOST=db.your-ref.supabase.co
# DB_PORT=5432
```

### 4. Initialize Database

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Populate with sample data
python manage.py populate_sample_data --count 20

# Collect static files
python manage.py collectstatic --noinput
```

### 5. Run the Server

```bash
python manage.py runserver
```

🎉 **Your app is now running!**

- **Dashboard**: http://127.0.0.1:8000/
- **API Docs**: http://127.0.0.1:8000/api/books/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Frontend**: http://127:0.0.1:5173

## 📡 API Endpoints

### Books CRUD Operations

| Method | Endpoint | Description | Example |
|--------|----------|-------------|---------|
| `GET` | `/api/books/` | List all books | `curl http://127.0.0.1:8000/api/books/` |
| `POST` | `/api/books/` | Create new book | See example below |
| `GET` | `/api/books/{id}/` | Get book by ID | `curl http://127.0.0.1:8000/api/books/1/` |
| `PUT` | `/api/books/{id}/` | Update book | See example below |
| `DELETE` | `/api/books/{id}/` | Delete book | `curl -X DELETE http://127.0.0.1:8000/api/books/1/` |

### Special Features

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/fetch-book-info/{title}/` | Fetch from Google Books API |
| `GET` | `/api/report/` | Get analytics report (JSON) |
| `GET` | `/api/chart/` | Get rating distribution chart (PNG) |

### Query Parameters

**Filter books:**
```bash
# Filter by author
curl "http://127.0.0.1:8000/api/books/?author=tolkien"

# Filter by rating
curl "http://127.0.0.1:8000/api/books/?rating=5"
```

## 📝 API Usage Examples

### Create a New Book

```bash
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "published_date": "1925-04-10",
    "rating": 5,
    "description": "A classic American novel"
  }'
```

### Update a Book

```bash
curl -X PUT http://127.0.0.1:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby (Updated)",
    "author": "F. Scott Fitzgerald",
    "published_date": "1925-04-10",
    "rating": 5
  }'
```

### Fetch Book from Google Books API

```bash
# Just fetch information
curl "http://127.0.0.1:8000/api/fetch-book-info/The Great Gatsby/"

# Fetch and save to database
curl "http://127.0.0.1:8000/api/fetch-book-info/The Great Gatsby/?save=true"
```

### Get Analytics Report

```bash
curl http://127.0.0.1:8000/api/report/
```

**Response:**
```json
{
  "total_books": 25,
  "average_rating": 4.2,
  "rating_distribution": [
    {"rating": 1, "count": 2},
    {"rating": 2, "count": 3},
    {"rating": 3, "count": 5},
    {"rating": 4, "count": 8},
    {"rating": 5, "count": 7}
  ],
  "top_authors": [
    {"author": "J.R.R. Tolkien", "book_count": 3},
    {"author": "George Orwell", "book_count": 2}
  ]
}
```

## 🎨 Data Visualization

### Server-Side Chart (Matplotlib)
Visit `http://127.0.0.1:8000/api/chart/` to get a PNG chart showing rating distribution.

### Client-Side Dashboard
The main dashboard at `http://127.0.0.1:8000/` includes:
- Interactive Chart.js visualizations
- Real-time book statistics
- API testing interface
- Book management forms

## 🧪 Testing

### Run Unit Tests
```bash
python manage.py test
```

### Test Google Books API Integration
```bash
# Test API without saving
python manage.py test_google_books_api "The Great Gatsby"

# Test API and save to database
python manage.py test_google_books_api "1984" --save
```

### Manual API Testing
Use the built-in dashboard at `http://127.0.0.1:8000/` for interactive testing, or use tools like:
- **Postman** - Import the API collection
- **curl** - Command line testing (examples above)
- **Django REST Framework browser** - Visit API endpoints directly


## 📊 Database Schema

### Book Model
```python
class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Indexes and Constraints
- Indexed fields: `title`, `author`, `rating`
- Unique constraint: `isbn`
- Rating validation: 1-5 stars only
- Automatic timestamps: `created_at`, `updated_at`

## 🌐 External API Integration

### Google Books API
The application integrates with Google Books API to fetch book information:

**Features:**
- Search books by title
- Automatic data extraction (title, author, ISBN, description, etc.)
- Optional database saving
- Error handling and validation

**Usage:**
```bash
GET /api/fetch-book-info/The Great Gatsby/?save=true
```

**Response:**
```json
{
  "title": "The Great Gatsby",
  "authors": ["F. Scott Fitzgerald"],
  "published_date": "1925-04-10",
  "description": "The story of the mysteriously wealthy Jay Gatsby...",
  "page_count": 180,
  "isbn": "9780743273565",
  "thumbnail": "http://books.google.com/...",
  "saved_to_db": true,
  "db_id": 15
}
```

## ⚙️ Configuration

### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | - | ✅ |
| `DEBUG` | Debug mode | `False` | ❌ |
| `DB_NAME` | Database name | `books_db` | ✅ |
| `DB_USER` | Database user | `postgres` | ✅ |
| `DB_PASSWORD` | Database password | - | ✅ |
| `DB_HOST` | Database host | `localhost` | ✅ |
| `DB_PORT` | Database port | `5432` | ✅ |

### Django Settings
Key configurations in `settings.py`:
- **CORS enabled** for frontend integration
- **Pagination** set to 20 items per page
- **Static files** configuration for production
- **Database indexing** for performance
- **REST Framework** browsable API enabled

## 🔒 Security Considerations

### Production Deployment
1. **Environment Variables**: Never commit `.env` files
2. **Secret Key**: Generate a new secret key for production
3. **Debug Mode**: Set `DEBUG=False` in production
4. **Allowed Hosts**: Configure proper `ALLOWED_HOSTS`
5. **Database Security**: Use strong passwords and SSL connections
6. **CORS**: Configure specific origins instead of `CORS_ALLOW_ALL_ORIGINS`

### API Security
- CSRF protection enabled
- Input validation on all endpoints
- SQL injection prevention (Django ORM)
- Rate limiting ready (can be added with django-ratelimit)

## 📈 Performance Optimizations

### Database
- **Indexes** on frequently queried fields (`title`, `author`, `rating`)
- **Pagination** to handle large datasets
- **Select related** for efficient queries
- **Connection pooling** ready for production


## 🚨 Troubleshooting

### Common Issues

**Database Connection Error**
```
django.db.utils.OperationalError: could not connect to server
```
**Solution**: Check PostgreSQL is running and credentials in `.env` are correct.

**Migration Errors**
```
django.db.utils.ProgrammingError: relation "books_book" does not exist
```
**Solution**: Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

**Google Books API Timeout**
```
requests.exceptions.Timeout
```
**Solution**: Check internet connection or increase timeout in `views.py`.

**Static Files Not Loading**
```
404 error for CSS/JS files
```
**Solution**: Run `python manage.py collectstatic` and check `STATIC_URL` configuration.

### Debug Mode
Enable detailed error messages:
```python
# In settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

## 🔄 API Response Formats

### Success Responses

**List Books (GET /api/books/)**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "rating": 5,
      "published_date": "1925-04-10",
      "is_recent": false
    }
  ]
}
```

**Single Book (GET /api/books/1/)**
```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "published_date": "1925-04-10",
  "rating": 5,
  "isbn": "9780743273565",
  "description": "A classic American novel...",
  "page_count": 180,
  "thumbnail_url": "http://books.google.com/...",
  "is_recent": false,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

### Error Responses

**Validation Error (400)**
```json
{
  "rating": ["Rating must be between 1 and 5."],
  "published_date": ["Published date cannot be in the future."]
}
```

**Not Found (404)**
```json
{
  "detail": "Not found."
}
```

**Server Error (500)**
```json
{
  "error": "An unexpected error occurred: ..."
}
```

## 📚 Additional Resources

### Django Documentation
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL with Django](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)

### External APIs
- [Google Books API Documentation](https://developers.google.com/books/docs/v1/using)
- [Open Library API](https://openlibrary.org/developers/api) (Alternative)

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
coverage run manage.py test
coverage report

# Code formatting
black .
isort .

# Linting
flake8 .
```

---

**Made with ❤️ using Django, PostgreSQL, and modern web technologies.**

🚀 **Happy Coding!** 🚀