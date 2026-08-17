from django import forms
from .models import (
    StudentFeedback,
    ParentFeedback,
    FacultyFeedback,
    AlumniFeedback,
    EventFeedbackCampaign,
    EventFeedbackResponse,
)
from .event_i18n import (
    campaign_choice_pairs,
    field_label,
    get_ui,
    localized_campaign_copy,
    normalize_lang,
    star_rating_choices,
)

RATING_WIDGET = forms.Select(
    choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
    attrs={'class': 'form-select'},
)

YEAR_CHOICES = [(str(y), f"{y}-{y + 1}") for y in range(2020, 2027)]

SCALE_CHOICES = [
    (5, '5'),
    (4, '4'),
    (3, '3'),
    (2, '2'),
    (1, '1'),
]


class StudentFeedbackForm(forms.ModelForm):
    class Meta:
        model = StudentFeedback
        fields = '__all__'
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_study': forms.Select(
                choices=[('1st', '1st Year'), ('2nd', '2nd Year'), ('3rd', '3rd Year')],
                attrs={'class': 'form-select'},
            ),
            'academic_year': forms.Select(choices=YEAR_CHOICES, attrs={'class': 'form-select'}),
            'teaching_quality': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'infrastructure': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'library_resources': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'sports_facilities': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'overall_experience': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'suggestions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ParentFeedbackForm(forms.ModelForm):
    class Meta:
        model = ParentFeedback
        fields = '__all__'
        widgets = {
            'parent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(choices=YEAR_CHOICES, attrs={'class': 'form-select'}),
            'teaching_quality': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'communication': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'safety': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'overall_satisfaction': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'suggestions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class FacultyFeedbackForm(forms.ModelForm):
    class Meta:
        model = FacultyFeedback
        fields = '__all__'
        widgets = {
            'faculty_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.Select(choices=YEAR_CHOICES, attrs={'class': 'form-select'}),
            'infrastructure': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'admin_support': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'research_support': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'work_environment': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'overall_satisfaction': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'suggestions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class AlumniFeedbackForm(forms.ModelForm):
    class Meta:
        model = AlumniFeedback
        fields = '__all__'
        widgets = {
            'alumni_name': forms.TextInput(attrs={'class': 'form-control'}),
            'batch_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2001}),
            'program': forms.TextInput(attrs={'class': 'form-control'}),
            'current_status': forms.TextInput(attrs={'class': 'form-control'}),
            'teaching_quality': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'campus_experience': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'career_support': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'overall_experience': forms.Select(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
                attrs={'class': 'form-select'},
            ),
            'suggestions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class EventFeedbackCampaignAdminForm(forms.ModelForm):
    """
    Admin ModelForm for bilingual event feedback campaigns.
    English + Hindi fields with clear widgets and help text.
    """

    class Meta:
        model = EventFeedbackCampaign
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 40em;'}),
            'title_hi': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 40em;'}),
            'menu_title': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 30em;'}),
            'menu_title_hi': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 30em;'}),
            'subtitle': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 40em;'}),
            'subtitle_hi': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 40em;'}),
            'featured_guest': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 25em;'}),
            'featured_guest_hi': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 25em;'}),
            'event_name_hi': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 25em;'}),
            'institution_line': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 40em;'}),
            'institution_line_hi': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 40em;'}),
            'accreditation_line': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 40em;'}),
            'accreditation_line_hi': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 40em;'}),
            'intro_text': forms.Textarea(attrs={'rows': 6, 'cols': 80, 'class': 'vLargeTextField'}),
            'intro_text_hi': forms.Textarea(attrs={'rows': 6, 'cols': 80, 'class': 'vLargeTextField'}),
            'confirmation_message': forms.Textarea(attrs={'rows': 6, 'cols': 80, 'class': 'vLargeTextField'}),
            'confirmation_message_hi': forms.Textarea(attrs={'rows': 6, 'cols': 80, 'class': 'vLargeTextField'}),
            'tagline': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 30em;'}),
            'tagline_hi': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 30em;'}),
            # Option lists – tall textareas
            'visitor_type_options': forms.Textarea(attrs={'rows': 8, 'cols': 60}),
            'visitor_type_options_hi': forms.Textarea(attrs={'rows': 8, 'cols': 60}),
            'attraction_options': forms.Textarea(attrs={'rows': 9, 'cols': 60}),
            'attraction_options_hi': forms.Textarea(attrs={'rows': 9, 'cols': 60}),
            'heard_from_options': forms.Textarea(attrs={'rows': 8, 'cols': 60}),
            'heard_from_options_hi': forms.Textarea(attrs={'rows': 8, 'cols': 60}),
            'attended_meet_greet_options': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
            'attended_meet_greet_options_hi': forms.Textarea(attrs={'rows': 4, 'cols': 60}),
            'excitement_options': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'excitement_options_hi': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'presence_made_exciting_options': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'presence_made_exciting_options_hi': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'enjoy_meet_greet_options': forms.Textarea(attrs={'rows': 8, 'cols': 60}),
            'enjoy_meet_greet_options_hi': forms.Textarea(attrs={'rows': 8, 'cols': 60}),
            'college_knowledge_options': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
            'college_knowledge_options_hi': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
            'learned_options': forms.Textarea(attrs={'rows': 10, 'cols': 60}),
            'learned_options_hi': forms.Textarea(attrs={'rows': 10, 'cols': 60}),
            'campus_impression_options': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'campus_impression_options_hi': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'another_celebrity_options': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'another_celebrity_options_hi': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'final_description_options': forms.Textarea(attrs={'rows': 7, 'cols': 60}),
            'final_description_options_hi': forms.Textarea(attrs={'rows': 7, 'cols': 60}),
            'contribution_areas_options': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
            'contribution_areas_options_hi': forms.Textarea(attrs={'rows': 5, 'cols': 60}),
        }

    def clean(self):
        cleaned = super().clean()
        # Soft validation: warn via error if Hindi option line counts mismatch English
        option_pairs = [
            ('visitor_type_options', 'visitor_type_options_hi'),
            ('attraction_options', 'attraction_options_hi'),
            ('heard_from_options', 'heard_from_options_hi'),
            ('attended_meet_greet_options', 'attended_meet_greet_options_hi'),
            ('excitement_options', 'excitement_options_hi'),
            ('presence_made_exciting_options', 'presence_made_exciting_options_hi'),
            ('enjoy_meet_greet_options', 'enjoy_meet_greet_options_hi'),
            ('college_knowledge_options', 'college_knowledge_options_hi'),
            ('learned_options', 'learned_options_hi'),
            ('campus_impression_options', 'campus_impression_options_hi'),
            ('another_celebrity_options', 'another_celebrity_options_hi'),
            ('final_description_options', 'final_description_options_hi'),
            ('contribution_areas_options', 'contribution_areas_options_hi'),
        ]
        for en_f, hi_f in option_pairs:
            en_text = cleaned.get(en_f) or ''
            hi_text = cleaned.get(hi_f) or ''
            en_lines = [ln for ln in en_text.splitlines() if ln.strip()]
            hi_lines = [ln for ln in hi_text.splitlines() if ln.strip()]
            if hi_lines and len(hi_lines) != len(en_lines):
                self.add_error(
                    hi_f,
                    f'Hindi list has {len(hi_lines)} line(s) but English has {len(en_lines)}. '
                    f'Keep the same number of lines in the same order.',
                )
        return cleaned


class EventFeedbackResponseForm(forms.ModelForm):
    """Dynamic form bound to a specific EventFeedbackCampaign."""

    attractions = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        label='What attracted you to this event?',
    )
    learned_experienced = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='What did you learn or experience during this event?',
    )
    contribution_areas = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='In which area would you like to contribute to the development of the college?',
    )

    class Meta:
        model = EventFeedbackResponse
        fields = [
            'name',
            'visitor_type',
            'institution_name',
            'city_village',
            'attractions',
            'heard_from',
            'overall_rating',
            'organization_rating',
            'hospitality_rating',
            'atmosphere_rating',
            'stage_programme_rating',
            'crowd_management_rating',
            'facilities_rating',
            'attended_meet_greet',
            'meet_greet_rating',
            'excitement_level',
            'presence_made_exciting',
            'enjoy_most_meet_greet',
            'college_knowledge',
            'learned_experienced',
            'campus_impression',
            'contribution_areas',
            'contribution_other_suggestion',
            'memorable_scale',
            'attend_future_scale',
            'recommend_events_scale',
            'another_celebrity_meet',
            'best_part',
            'improvements',
            'message_for_guest',
            'additional_comments',
            'final_description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'visitor_type': forms.Select(attrs={'class': 'form-select'}),
            'institution_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional',
            }),
            'city_village': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional',
            }),
            'heard_from': forms.Select(attrs={'class': 'form-select'}),
            'overall_rating': forms.Select(attrs={'class': 'form-select'}),
            'organization_rating': forms.Select(attrs={'class': 'form-select'}),
            'hospitality_rating': forms.Select(attrs={'class': 'form-select'}),
            'atmosphere_rating': forms.Select(attrs={'class': 'form-select'}),
            'stage_programme_rating': forms.Select(attrs={'class': 'form-select'}),
            'crowd_management_rating': forms.Select(attrs={'class': 'form-select'}),
            'facilities_rating': forms.Select(attrs={'class': 'form-select'}),
            'attended_meet_greet': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'meet_greet_rating': forms.Select(attrs={'class': 'form-select'}),
            'excitement_level': forms.Select(attrs={'class': 'form-select'}),
            'presence_made_exciting': forms.Select(attrs={'class': 'form-select'}),
            'enjoy_most_meet_greet': forms.Select(attrs={'class': 'form-select'}),
            'college_knowledge': forms.Select(attrs={'class': 'form-select'}),
            'campus_impression': forms.Select(attrs={'class': 'form-select'}),
            'memorable_scale': forms.Select(attrs={'class': 'form-select'}),
            'attend_future_scale': forms.Select(attrs={'class': 'form-select'}),
            'recommend_events_scale': forms.Select(attrs={'class': 'form-select'}),
            'another_celebrity_meet': forms.Select(attrs={'class': 'form-select'}),
            'best_part': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about your favourite moment or experience…',
            }),
            'improvements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your suggestions help us improve…',
            }),
            'message_for_guest': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share a message or memorable experience…',
            }),
            'additional_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional',
            }),
            'contribution_other_suggestion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional',
            }),
            'final_description': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, campaign=None, lang='en', **kwargs):
        super().__init__(*args, **kwargs)
        self.campaign = campaign
        self.lang = normalize_lang(lang)
        if campaign is None:
            return

        ui = get_ui(self.lang)
        copy = localized_campaign_copy(campaign, self.lang)
        guest = copy['guest']
        event_name = copy['event_name']
        fl = lambda key: field_label(key, self.lang, guest=guest, event=event_name)

        # Multi-choice options from campaign (values stay English; labels from admin Hindi fields)
        self.fields['attractions'] = forms.MultipleChoiceField(
            choices=campaign_choice_pairs(campaign, 'attraction_options', self.lang),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            required=True,
            label=fl('attractions'),
        )
        self.fields['learned_experienced'] = forms.MultipleChoiceField(
            choices=campaign_choice_pairs(campaign, 'learned_options', self.lang),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            required=False,
            label=fl('learned_experienced'),
        )
        self.fields['contribution_areas'] = forms.MultipleChoiceField(
            choices=campaign_choice_pairs(campaign, 'contribution_areas_options', self.lang),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            required=False,
            label=fl('contribution_areas'),
        )

        def set_choice(name, options_field, required=True, radio=False, include_blank=True):
            opts = campaign_choice_pairs(campaign, options_field, self.lang)
            if radio or not include_blank:
                choices = opts
            else:
                choices = [('', ui['select'])] + opts
            widget = (
                forms.RadioSelect(attrs={'class': 'form-check-input'})
                if radio
                else forms.Select(attrs={'class': 'form-select'})
            )
            self.fields[name] = forms.ChoiceField(
                choices=choices,
                required=required,
                widget=widget,
                label=fl(name),
            )

        set_choice('visitor_type', 'visitor_type_options')
        set_choice('heard_from', 'heard_from_options')
        set_choice(
            'attended_meet_greet',
            'attended_meet_greet_options',
            required=campaign.show_meet_greet_section,
            radio=True,
        )
        set_choice(
            'excitement_level',
            'excitement_options',
            required=campaign.show_meet_greet_section,
        )
        set_choice(
            'presence_made_exciting',
            'presence_made_exciting_options',
            required=campaign.show_meet_greet_section,
        )
        set_choice('enjoy_most_meet_greet', 'enjoy_meet_greet_options', required=False)
        set_choice(
            'college_knowledge',
            'college_knowledge_options',
            required=campaign.show_college_experience_section,
        )
        set_choice(
            'campus_impression',
            'campus_impression_options',
            required=campaign.show_college_experience_section,
        )
        set_choice(
            'another_celebrity_meet',
            'another_celebrity_options',
            required=campaign.show_event_impact_section,
        )
        set_choice('final_description', 'final_description_options', required=True)

        star_choices = star_rating_choices(self.lang)

        def set_int_choice(name, choices, blank_label, required=True):
            full = [('', blank_label)] + list(choices)
            self.fields[name] = forms.TypedChoiceField(
                choices=full,
                coerce=lambda v: int(v) if v not in (None, '') else None,
                empty_value=None,
                required=required,
                widget=forms.Select(attrs={'class': 'form-select'}),
                label=fl(name) if name in (
                    'overall_rating', 'organization_rating', 'hospitality_rating',
                    'atmosphere_rating', 'stage_programme_rating', 'crowd_management_rating',
                    'facilities_rating', 'meet_greet_rating', 'memorable_scale',
                    'attend_future_scale', 'recommend_events_scale',
                ) else name,
            )

        rating_fields = (
            'overall_rating',
            'organization_rating',
            'hospitality_rating',
            'atmosphere_rating',
            'stage_programme_rating',
            'crowd_management_rating',
            'facilities_rating',
        )
        for fname in rating_fields:
            set_int_choice(fname, star_choices, ui['select_rating'], required=True)

        set_int_choice(
            'meet_greet_rating',
            star_choices,
            ui['select_rating_optional'],
            required=False,
        )

        for fname in ('memorable_scale', 'attend_future_scale', 'recommend_events_scale'):
            set_int_choice(
                fname,
                SCALE_CHOICES,
                ui['select_scale'],
                required=campaign.show_event_impact_section,
            )

        # Labels & placeholders
        for key in (
            'name', 'visitor_type', 'institution_name', 'city_village', 'attractions',
            'heard_from', 'overall_rating', 'organization_rating', 'hospitality_rating',
            'atmosphere_rating', 'stage_programme_rating', 'crowd_management_rating',
            'facilities_rating', 'attended_meet_greet', 'meet_greet_rating',
            'excitement_level', 'presence_made_exciting', 'enjoy_most_meet_greet',
            'college_knowledge', 'learned_experienced', 'campus_impression',
            'contribution_areas', 'contribution_other_suggestion',
            'memorable_scale', 'attend_future_scale', 'recommend_events_scale',
            'another_celebrity_meet', 'best_part', 'improvements', 'message_for_guest',
            'additional_comments', 'final_description',
        ):
            if key in self.fields:
                self.fields[key].label = fl(key)

        self.fields['name'].widget.attrs['placeholder'] = ui['placeholder_name']
        self.fields['institution_name'].widget.attrs['placeholder'] = ui['placeholder_optional']
        self.fields['city_village'].widget.attrs['placeholder'] = ui['placeholder_optional']
        self.fields['best_part'].widget.attrs['placeholder'] = ui['placeholder_best']
        self.fields['improvements'].widget.attrs['placeholder'] = ui['placeholder_improve']
        self.fields['message_for_guest'].widget.attrs['placeholder'] = ui['placeholder_message']
        self.fields['additional_comments'].widget.attrs['placeholder'] = ui['placeholder_optional']
        self.fields['contribution_other_suggestion'].widget.attrs['placeholder'] = ui['placeholder_optional']
        self.fields['contribution_other_suggestion'].required = False

        # Hide / relax fields for disabled sections
        if not campaign.show_meet_greet_section:
            for f in (
                'attended_meet_greet',
                'meet_greet_rating',
                'excitement_level',
                'presence_made_exciting',
                'enjoy_most_meet_greet',
            ):
                self.fields[f].required = False
                self.fields[f].widget = forms.HiddenInput()

        if not campaign.show_college_experience_section:
            for f in (
                'college_knowledge',
                'learned_experienced',
                'campus_impression',
                'contribution_areas',
                'contribution_other_suggestion',
            ):
                self.fields[f].required = False
                if f in ('learned_experienced', 'contribution_areas'):
                    self.fields[f].widget = forms.MultipleHiddenInput()
                else:
                    self.fields[f].widget = forms.HiddenInput()

        if not campaign.show_event_impact_section:
            for f in (
                'memorable_scale',
                'attend_future_scale',
                'recommend_events_scale',
                'another_celebrity_meet',
            ):
                self.fields[f].required = False
                self.fields[f].widget = forms.HiddenInput()

        if not campaign.show_voice_section:
            for f in ('best_part', 'improvements', 'message_for_guest', 'additional_comments'):
                self.fields[f].required = False
                self.fields[f].widget = forms.HiddenInput()

        # Prefill multi-select from instance
        if self.instance and self.instance.pk:
            if self.instance.attractions:
                self.initial['attractions'] = [
                    v.strip() for v in self.instance.attractions.split(',') if v.strip()
                ]
            if self.instance.learned_experienced:
                self.initial['learned_experienced'] = [
                    v.strip() for v in self.instance.learned_experienced.split(',') if v.strip()
                ]
            if self.instance.contribution_areas:
                self.initial['contribution_areas'] = [
                    v.strip() for v in self.instance.contribution_areas.split(',') if v.strip()
                ]

    def clean_attractions(self):
        values = self.cleaned_data.get('attractions') or []
        if not values:
            msg = (
                'कृपया कम से कम एक विकल्प चुनें।'
                if self.lang == 'hi'
                else 'Please select at least one option.'
            )
            raise forms.ValidationError(msg)
        return ','.join(values)

    def clean_learned_experienced(self):
        values = self.cleaned_data.get('learned_experienced') or []
        return ','.join(values) if values else ''

    def clean_contribution_areas(self):
        values = self.cleaned_data.get('contribution_areas') or []
        return ','.join(values) if values else ''

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self.campaign is not None:
            obj.campaign = self.campaign
        if commit:
            obj.save()
        return obj
