from django.contrib import admin
from .models import NAACDocument, IQACMember, NAACCriteria, NAACInfo


@admin.register(NAACDocument)
class NAACDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'uploaded_at', 'order')
    list_filter = ('doc_type',)
    list_editable = ('order',)
    search_fields = ('title',)


@admin.register(IQACMember)
class IQACMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'role', 'department', 'order')
    list_filter = ('role',)
    list_editable = ('order',)


@admin.register(NAACCriteria)
class NAACCriteriaAdmin(admin.ModelAdmin):
    list_display = ('criterion', 'criterion_number', 'title', 'order')
    list_filter = ('criterion',)
    list_editable = ('order',)
    fields = ('criterion', 'criterion_number', 'title', 'description', 'document', 'document_url', 'order')


@admin.register(NAACInfo)
class NAACInfoAdmin(admin.ModelAdmin):
    list_display = ('grade', 'cgpa', 'accreditation_date', 'valid_until')
