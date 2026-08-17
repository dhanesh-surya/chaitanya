from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# ---------------------------------------------------------------------------
# Existing academic feedback models
# ---------------------------------------------------------------------------

class StudentFeedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    student_name = models.CharField(max_length=150)
    roll_number = models.CharField(max_length=30, blank=True)
    program = models.CharField(max_length=200)
    year_of_study = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=10)
    teaching_quality = models.IntegerField(choices=RATING_CHOICES)
    infrastructure = models.IntegerField(choices=RATING_CHOICES)
    library_resources = models.IntegerField(choices=RATING_CHOICES)
    sports_facilities = models.IntegerField(choices=RATING_CHOICES)
    overall_experience = models.IntegerField(choices=RATING_CHOICES)
    suggestions = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Student Feedback"
        verbose_name_plural = "Student Feedback"

    def __str__(self):
        return f"{self.student_name} ({self.academic_year})"


class ParentFeedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    parent_name = models.CharField(max_length=150)
    student_name = models.CharField(max_length=150)
    program = models.CharField(max_length=200)
    academic_year = models.CharField(max_length=10)
    teaching_quality = models.IntegerField(choices=RATING_CHOICES)
    communication = models.IntegerField(choices=RATING_CHOICES)
    safety = models.IntegerField(choices=RATING_CHOICES)
    overall_satisfaction = models.IntegerField(choices=RATING_CHOICES)
    suggestions = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Parent Feedback"
        verbose_name_plural = "Parent Feedback"

    def __str__(self):
        return f"{self.parent_name} - Parent of {self.student_name}"


class FacultyFeedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    faculty_name = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    academic_year = models.CharField(max_length=10)
    infrastructure = models.IntegerField(choices=RATING_CHOICES)
    admin_support = models.IntegerField(choices=RATING_CHOICES)
    research_support = models.IntegerField(choices=RATING_CHOICES)
    work_environment = models.IntegerField(choices=RATING_CHOICES)
    overall_satisfaction = models.IntegerField(choices=RATING_CHOICES)
    suggestions = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Faculty Feedback"
        verbose_name_plural = "Faculty Feedback"

    def __str__(self):
        return f"{self.faculty_name} ({self.department})"


class AlumniFeedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    alumni_name = models.CharField(max_length=150)
    batch_year = models.IntegerField()
    program = models.CharField(max_length=200)
    current_status = models.CharField(max_length=200, blank=True, help_text="e.g. Employed at XYZ / Higher Studies")
    teaching_quality = models.IntegerField(choices=RATING_CHOICES)
    campus_experience = models.IntegerField(choices=RATING_CHOICES)
    career_support = models.IntegerField(choices=RATING_CHOICES)
    overall_experience = models.IntegerField(choices=RATING_CHOICES)
    suggestions = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Alumni Feedback"
        verbose_name_plural = "Alumni Feedback"

    def __str__(self):
        return f"{self.alumni_name} (Batch {self.batch_year})"


# ---------------------------------------------------------------------------
# Multi-event feedback (create / customize campaigns in admin)
# ---------------------------------------------------------------------------

def _default_lines(*lines):
    return '\n'.join(lines)


class EventFeedbackCampaign(models.Model):
    """
    Configurable event feedback form.
    Create new events in admin, customize copy/options, toggle sections.
    """

    title = models.CharField(
        max_length=200,
        help_text='Form heading, e.g. "Admission Fest 2026 – Feedback Form"',
    )
    slug = models.SlugField(
        max_length=80,
        unique=True,
        help_text='URL path: /feedback/events/<slug>/',
    )
    menu_title = models.CharField(
        max_length=120,
        blank=True,
        help_text='Short title for navbar (defaults to title)',
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        help_text='e.g. Special Meet & Greet with Mann Qureshi',
    )
    featured_guest = models.CharField(
        max_length=150,
        blank=True,
        help_text='Guest name used in Meet & Greet questions (e.g. Mann Qureshi)',
    )
    institution_line = models.CharField(
        max_length=200,
        default='Chaitanya Science and Arts College, Pamgarh',
    )
    accreditation_line = models.CharField(
        max_length=200,
        default="An Autonomous Institution | NAAC Accredited Grade 'A'",
        blank=True,
    )
    intro_text = models.TextField(
        help_text='Shown above the form. Use blank lines for paragraphs.',
    )
    confirmation_message = models.TextField(
        default=(
            'Thank You for Your Feedback!\n\n'
            'We are delighted that you were a part of this event.\n\n'
            'Your feedback will help us organize even better events in the future.\n\n'
            'Chaitanya Science and Arts College, Pamgarh\n'
            '✨ Learn • Grow • Achieve ✨'
        ),
    )
    tagline = models.CharField(max_length=100, default='✨ Learn • Grow • Achieve ✨', blank=True)

    # Hindi translations (edited in admin – used when visitor selects हिन्दी)
    title_hi = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Title (Hindi)',
        help_text='हिन्दी शीर्षक – shown when language is Hindi',
    )
    menu_title_hi = models.CharField(max_length=120, blank=True, verbose_name='Menu title (Hindi)')
    subtitle_hi = models.CharField(max_length=300, blank=True, verbose_name='Subtitle (Hindi)')
    featured_guest_hi = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Featured guest (Hindi)',
        help_text='e.g. मान कुरैशी',
    )
    event_name_hi = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Short event name (Hindi)',
        help_text='Used inside questions, e.g. एडमिशन फेस्ट 2026',
    )
    institution_line_hi = models.CharField(
        max_length=200, blank=True, verbose_name='Institution line (Hindi)'
    )
    accreditation_line_hi = models.CharField(
        max_length=200, blank=True, verbose_name='Accreditation line (Hindi)'
    )
    intro_text_hi = models.TextField(blank=True, verbose_name='Intro text (Hindi)')
    confirmation_message_hi = models.TextField(
        blank=True, verbose_name='Confirmation message (Hindi)'
    )
    tagline_hi = models.CharField(max_length=100, blank=True, verbose_name='Tagline (Hindi)')

    event_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text='Public form is open for responses')
    show_in_menu = models.BooleanField(default=True, help_text='List under Feedback in the navbar')
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')

    # Section visibility
    show_meet_greet_section = models.BooleanField(
        default=True,
        verbose_name='Show Meet & Greet section',
    )
    show_college_experience_section = models.BooleanField(
        default=True,
        verbose_name='Show College Experience section',
    )
    show_event_impact_section = models.BooleanField(
        default=True,
        verbose_name='Show Event Impact section',
    )
    show_voice_section = models.BooleanField(
        default=True,
        verbose_name='Show Your Voice section',
    )

    # Customizable option lists (one option per line)
    visitor_type_options = models.TextField(
        default=_default_lines(
            'School Student',
            'College Student',
            'Graduate / Postgraduate',
            'Parent / Guardian',
            'Alumni',
            'Local Visitor',
            'Other',
        ),
        help_text='One option per line',
    )
    attraction_options = models.TextField(
        default=_default_lines(
            'Meet & Greet with celebrity / guest',
            'Admission / Course Information',
            'College Campus Visit',
            'Entertainment & Activities',
            'Friends / Family',
            'Social Media Promotion',
            'College Invitation',
            'Other',
        ),
        help_text='Checkbox options – one per line',
    )
    heard_from_options = models.TextField(
        default=_default_lines(
            'Instagram / Facebook / Social Media',
            'WhatsApp',
            'Friends / Family',
            'School / College',
            'Posters / Banners',
            'College Staff / Students',
            'Other',
        ),
    )
    attended_meet_greet_options = models.TextField(
        default=_default_lines(
            'Yes',
            'No',
            'I watched from the audience',
        ),
    )
    excitement_options = models.TextField(
        default=_default_lines(
            'Extremely Excited',
            'Very Excited',
            'Excited',
            'Somewhat Excited',
            'Neutral',
        ),
    )
    presence_made_exciting_options = models.TextField(
        default=_default_lines(
            'Definitely Yes',
            'Yes',
            'Somewhat',
            'Not Much',
            'No',
        ),
    )
    enjoy_meet_greet_options = models.TextField(
        default=_default_lines(
            'Seeing the guest in person',
            'Meeting / interacting with them',
            'Taking photos / selfies',
            'Stage interaction',
            'Overall atmosphere',
            'Being part of the crowd',
            'Other',
        ),
    )
    college_knowledge_options = models.TextField(
        default=_default_lines(
            'Yes, a lot',
            'Yes, somewhat',
            'A little',
            'Not really',
        ),
    )
    learned_options = models.TextField(
        default=_default_lines(
            'Courses & Programmes',
            'College Facilities',
            'Admission Process',
            'Scholarships',
            'Campus Environment',
            'Faculty & Student Interaction',
            'Career Opportunities',
            'Cultural / Student Activities',
            'I mainly attended the event',
            'Other',
        ),
        help_text='Checkbox options – one per line',
    )
    campus_impression_options = models.TextField(
        default=_default_lines(
            'Excellent',
            'Very Good',
            'Good',
            'Average',
            'Needs Improvement',
        ),
    )
    another_celebrity_options = models.TextField(
        default=_default_lines(
            'Definitely Yes!',
            'Yes',
            'Maybe',
            'Not Sure',
            'No',
        ),
    )
    final_description_options = models.TextField(
        default=_default_lines(
            'Amazing – Loved It!',
            'Excellent',
            'Very Good',
            'Good',
            'Average',
            'Needs Improvement',
        ),
    )
    contribution_areas_options = models.TextField(
        default=_default_lines(
            'Financial assistance for needy students',
            'Subject expert / mentor',
            'Support for library enrichment',
            'Other suggestions for development',
        ),
        help_text='Checkbox options – one per line. Contribution areas for college development.',
        verbose_name='Contribution area options (English)',
    )

    # Hindi option lists – one line per English option (same order)
    visitor_type_options_hi = models.TextField(
        blank=True,
        verbose_name='Visitor type options (Hindi)',
        help_text='One Hindi label per line, same order as English list',
    )
    attraction_options_hi = models.TextField(
        blank=True,
        verbose_name='Attraction options (Hindi)',
        help_text='One Hindi label per line, same order as English list',
    )
    heard_from_options_hi = models.TextField(
        blank=True,
        verbose_name='Heard from options (Hindi)',
        help_text='One Hindi label per line, same order as English list',
    )
    attended_meet_greet_options_hi = models.TextField(
        blank=True, verbose_name='Attended Meet & Greet options (Hindi)'
    )
    excitement_options_hi = models.TextField(
        blank=True, verbose_name='Excitement options (Hindi)'
    )
    presence_made_exciting_options_hi = models.TextField(
        blank=True, verbose_name='Presence made exciting options (Hindi)'
    )
    enjoy_meet_greet_options_hi = models.TextField(
        blank=True, verbose_name='Enjoy Meet & Greet options (Hindi)'
    )
    college_knowledge_options_hi = models.TextField(
        blank=True, verbose_name='College knowledge options (Hindi)'
    )
    learned_options_hi = models.TextField(
        blank=True, verbose_name='Learned / experienced options (Hindi)'
    )
    campus_impression_options_hi = models.TextField(
        blank=True, verbose_name='Campus impression options (Hindi)'
    )
    another_celebrity_options_hi = models.TextField(
        blank=True, verbose_name='Another celebrity Meet & Greet options (Hindi)'
    )
    final_description_options_hi = models.TextField(
        blank=True, verbose_name='Final description options (Hindi)'
    )
    contribution_areas_options_hi = models.TextField(
        blank=True,
        verbose_name='Contribution area options (Hindi)',
        help_text=(
            'One Hindi label per line, same order as English list. '
            'e.g. निर्धन छात्रों हेतु आर्थिक सहायता'
        ),
        default=_default_lines(
            'निर्धन छात्रों हेतु आर्थिक सहायता',
            'विषय विशेषज्ञ / मार्गदर्शक',
            'पुस्तकालय संवर्धन हेतु सहयोग',
            'विकास हेतु अन्य कोई सुझाव',
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-event_date', 'title']
        verbose_name = 'Event Feedback Form'
        verbose_name_plural = 'Event Feedback Forms (create / edit)'

    def __str__(self):
        status = 'Active' if self.is_active else 'Inactive'
        return f'{self.title} ({status})'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:80]
        if not self.menu_title:
            self.menu_title = self.title[:120]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('feedback:event_feedback', kwargs={'slug': self.slug})

    def get_public_url_path(self):
        return f'/feedback/events/{self.slug}/'

    @staticmethod
    def parse_options(text):
        if not text:
            return []
        lines = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            # Allow "English||Hindi" legacy format – value is English part
            if '||' in line:
                line = line.split('||', 1)[0].strip()
            if line:
                lines.append(line)
        return lines

    def options(self, field_name):
        return self.parse_options(getattr(self, field_name, ''))

    def options_hi(self, field_name):
        """Hindi labels for an English options field (same line order)."""
        hi_field = f'{field_name}_hi' if not field_name.endswith('_hi') else field_name
        if not hasattr(self, hi_field):
            hi_field = field_name if field_name.endswith('_hi') else f'{field_name}_hi'
        return self.parse_options(getattr(self, hi_field, '') or '')

    def guest_display(self, lang='en'):
        if lang == 'hi' and self.featured_guest_hi:
            return self.featured_guest_hi
        return self.featured_guest or 'the guest'


class EventFeedbackResponse(models.Model):
    """One visitor response to an EventFeedbackCampaign."""

    SCALE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    RATING_LABELS = [
        (5, '5 – Excellent'),
        (4, '4 – Very Good'),
        (3, '3 – Good'),
        (2, '2 – Fair'),
        (1, '1 – Poor'),
    ]

    campaign = models.ForeignKey(
        EventFeedbackCampaign,
        on_delete=models.CASCADE,
        related_name='responses',
    )

    # Section 1 – About You
    name = models.CharField(max_length=150, verbose_name='Your Name')
    visitor_type = models.CharField(max_length=100, verbose_name='You are a')
    institution_name = models.CharField(
        max_length=250, blank=True, verbose_name='School / College / Institution Name'
    )
    city_village = models.CharField(max_length=150, blank=True, verbose_name='City / Village')

    # Section 2 – Why join
    attractions = models.TextField(
        verbose_name='What attracted you to this event?',
        help_text='Comma-separated selections',
    )
    heard_from = models.CharField(max_length=150, verbose_name='How did you hear about this event?')

    # Section 3 – Ratings (1–5)
    overall_rating = models.IntegerField(choices=RATING_LABELS, verbose_name='Overall event rating')
    organization_rating = models.IntegerField(choices=RATING_LABELS, verbose_name='Organization')
    hospitality_rating = models.IntegerField(choices=RATING_LABELS, verbose_name='Welcome & hospitality')
    atmosphere_rating = models.IntegerField(choices=RATING_LABELS, verbose_name='Event atmosphere')
    stage_programme_rating = models.IntegerField(
        choices=RATING_LABELS, verbose_name='Stage & programme arrangements'
    )
    crowd_management_rating = models.IntegerField(choices=RATING_LABELS, verbose_name='Crowd management')
    facilities_rating = models.IntegerField(choices=RATING_LABELS, verbose_name='Facilities')

    # Section 4 – Meet & Greet
    attended_meet_greet = models.CharField(max_length=100, blank=True)
    meet_greet_rating = models.IntegerField(choices=RATING_LABELS, blank=True, null=True)
    excitement_level = models.CharField(max_length=100, blank=True)
    presence_made_exciting = models.CharField(max_length=100, blank=True)
    enjoy_most_meet_greet = models.CharField(max_length=150, blank=True)

    # Section 5 – College experience
    college_knowledge = models.CharField(max_length=100, blank=True)
    learned_experienced = models.TextField(blank=True, help_text='Comma-separated selections')
    campus_impression = models.CharField(max_length=100, blank=True)
    contribution_areas = models.TextField(
        blank=True,
        help_text='Comma-separated selections',
        verbose_name='Areas of contribution to college development',
    )
    contribution_other_suggestion = models.TextField(
        blank=True,
        verbose_name='Other suggestion for college development',
    )

    # Section 6 – Event impact (1–5 scales)
    memorable_scale = models.IntegerField(choices=SCALE_CHOICES, blank=True, null=True)
    attend_future_scale = models.IntegerField(choices=SCALE_CHOICES, blank=True, null=True)
    recommend_events_scale = models.IntegerField(choices=SCALE_CHOICES, blank=True, null=True)
    another_celebrity_meet = models.CharField(max_length=100, blank=True)

    # Section 7 – Your voice
    best_part = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    message_for_guest = models.TextField(blank=True)
    additional_comments = models.TextField(blank=True)

    # Final
    final_description = models.CharField(max_length=100, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Event Feedback Response'
        verbose_name_plural = 'Event Feedback Responses'

    def __str__(self):
        return f'{self.name} → {self.campaign.title} ({self.submitted_at:%Y-%m-%d})'


# Keep old model for any historical rows (admin can still view; no new public form)
class AdmissionFest2026Feedback(models.Model):
    """Deprecated: use EventFeedbackCampaign + EventFeedbackResponse."""

    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ Excellent'),
        (4, '⭐⭐⭐⭐ Very Good'),
        (3, '⭐⭐⭐ Good'),
        (2, '⭐⭐ Fair'),
        (1, '⭐ Poor'),
    ]
    VISITOR_TYPE_CHOICES = [
        ('school_student', 'School Student'),
        ('college_student', 'College Student'),
        ('graduate', 'Graduate / Postgraduate'),
        ('parent', 'Parent / Guardian'),
        ('alumni', 'Alumni'),
        ('local_visitor', 'Local Visitor'),
        ('other', 'Other'),
    ]
    HEARD_FROM_CHOICES = [
        ('social_media', 'Instagram / Facebook / Social Media'),
        ('whatsapp', 'WhatsApp'),
        ('friends_family', 'Friends / Family'),
        ('school_college', 'School / College'),
        ('posters', 'Posters / Banners'),
        ('staff_students', 'College Staff / Students'),
        ('other', 'Other'),
    ]
    ATTENDED_MEET_GREET_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('audience', 'I watched from the audience'),
    ]
    EXCITEMENT_CHOICES = [
        ('extremely', 'Extremely Excited'),
        ('very', 'Very Excited'),
        ('excited', 'Excited'),
        ('somewhat', 'Somewhat Excited'),
        ('neutral', 'Neutral'),
    ]
    YES_NO_SOMEWHAT_CHOICES = [
        ('yes', 'Yes, definitely'),
        ('somewhat', 'Somewhat'),
        ('no', 'No'),
    ]
    YES_NO_MAYBE_CHOICES = [
        ('yes', 'Yes'),
        ('maybe', 'Maybe'),
        ('no', 'No'),
    ]

    name = models.CharField(max_length=150, verbose_name='Your Name')
    visitor_type = models.CharField(max_length=30, choices=VISITOR_TYPE_CHOICES)
    institution_name = models.CharField(max_length=250, blank=True)
    city_village = models.CharField(max_length=150, blank=True)
    attractions = models.TextField()
    heard_from = models.CharField(max_length=30, choices=HEARD_FROM_CHOICES)
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    organization_rating = models.IntegerField(choices=RATING_CHOICES)
    hospitality_rating = models.IntegerField(choices=RATING_CHOICES)
    atmosphere_rating = models.IntegerField(choices=RATING_CHOICES)
    stage_programme_rating = models.IntegerField(choices=RATING_CHOICES)
    crowd_management_rating = models.IntegerField(choices=RATING_CHOICES)
    facilities_rating = models.IntegerField(choices=RATING_CHOICES)
    attended_meet_greet = models.CharField(max_length=20, choices=ATTENDED_MEET_GREET_CHOICES)
    meet_greet_rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    excitement_level = models.CharField(max_length=20, choices=EXCITEMENT_CHOICES)
    presence_made_exciting = models.CharField(max_length=20, choices=YES_NO_SOMEWHAT_CHOICES)
    best_part = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    would_recommend = models.CharField(max_length=10, choices=YES_NO_MAYBE_CHOICES)
    would_attend_again = models.CharField(max_length=10, choices=YES_NO_MAYBE_CHOICES)
    interested_in_admission = models.CharField(max_length=10, choices=YES_NO_MAYBE_CHOICES, blank=True)
    additional_comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Admission Fest 2026 Feedback (legacy)'
        verbose_name_plural = 'Admission Fest 2026 Feedback (legacy)'

    def __str__(self):
        return f'{self.name} – Admission Fest 2026 ({self.submitted_at:%Y-%m-%d})'
