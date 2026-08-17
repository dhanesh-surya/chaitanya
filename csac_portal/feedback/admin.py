from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html
from .models import (
    StudentFeedback,
    ParentFeedback,
    FacultyFeedback,
    AlumniFeedback,
    AdmissionFest2026Feedback,
    EventFeedbackCampaign,
    EventFeedbackResponse,
)
from .forms import EventFeedbackCampaignAdminForm
from .export_utils import build_excel_response, build_pdf_response


@admin.register(StudentFeedback)
class StudentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'program', 'academic_year', 'overall_experience', 'submitted_at')
    list_filter = ('academic_year', 'program')
    search_fields = ('student_name', 'roll_number')
    readonly_fields = ('submitted_at',)


@admin.register(ParentFeedback)
class ParentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('parent_name', 'student_name', 'academic_year', 'overall_satisfaction', 'submitted_at')
    list_filter = ('academic_year',)
    search_fields = ('parent_name', 'student_name')
    readonly_fields = ('submitted_at',)


@admin.register(FacultyFeedback)
class FacultyFeedbackAdmin(admin.ModelAdmin):
    list_display = ('faculty_name', 'department', 'academic_year', 'overall_satisfaction', 'submitted_at')
    list_filter = ('academic_year', 'department')
    search_fields = ('faculty_name', 'department')
    readonly_fields = ('submitted_at',)


@admin.register(AlumniFeedback)
class AlumniFeedbackAdmin(admin.ModelAdmin):
    list_display = ('alumni_name', 'batch_year', 'program', 'overall_experience', 'submitted_at')
    list_filter = ('batch_year',)
    search_fields = ('alumni_name', 'program')
    readonly_fields = ('submitted_at',)


@admin.register(AdmissionFest2026Feedback)
class AdmissionFest2026FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'visitor_type', 'overall_rating', 'submitted_at')
    search_fields = ('name', 'institution_name', 'city_village')
    readonly_fields = ('submitted_at',)


class EventFeedbackResponseInline(admin.TabularInline):
    model = EventFeedbackResponse
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ('name', 'visitor_type', 'overall_rating', 'final_description', 'submitted_at')
    readonly_fields = fields
    max_num = 0


@admin.register(EventFeedbackCampaign)
class EventFeedbackCampaignAdmin(admin.ModelAdmin):
    form = EventFeedbackCampaignAdminForm
    list_display = (
        'title',
        'slug',
        'is_active',
        'show_in_menu',
        'has_hindi',
        'order',
        'response_count',
        'public_link',
        'updated_at',
    )
    list_filter = ('is_active', 'show_in_menu', 'show_meet_greet_section')
    search_fields = (
        'title', 'title_hi', 'slug', 'featured_guest', 'featured_guest_hi',
        'subtitle', 'subtitle_hi',
    )
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'show_in_menu', 'order')
    readonly_fields = ('created_at', 'updated_at', 'public_link_display')
    save_as = True
    inlines = [EventFeedbackResponseInline]

    fieldsets = (
        ('Form identity (English)', {
            'fields': (
                'title',
                'slug',
                'menu_title',
                'subtitle',
                'featured_guest',
                'event_date',
                'public_link_display',
            ),
            'description': (
                'Create or edit an event feedback form. Use “Save as new” to clone for another event. '
                'Public language switcher shows English or Hindi based on the fields below.'
            ),
        }),
        ('हिन्दी अनुवाद – Form identity (Hindi)', {
            'fields': (
                'title_hi',
                'menu_title_hi',
                'subtitle_hi',
                'featured_guest_hi',
                'event_name_hi',
            ),
            'description': (
                'Filled Hindi text is shown when visitors choose हिन्दी on the public form. '
                'If left blank, built-in fallback translations may apply for known events.'
            ),
        }),
        ('Header & messages (English)', {
            'fields': (
                'institution_line',
                'accreditation_line',
                'intro_text',
                'confirmation_message',
                'tagline',
            ),
        }),
        ('हिन्दी अनुवाद – Header & messages (Hindi)', {
            'fields': (
                'institution_line_hi',
                'accreditation_line_hi',
                'intro_text_hi',
                'confirmation_message_hi',
                'tagline_hi',
            ),
        }),
        ('Visibility & menu', {
            'fields': ('is_active', 'show_in_menu', 'order'),
        }),
        ('Sections (show / hide)', {
            'fields': (
                'show_meet_greet_section',
                'show_college_experience_section',
                'show_event_impact_section',
                'show_voice_section',
            ),
        }),
        ('Option lists – English (one option per line)', {
            'classes': ('collapse',),
            'fields': (
                'visitor_type_options',
                'attraction_options',
                'heard_from_options',
                'attended_meet_greet_options',
                'excitement_options',
                'presence_made_exciting_options',
                'enjoy_meet_greet_options',
                'college_knowledge_options',
                'learned_options',
                'campus_impression_options',
                'another_celebrity_options',
                'final_description_options',
                'contribution_areas_options',
            ),
            'description': (
                'English values are stored in responses (for reports). '
                'Edit these lists to customize answer choices.'
            ),
        }),
        ('हिन्दी अनुवाद – Option lists (Hindi labels)', {
            'classes': ('collapse',),
            'fields': (
                'visitor_type_options_hi',
                'attraction_options_hi',
                'heard_from_options_hi',
                'attended_meet_greet_options_hi',
                'excitement_options_hi',
                'presence_made_exciting_options_hi',
                'enjoy_meet_greet_options_hi',
                'college_knowledge_options_hi',
                'learned_options_hi',
                'campus_impression_options_hi',
                'another_celebrity_options_hi',
                'final_description_options_hi',
                'contribution_areas_options_hi',
            ),
            'description': (
                'One Hindi label per line, in the same order as the English list. '
                'Line count must match the English list. Blank = use built-in dictionary fallback.'
            ),
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Responses')
    def response_count(self, obj):
        return obj.responses.count()

    @admin.display(boolean=True, description='Hindi')
    def has_hindi(self, obj):
        return bool(obj.title_hi or obj.intro_text_hi or obj.visitor_type_options_hi)

    @admin.display(description='Public form')
    def public_link(self, obj):
        if not obj.pk:
            return '—'
        url = obj.get_public_url_path()
        return format_html(
            '<a href="{}" target="_blank">EN</a> · <a href="{}?lang=hi" target="_blank">HI</a>',
            url,
            url,
        )

    @admin.display(description='Public form URL')
    def public_link_display(self, obj):
        if not obj.pk:
            return 'Save first to get the public URL.'
        url = obj.get_public_url_path()
        return format_html(
            '<a href="{}" target="_blank">{}</a> &nbsp;|&nbsp; '
            '<a href="{}?lang=hi" target="_blank">Hindi (?lang=hi)</a>',
            url,
            url,
            url,
        )


@admin.register(EventFeedbackResponse)
class EventFeedbackResponseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'campaign',
        'visitor_type',
        'overall_rating',
        'final_description',
        'submitted_at',
        'certificate_link',
    )
    list_filter = (
        'campaign',
        'visitor_type',
        'overall_rating',
        'final_description',
        'attended_meet_greet',
    )
    search_fields = (
        'name',
        'institution_name',
        'city_village',
        'best_part',
        'additional_comments',
        'message_for_guest',
    )
    readonly_fields = ('submitted_at',)
    date_hierarchy = 'submitted_at'
    actions = ('export_selected_excel', 'export_selected_pdf', 'download_certificates_zip')
    change_list_template = 'admin/feedback/eventfeedbackresponse/change_list.html'

    fieldsets = (
        (None, {
            'fields': ('campaign', 'submitted_at'),
        }),
        ('About the visitor', {
            'fields': ('name', 'visitor_type', 'institution_name', 'city_village'),
        }),
        ('Why they joined', {
            'fields': ('attractions', 'heard_from'),
        }),
        ('Event ratings', {
            'fields': (
                'overall_rating',
                'organization_rating',
                'hospitality_rating',
                'atmosphere_rating',
                'stage_programme_rating',
                'crowd_management_rating',
                'facilities_rating',
            ),
        }),
        ('Meet & Greet', {
            'fields': (
                'attended_meet_greet',
                'meet_greet_rating',
                'excitement_level',
                'presence_made_exciting',
                'enjoy_most_meet_greet',
            ),
        }),
        ('College experience', {
            'fields': (
                'college_knowledge',
                'learned_experienced',
                'campus_impression',
                'contribution_areas',
                'contribution_other_suggestion',
            ),
        }),
        ('Event impact', {
            'fields': (
                'memorable_scale',
                'attend_future_scale',
                'recommend_events_scale',
                'another_celebrity_meet',
            ),
        }),
        ('Your voice', {
            'fields': (
                'best_part',
                'improvements',
                'message_for_guest',
                'additional_comments',
                'final_description',
            ),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'export/excel/',
                self.admin_site.admin_view(self.export_all_excel_view),
                name='feedback_eventfeedbackresponse_export_excel',
            ),
            path(
                'export/pdf/',
                self.admin_site.admin_view(self.export_all_pdf_view),
                name='feedback_eventfeedbackresponse_export_pdf',
            ),
            path(
                '<int:response_id>/certificate/',
                self.admin_site.admin_view(self.admin_certificate_view),
                name='feedback_eventfeedbackresponse_certificate',
            ),
        ]
        return custom + urls

    def admin_certificate_view(self, request, response_id):
        from .certificate import certificate_http_response
        obj = get_object_or_404(EventFeedbackResponse, pk=response_id)
        return certificate_http_response(obj, lang='en')

    @admin.display(description='Certificate')
    def certificate_link(self, obj):
        url = reverse(
            'admin:feedback_eventfeedbackresponse_certificate',
            args=[obj.pk],
        )
        return format_html(
            '<a href="{}" target="_blank" style="color:#E61013;font-weight:600;">PDF</a>',
            url,
        )

    def _filtered_queryset(self, request):
        """Same queryset as the changelist (respects filters/search)."""
        cl = self.get_changelist_instance(request)
        return cl.get_queryset(request)

    def export_all_excel_view(self, request):
        qs = self._filtered_queryset(request)
        if not qs.exists():
            self.message_user(request, 'No responses to export.', level=messages.WARNING)
            return HttpResponseRedirect(
                reverse('admin:feedback_eventfeedbackresponse_changelist')
            )
        return build_excel_response(qs)

    def export_all_pdf_view(self, request):
        qs = self._filtered_queryset(request)
        if not qs.exists():
            self.message_user(request, 'No responses to export.', level=messages.WARNING)
            return HttpResponseRedirect(
                reverse('admin:feedback_eventfeedbackresponse_changelist')
            )
        return build_pdf_response(qs)

    @admin.action(description='Export selected as Excel')
    def export_selected_excel(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, 'No rows selected.', level=messages.WARNING)
            return None
        return build_excel_response(queryset)

    @admin.action(description='Export selected as PDF')
    def export_selected_pdf(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, 'No rows selected.', level=messages.WARNING)
            return None
        return build_pdf_response(queryset)

    @admin.action(description='Download participation certificates (ZIP)')
    def download_certificates_zip(self, request, queryset):
        import zipfile
        from io import BytesIO
        from django.http import HttpResponse
        from .certificate import build_participation_certificate_pdf, certificate_number

        if not queryset.exists():
            self.message_user(request, 'No rows selected.', level=messages.WARNING)
            return None

        buf = BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for obj in queryset.select_related('campaign'):
                pdf = build_participation_certificate_pdf(obj)
                cert_no = certificate_number(obj)
                safe = ''.join(ch if ch.isalnum() or ch in '-_' else '_' for ch in obj.name)[:40]
                zf.writestr(f'{cert_no}_{safe}.pdf', pdf)
        buf.seek(0)
        resp = HttpResponse(buf.getvalue(), content_type='application/zip')
        resp['Content-Disposition'] = 'attachment; filename="participation_certificates.zip"'
        return resp

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Preserve current filter query string on export links
        query = request.GET.urlencode()
        excel_url = reverse('admin:feedback_eventfeedbackresponse_export_excel')
        pdf_url = reverse('admin:feedback_eventfeedbackresponse_export_pdf')
        if query:
            excel_url = f'{excel_url}?{query}'
            pdf_url = f'{pdf_url}?{query}'
        extra_context.update({
            'export_excel_url': excel_url,
            'export_pdf_url': pdf_url,
        })
        return super().changelist_view(request, extra_context=extra_context)
