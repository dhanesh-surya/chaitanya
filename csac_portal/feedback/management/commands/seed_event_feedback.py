from django.core.management.base import BaseCommand
from feedback.models import EventFeedbackCampaign
from feedback.event_i18n import OPTION_HI


ADMISSION_FEST_INTRO = (
    "Thank you for being a part of Admission Fest 2026!\n\n"
    "We hope you enjoyed the celebration and the special opportunity "
    "to meet Chhattisgarh Superstar Mann Qureshi.\n\n"
    "Your feedback is valuable to us. Please take a minute to share "
    "your experience and help us make our future events even better."
)

ADMISSION_FEST_CONFIRM = (
    "Thank You for Your Feedback!\n\n"
    "We are delighted that you were a part of Admission Fest 2026.\n\n"
    "Your feedback will help us organize even better events in the future.\n\n"
    "Chaitanya Science and Arts College, Pamgarh\n"
    "✨ Learn • Grow • Achieve ✨"
)

ADMISSION_FEST_INTRO_HI = (
    'एडमिशन फेस्ट 2026 का हिस्सा बनने के लिए धन्यवाद!\n\n'
    'हमें आशा है कि आपने उत्सव और छत्तीसगढ़ सुपरस्टार मान कुरैशी से '
    'मिलने के विशेष अवसर का आनंद लिया।\n\n'
    'आपकी प्रतिक्रिया हमारे लिए महत्वपूर्ण है। कृपया एक मिनट निकालकर '
    'अपना अनुभव साझा करें और हमारे भविष्य के कार्यक्रमों को और बेहतर बनाने में मदद करें।'
)

ADMISSION_FEST_CONFIRM_HI = (
    'आपकी प्रतिक्रिया के लिए धन्यवाद!\n\n'
    'हमें खुशी है कि आप एडमिशन फेस्ट 2026 का हिस्सा बने।\n\n'
    'आपकी प्रतिक्रिया हमें भविष्य में और बेहतर कार्यक्रम आयोजित करने में मदद करेगी।\n\n'
    'चैतन्य साइंस एंड आर्ट्स कॉलेज, पामगढ़\n'
    '✨ सीखें • बढ़ें • हासिल करें ✨'
)


def _hi_lines(english_lines):
    """Map English option lines to Hindi using OPTION_HI (fallback = English)."""
    return '\n'.join(OPTION_HI.get(line, line) for line in english_lines)


def ensure_admission_fest_2026():
    visitor_en = [
        'School Student',
        'College Student',
        'Graduate / Postgraduate',
        'Parent / Guardian',
        'Alumni',
        'Local Visitor',
        'Other',
    ]
    attraction_en = [
        'Meet & Greet with Mann Qureshi',
        'Admission / Course Information',
        'College Campus Visit',
        'Entertainment & Activities',
        'Friends / Family',
        'Social Media Promotion',
        'College Invitation',
        'Other',
    ]
    heard_en = [
        'Instagram / Facebook / Social Media',
        'WhatsApp',
        'Friends / Family',
        'School / College',
        'Posters / Banners',
        'College Staff / Students',
        'Other',
    ]
    attended_en = [
        'Yes',
        'No',
        'I watched from the audience',
    ]
    excitement_en = [
        'Extremely Excited',
        'Very Excited',
        'Excited',
        'Somewhat Excited',
        'Neutral',
    ]
    presence_en = [
        'Definitely Yes',
        'Yes',
        'Somewhat',
        'Not Much',
        'No',
    ]
    enjoy_en = [
        'Seeing Mann Qureshi in person',
        'Meeting / interacting with him',
        'Taking photos / selfies',
        'Stage interaction',
        'Overall atmosphere',
        'Being part of the crowd',
        'Other',
    ]
    knowledge_en = [
        'Yes, a lot',
        'Yes, somewhat',
        'A little',
        'Not really',
    ]
    learned_en = [
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
    ]
    campus_en = [
        'Excellent',
        'Very Good',
        'Good',
        'Average',
        'Needs Improvement',
    ]
    celebrity_en = [
        'Definitely Yes!',
        'Yes',
        'Maybe',
        'Not Sure',
        'No',
    ]
    final_en = [
        'Amazing – Loved It!',
        'Excellent',
        'Very Good',
        'Good',
        'Average',
        'Needs Improvement',
    ]
    contribution_en = [
        'Financial assistance for needy students',
        'Subject expert / mentor',
        'Support for library enrichment',
        'Other suggestions for development',
    ]
    contribution_hi = [
        'निर्धन छात्रों हेतु आर्थिक सहायता',
        'विषय विशेषज्ञ / मार्गदर्शक',
        'पुस्तकालय संवर्धन हेतु सहयोग',
        'विकास हेतु अन्य कोई सुझाव',
    ]

    campaign, created = EventFeedbackCampaign.objects.update_or_create(
        slug='admission-fest-2026',
        defaults={
            'title': 'Admission Fest 2026 – Feedback Form',
            'menu_title': 'Admission Fest 2026 Feedback',
            'subtitle': 'Special Meet & Greet with Chhattisgarh Superstar Mann Qureshi',
            'featured_guest': 'Mann Qureshi',
            'institution_line': 'Chaitanya Science and Arts College, Pamgarh',
            'accreditation_line': "An Autonomous Institution | NAAC Accredited Grade 'A'",
            'intro_text': ADMISSION_FEST_INTRO,
            'confirmation_message': ADMISSION_FEST_CONFIRM,
            'tagline': '✨ Learn • Grow • Achieve ✨',
            # Hindi
            'title_hi': 'एडमिशन फेस्ट 2026 – प्रतिक्रिया फॉर्म',
            'menu_title_hi': 'एडमिशन फेस्ट 2026 प्रतिक्रिया',
            'subtitle_hi': 'छत्तीसगढ़ सुपरस्टार मान कुरैशी के साथ विशेष मिलना-जुलना',
            'featured_guest_hi': 'मान कुरैशी',
            'event_name_hi': 'एडमिशन फेस्ट 2026',
            'institution_line_hi': 'चैतन्य साइंस एंड आर्ट्स कॉलेज, पामगढ़',
            'accreditation_line_hi': "स्वायत्त संस्था | NAAC ग्रेड 'A' मान्यता प्राप्त",
            'intro_text_hi': ADMISSION_FEST_INTRO_HI,
            'confirmation_message_hi': ADMISSION_FEST_CONFIRM_HI,
            'tagline_hi': '✨ सीखें • बढ़ें • हासिल करें ✨',
            'is_active': True,
            'show_in_menu': True,
            'order': 1,
            'show_meet_greet_section': True,
            'show_college_experience_section': True,
            'show_event_impact_section': True,
            'show_voice_section': True,
            'visitor_type_options': '\n'.join(visitor_en),
            'visitor_type_options_hi': _hi_lines(visitor_en),
            'attraction_options': '\n'.join(attraction_en),
            'attraction_options_hi': _hi_lines(attraction_en),
            'heard_from_options': '\n'.join(heard_en),
            'heard_from_options_hi': _hi_lines(heard_en),
            'attended_meet_greet_options': '\n'.join(attended_en),
            'attended_meet_greet_options_hi': _hi_lines(attended_en),
            'excitement_options': '\n'.join(excitement_en),
            'excitement_options_hi': _hi_lines(excitement_en),
            'presence_made_exciting_options': '\n'.join(presence_en),
            'presence_made_exciting_options_hi': _hi_lines(presence_en),
            'enjoy_meet_greet_options': '\n'.join(enjoy_en),
            'enjoy_meet_greet_options_hi': _hi_lines(enjoy_en),
            'college_knowledge_options': '\n'.join(knowledge_en),
            'college_knowledge_options_hi': _hi_lines(knowledge_en),
            'learned_options': '\n'.join(learned_en),
            'learned_options_hi': _hi_lines(learned_en),
            'campus_impression_options': '\n'.join(campus_en),
            'campus_impression_options_hi': _hi_lines(campus_en),
            'another_celebrity_options': '\n'.join(celebrity_en),
            'another_celebrity_options_hi': _hi_lines(celebrity_en),
            'final_description_options': '\n'.join(final_en),
            'final_description_options_hi': _hi_lines(final_en),
            'contribution_areas_options': '\n'.join(contribution_en),
            'contribution_areas_options_hi': '\n'.join(contribution_hi),
        },
    )
    return campaign, created


class Command(BaseCommand):
    help = 'Seed default event feedback campaigns (Admission Fest 2026) with English + Hindi.'

    def handle(self, *args, **options):
        campaign, created = ensure_admission_fest_2026()
        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            f'{action}: {campaign.title} / {campaign.title_hi} → /feedback/events/{campaign.slug}/'
        ))
