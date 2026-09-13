from django.contrib import admin
from .models import (
    Publisher, Subject, BookCategory, StudentProfile, LibrarianProfile,
    Book, BookCopy, LibraryRequest, CirculationTransaction, Fine,
    LibrarySetting, AuditLog, ExcelImport
)


class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 1
    fields = ('accession_number', 'barcode', 'rack_location', 'status', 'condition', 'is_active')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publisher', 'department', 'total_copies_count', 'available_copies_count', 'is_active')
    list_filter = ('is_active', 'department', 'subject', 'category', 'publisher')
    search_fields = ('title', 'author', 'isbn', 'copies__accession_number')
    inlines = [BookCopyInline]


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('accession_number', 'book', 'rack_location', 'status', 'condition', 'is_active')
    list_filter = ('status', 'condition', 'is_active')
    search_fields = ('accession_number', 'barcode', 'book__title', 'rack_location')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('enrollment_number', 'library_card_number', 'full_name', 'course', 'semester', 'status', 'is_library_eligible', 'active_issued_count')
    list_filter = ('status', 'is_library_eligible', 'course', 'semester')
    search_fields = ('enrollment_number', 'library_card_number', 'user__username', 'user__first_name', 'user__last_name', 'mobile')


@admin.register(LibrarianProfile)
class LibrarianProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'designation', 'contact_phone')
    search_fields = ('employee_id', 'user__username', 'user__first_name', 'user__last_name')


@admin.register(LibraryRequest)
class LibraryRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'student', 'book_copy', 'status', 'requested_at', 'reviewed_by')
    list_filter = ('status', 'requested_at')
    search_fields = ('request_number', 'student__enrollment_number', 'book_copy__accession_number', 'book_copy__book__title')
    readonly_fields = ('request_number', 'requested_at')


@admin.register(CirculationTransaction)
class CirculationTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_number', 'student', 'book_copy', 'status', 'issued_at', 'due_date', 'fine_amount', 'fine_paid')
    list_filter = ('status', 'fine_paid', 'issued_at', 'due_date')
    search_fields = ('transaction_number', 'student__enrollment_number', 'book_copy__accession_number', 'book_copy__book__title')
    readonly_fields = ('transaction_number', 'issued_at')


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'student', 'amount', 'overdue_days', 'is_settled', 'payment_method')
    list_filter = ('is_settled', 'payment_method')
    search_fields = ('student__enrollment_number', 'transaction__transaction_number')


@admin.register(LibrarySetting)
class LibrarySettingAdmin(admin.ModelAdmin):
    list_display = ('max_books_per_student', 'default_loan_days', 'fine_per_day', 'max_pending_requests', 'request_expiry_days')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action', 'reference_id', 'user', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('reference_id', 'description', 'user__username')
    readonly_fields = ('timestamp', 'action', 'reference_id', 'description', 'user', 'ip_address')


@admin.register(ExcelImport)
class ExcelImportAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'uploaded_by', 'uploaded_at', 'total_rows', 'valid_rows', 'duplicate_accessions', 'status')
    list_filter = ('status', 'uploaded_at')


admin.site.register(Publisher)
admin.site.register(Subject)
admin.site.register(BookCategory)
