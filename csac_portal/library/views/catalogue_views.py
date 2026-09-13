from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from library.models import Book, BookCopy, Subject, BookCategory, Publisher
from academics.models import Department


def library_home(request):
    recent_books = Book.objects.filter(is_active=True).prefetch_related('copies').order_by('-created_at')[:6]
    total_titles = Book.objects.filter(is_active=True).count()
    total_copies = BookCopy.objects.filter(is_active=True).count()
    available_copies = BookCopy.objects.filter(is_active=True, status='AVAILABLE').count()
    subjects = Subject.objects.all()[:8]
    departments = Department.objects.all()[:8]

    context = {
        'page_title': 'Central Library',
        'breadcrumb': 'Digital Library & Circulation',
        'recent_books': recent_books,
        'total_titles': total_titles,
        'total_copies': total_copies,
        'available_copies': available_copies,
        'subjects': subjects,
        'departments': departments,
    }
    return render(request, 'library/home.html', context)


def catalogue(request):
    query = request.GET.get('q', '').strip()
    subject_id = request.GET.get('subject', '').strip()
    category_id = request.GET.get('category', '').strip()
    dept_id = request.GET.get('dept', '').strip()
    availability = request.GET.get('availability', '').strip()
    sort_by = request.GET.get('sort', '-created_at')

    books = Book.objects.filter(is_active=True).select_related('publisher', 'subject', 'category', 'department').prefetch_related('copies')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query) |
            Q(publisher__name__icontains=query) |
            Q(copies__accession_number__icontains=query)
        ).distinct()

    if subject_id:
        books = books.filter(subject_id=subject_id)

    if category_id:
        books = books.filter(category_id=category_id)

    if dept_id:
        books = books.filter(department_id=dept_id)

    if availability == 'available':
        books = books.filter(copies__status='AVAILABLE', copies__is_active=True).distinct()

    valid_sorts = {
        'title_asc': 'title',
        'title_desc': '-title',
        'author': 'author',
        'year_desc': '-publication_year',
        '-created_at': '-created_at'
    }
    order_field = valid_sorts.get(sort_by, '-created_at')
    books = books.order_by(order_field)

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_subjects = Subject.objects.all()
    all_categories = BookCategory.objects.all()
    all_departments = Department.objects.all()

    context = {
        'page_title': 'Library Catalogue',
        'breadcrumb': 'Book Catalogue & Search',
        'books': page_obj,
        'query': query,
        'selected_subject': subject_id,
        'selected_category': category_id,
        'selected_dept': dept_id,
        'selected_availability': availability,
        'selected_sort': sort_by,
        'all_subjects': all_subjects,
        'all_categories': all_categories,
        'all_departments': all_departments,
    }
    return render(request, 'library/catalogue.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(
        Book.objects.select_related('publisher', 'subject', 'category', 'department').prefetch_related('copies'),
        id=book_id,
        is_active=True
    )
    copies = book.copies.filter(is_active=True).order_by('accession_number')

    student_profile = None
    if request.user.is_authenticated and hasattr(request.user, 'library_student_profile'):
        student_profile = request.user.library_student_profile

    context = {
        'page_title': book.title,
        'breadcrumb': 'Book Details',
        'book': book,
        'copies': copies,
        'student_profile': student_profile,
    }
    return render(request, 'library/book_detail.html', context)
