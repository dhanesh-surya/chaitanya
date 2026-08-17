"""
English / Hindi UI strings and option labels for event feedback forms.
Submitted answers keep the English option value for consistent admin reports.
"""

SUPPORTED_LANGS = ('en', 'hi')
DEFAULT_LANG = 'en'
SESSION_KEY = 'event_feedback_lang'


# ---------------------------------------------------------------------------
# Option value (English) → Hindi display label
# ---------------------------------------------------------------------------
OPTION_HI = {
    # Visitor type
    'School Student': 'विद्यालय छात्र/छात्रा',
    'College Student': 'महाविद्यालय छात्र/छात्रा',
    'Graduate / Postgraduate': 'स्नातक / स्नातकोत्तर',
    'Parent / Guardian': 'अभिभावक / संरक्षक',
    'Alumni': 'पूर्व छात्र/छात्रा',
    'Local Visitor': 'स्थानीय आगंतुक',
    'Other': 'अन्य',

    # Attractions
    'Meet & Greet with Mann Qureshi': 'मान कुरैशी से मिलना-जुलना',
    'Meet & Greet with celebrity / guest': 'सेलिब्रिटी / अतिथि से मिलना-जुलना',
    'Admission / Course Information': 'प्रवेश / पाठ्यक्रम की जानकारी',
    'College Campus Visit': 'कॉलेज कैंपस दर्शन',
    'Entertainment & Activities': 'मनोरंजन और गतिविधियाँ',
    'Friends / Family': 'मित्र / परिवार',
    'Social Media Promotion': 'सोशल मीडिया प्रचार',
    'College Invitation': 'कॉलेज का निमंत्रण',

    # Heard from
    'Instagram / Facebook / Social Media': 'इंस्टाग्राम / फेसबुक / सोशल मीडिया',
    'WhatsApp': 'व्हाट्सऐप',
    'School / College': 'विद्यालय / महाविद्यालय',
    'Posters / Banners': 'पोस्टर / बैनर',
    'College Staff / Students': 'कॉलेज स्टाफ / छात्र',

    # Attend meet & greet
    'Yes': 'हाँ',
    'No': 'नहीं',
    'I watched from the audience': 'मैं दर्शकों में से देख रहा/रही था/थी',

    # Excitement
    'Extremely Excited': 'अत्यंत उत्साहित',
    'Very Excited': 'बहुत उत्साहित',
    'Excited': 'उत्साहित',
    'Somewhat Excited': 'कुछ हद तक उत्साहित',
    'Neutral': 'तटस्थ',

    # Presence made exciting
    'Definitely Yes': 'बिल्कुल हाँ',
    'Somewhat': 'कुछ हद तक',
    'Not Much': 'ज्यादा नहीं',

    # Enjoy meet & greet
    'Seeing Mann Qureshi in person': 'मान कुरैशी को आमने-सामने देखना',
    'Seeing the guest in person': 'अतिथि को आमने-सामने देखना',
    'Meeting / interacting with him': 'उनसे मिलना / बातचीत करना',
    'Meeting / interacting with them': 'उनसे मिलना / बातचीत करना',
    'Taking photos / selfies': 'फोटो / सेल्फी लेना',
    'Stage interaction': 'मंच पर बातचीत',
    'Overall atmosphere': 'समग्र माहौल',
    'Being part of the crowd': 'भीड़ का हिस्सा बनना',

    # College knowledge
    'Yes, a lot': 'हाँ, बहुत कुछ',
    'Yes, somewhat': 'हाँ, कुछ हद तक',
    'A little': 'थोड़ा सा',
    'Not really': 'खास नहीं',

    # Learned
    'Courses & Programmes': 'पाठ्यक्रम और कार्यक्रम',
    'College Facilities': 'कॉलेज सुविधाएँ',
    'Admission Process': 'प्रवेश प्रक्रिया',
    'Scholarships': 'छात्रवृत्तियाँ',
    'Campus Environment': 'कैंपस वातावरण',
    'Faculty & Student Interaction': 'फैकल्टी और छात्र संवाद',
    'Career Opportunities': 'करियर के अवसर',
    'Cultural / Student Activities': 'सांस्कृतिक / छात्र गतिविधियाँ',
    'I mainly attended the event': 'मैं मुख्य रूप से कार्यक्रम में शामिल हुआ/हुई',

    # Contribution areas
    'Financial assistance for needy students': 'निर्धन छात्रों हेतु आर्थिक सहायता',
    'Subject expert / mentor': 'विषय विशेषज्ञ / मार्गदर्शक',
    'Support for library enrichment': 'पुस्तकालय संवर्धन हेतु सहयोग',
    'Other suggestions for development': 'विकास हेतु अन्य कोई सुझाव',

    # Campus impression / final
    'Excellent': 'उत्कृष्ट',
    'Very Good': 'बहुत अच्छा',
    'Good': 'अच्छा',
    'Average': 'औसत',
    'Needs Improvement': 'सुधार की आवश्यकता',
    'Amazing – Loved It!': 'शानदार – बहुत पसंद आया!',

    # Another celebrity
    'Definitely Yes!': 'बिल्कुल हाँ!',
    'Maybe': 'शायद',
    'Not Sure': 'पक्का नहीं',
}

# Star / scale choice labels
STAR_RATING_HI = {
    5: '5 – उत्कृष्ट',
    4: '4 – बहुत अच्छा',
    3: '3 – अच्छा',
    2: '2 – औसत',
    1: '1 – कमजोर',
}

STAR_RATING_EN = {
    5: '5 – Excellent',
    4: '4 – Very Good',
    3: '3 – Good',
    2: '2 – Fair',
    1: '1 – Poor',
}


# ---------------------------------------------------------------------------
# UI chrome (section titles, buttons, helpers)
# ---------------------------------------------------------------------------
UI = {
    'en': {
        'choose_language': 'Choose your language',
        'english': 'English',
        'hindi': 'हिन्दी',
        'section_about': 'Tell Us About Yourself',
        'section_about_help': 'Just a few details before you share your experience.',
        'section_experience': 'Your Event Experience',
        'section_experience_help': 'Tell us what brought you here.',
        'section_rate': 'Rate Your Experience',
        'section_rate_help': '1 = Poor · 5 = Excellent',
        'section_meet_greet': 'Meet & Greet',
        'section_meet_greet_help': 'Tell us about your experience of the special Meet & Greet.',
        'section_college': 'Your College Experience',
        'section_college_help': 'This event is also an opportunity to explore our college.',
        'section_contribution': 'Contribute to College Development',
        'section_contribution_help': (
            'In which area would you like to contribute to the development of the college?'
        ),
        'section_impression': 'Your Overall Impression',
        'section_impression_help': 'Rate on a scale of 1 (low) to 5 (high).',
        'section_voice': 'Your Voice Matters',
        'section_voice_help': 'Share your thoughts and help us make our next event even better.',
        'section_final': 'Final Question',
        'select_all': 'Select all that apply',
        'select_all_optional': 'Select all that apply (optional)',
        'optional': 'Optional',
        'optional_if_not_attend': 'Optional if you did not attend',
        'submit': 'Submit Feedback',
        'all_forms': 'All event feedback forms',
        'required_mark': '*',
        'scale_memorable': '1 = Not Memorable · 5 = Extremely Memorable',
        'scale_likely': '1 = Not Likely · 5 = Definitely',
        'select': '— Select —',
        'select_rating': '— Select rating —',
        'select_rating_optional': '— Select rating (optional if you did not attend) —',
        'select_scale': '— Select 1–5 —',
        'placeholder_name': 'Enter your full name',
        'placeholder_optional': 'Optional',
        'placeholder_best': 'Tell us about your favourite moment or experience…',
        'placeholder_improve': 'Your suggestions help us improve…',
        'placeholder_message': 'Share a message or memorable experience…',
        'form_closed': 'This feedback form is currently closed.',
        'institution_hi_fallback': 'चैतन्य साइंस एंड आर्ट्स कॉलेज, पामगढ़',
        'accreditation_hi_fallback': "स्वायत्त संस्था | NAAC ग्रेड 'A' मान्यता प्राप्त",
    },
    'hi': {
        'choose_language': 'अपनी भाषा चुनें',
        'english': 'English',
        'hindi': 'हिन्दी',
        'section_about': 'अपने बारे में बताएँ',
        'section_about_help': 'अपना अनुभव साझा करने से पहले कुछ विवरण दें।',
        'section_experience': 'आपका कार्यक्रम अनुभव',
        'section_experience_help': 'बताएँ कि आप यहाँ क्यों आए।',
        'section_rate': 'अपने अनुभव को रेट करें',
        'section_rate_help': '1 = कमजोर · 5 = उत्कृष्ट',
        'section_meet_greet': 'मिलना-जुलना (Meet & Greet)',
        'section_meet_greet_help': 'विशेष मिलना-जुलना कार्यक्रम के अपने अनुभव के बारे में बताएँ।',
        'section_college': 'आपका कॉलेज अनुभव',
        'section_college_help': 'यह कार्यक्रम हमारे कॉलेज को जानने का भी अवसर है।',
        'section_contribution': 'महाविद्यालय विकास में योगदान',
        'section_contribution_help': (
            'महाविद्यालय के विकास में आप किस क्षेत्र में अपना योगदान देना चाहेंगे?'
        ),
        'section_impression': 'आपकी समग्र छाप',
        'section_impression_help': '1 (कम) से 5 (अधिक) के पैमाने पर रेट करें।',
        'section_voice': 'आपकी राय महत्वपूर्ण है',
        'section_voice_help': 'अपने विचार साझा करें और हमें अगला कार्यक्रम और बेहतर बनाने में मदद करें।',
        'section_final': 'अंतिम प्रश्न',
        'select_all': 'सभी लागू विकल्प चुनें',
        'select_all_optional': 'सभी लागू विकल्प चुनें (वैकल्पिक)',
        'optional': 'वैकल्पिक',
        'optional_if_not_attend': 'यदि आप शामिल नहीं हुए तो वैकल्पिक',
        'submit': 'प्रतिक्रिया भेजें',
        'all_forms': 'सभी कार्यक्रम प्रतिक्रिया फॉर्म',
        'required_mark': '*',
        'scale_memorable': '1 = यादगार नहीं · 5 = अत्यंत यादगार',
        'scale_likely': '1 = संभावना नहीं · 5 = निश्चित रूप से',
        'select': '— चुनें —',
        'select_rating': '— रेटिंग चुनें —',
        'select_rating_optional': '— रेटिंग चुनें (यदि शामिल नहीं हुए तो वैकल्पिक) —',
        'select_scale': '— 1–5 चुनें —',
        'placeholder_name': 'अपना पूरा नाम लिखें',
        'placeholder_optional': 'वैकल्पिक',
        'placeholder_best': 'अपना पसंदीदा क्षण या अनुभव बताएँ…',
        'placeholder_improve': 'आपके सुझाव हमें सुधारने में मदद करते हैं…',
        'placeholder_message': 'संदेश या यादगार अनुभव साझा करें…',
        'form_closed': 'यह प्रतिक्रिया फॉर्म फिलहाल बंद है।',
        'institution_hi_fallback': 'चैतन्य साइंस एंड आर्ट्स कॉलेज, पामगढ़',
        'accreditation_hi_fallback': "स्वायत्त संस्था | NAAC ग्रेड 'A' मान्यता प्राप्त",
    },
}

# Field label templates: {guest}, {event}
FIELD_LABELS = {
    'en': {
        'name': 'Your Name',
        'visitor_type': 'You are a',
        'institution_name': 'School / College / Institution Name',
        'city_village': 'City / Village',
        'attractions': 'What attracted you to {event}?',
        'heard_from': 'How did you hear about {event}?',
        'overall_rating': 'Overall, how would you rate {event}?',
        'organization_rating': 'How would you rate the organization of the event?',
        'hospitality_rating': 'How would you rate the welcome and hospitality?',
        'atmosphere_rating': 'How would you rate the event atmosphere?',
        'stage_programme_rating': 'How would you rate the stage and programme arrangements?',
        'crowd_management_rating': 'How satisfied were you with the crowd management?',
        'facilities_rating': 'How would you rate the overall facilities provided during the event?',
        'attended_meet_greet': 'Did you attend the {guest} Meet & Greet?',
        'meet_greet_rating': 'How would you rate your overall {guest} Meet & Greet experience?',
        'excitement_level': 'How excited were you to see {guest} at {event}?',
        'presence_made_exciting': "Did {guest}'s presence make {event} more exciting?",
        'enjoy_most_meet_greet': 'What did you enjoy most about the Meet & Greet?',
        'college_knowledge': 'Did this event help you know more about Chaitanya Science and Arts College?',
        'learned_experienced': 'What did you learn or experience during {event}?',
        'campus_impression': 'How was your overall impression of the college campus?',
        'contribution_areas': (
            'In which area would you like to contribute to the development of the college?'
        ),
        'contribution_other_suggestion': 'Any other suggestion for college development?',
        'memorable_scale': 'How memorable was {event} for you?',
        'attend_future_scale': 'How likely are you to attend future events organized by our college?',
        'recommend_events_scale': 'How likely are you to recommend our college events to your friends?',
        'another_celebrity_meet': 'Would you like to attend another celebrity Meet & Greet at our college?',
        'best_part': 'What was the BEST part of {event}?',
        'improvements': 'What could we improve in our future events?',
        'message_for_guest': 'Any message for {guest}?',
        'additional_comments': 'Any other comments or suggestions?',
        'final_description': 'Finally, how would you describe {event}?',
    },
    'hi': {
        'name': 'आपका नाम',
        'visitor_type': 'आप हैं',
        'institution_name': 'विद्यालय / महाविद्यालय / संस्थान का नाम',
        'city_village': 'शहर / गाँव',
        'attractions': 'आप {event} की ओर क्यों आकर्षित हुए?',
        'heard_from': 'आपने {event} के बारे में कैसे जाना?',
        'overall_rating': 'कुल मिलाकर, आप {event} को कैसे रेट करेंगे?',
        'organization_rating': 'आप कार्यक्रम के आयोजन को कैसे रेट करेंगे?',
        'hospitality_rating': 'आप स्वागत और आतिथ्य को कैसे रेट करेंगे?',
        'atmosphere_rating': 'आप कार्यक्रम के माहौल को कैसे रेट करेंगे?',
        'stage_programme_rating': 'आप मंच और कार्यक्रम व्यवस्था को कैसे रेट करेंगे?',
        'crowd_management_rating': 'भीड़ प्रबंधन से आप कितने संतुष्ट थे?',
        'facilities_rating': 'कार्यक्रम के दौरान दी गई समग्र सुविधाओं को कैसे रेट करेंगे?',
        'attended_meet_greet': 'क्या आप {guest} के Meet & Greet में शामिल हुए?',
        'meet_greet_rating': 'आपने {guest} Meet & Greet अनुभव को कैसे रेट किया?',
        'excitement_level': '{event} में {guest} को देखकर आप कितने उत्साहित थे?',
        'presence_made_exciting': 'क्या {guest} की उपस्थिति ने {event} को और रोमांचक बनाया?',
        'enjoy_most_meet_greet': 'Meet & Greet में आपको सबसे अधिक क्या पसंद आया?',
        'college_knowledge': 'क्या इस कार्यक्रम से आपको चैतन्य साइंस एंड आर्ट्स कॉलेज के बारे में अधिक जानकारी मिली?',
        'learned_experienced': '{event} के दौरान आपने क्या जाना या अनुभव किया?',
        'campus_impression': 'कॉलेज कैंपस के बारे में आपकी समग्र छाप कैसी रही?',
        'contribution_areas': (
            'महाविद्यालय के विकास में आप किस क्षेत्र में अपना योगदान देना चाहेंगे?'
        ),
        'contribution_other_suggestion': 'विकास हेतु अन्य कोई सुझाव (विवरण)',
        'memorable_scale': '{event} आपके लिए कितना यादगार रहा?',
        'attend_future_scale': 'हमारे कॉलेज द्वारा आयोजित भविष्य के कार्यक्रमों में भाग लेने की संभावना कितनी है?',
        'recommend_events_scale': 'आप अपने मित्रों को हमारे कॉलेज कार्यक्रमों की सिफारिश कितनी संभावना से करेंगे?',
        'another_celebrity_meet': 'क्या आप हमारे कॉलेज में एक और सेलिब्रिटी Meet & Greet में भाग लेना चाहेंगे?',
        'best_part': '{event} का सबसे अच्छा हिस्सा क्या था?',
        'improvements': 'हम भविष्य के कार्यक्रमों में क्या सुधार कर सकते हैं?',
        'message_for_guest': '{guest} के लिए कोई संदेश?',
        'additional_comments': 'कोई अन्य टिप्पणी या सुझाव?',
        'final_description': 'अंत में, आप {event} का वर्णन कैसे करेंगे?',
    },
}

# Default Hindi campaign copy for Admission Fest (fallback if DB fields empty)
DEFAULT_CAMPAIGN_HI = {
    'admission-fest-2026': {
        'title': 'एडमिशन फेस्ट 2026 – प्रतिक्रिया फॉर्म',
        'subtitle': 'छत्तीसगढ़ सुपरस्टार मान कुरैशी के साथ विशेष मिलना-जुलना',
        'intro_text': (
            'एडमिशन फेस्ट 2026 का हिस्सा बनने के लिए धन्यवाद!\n\n'
            'हमें आशा है कि आपने उत्सव और छत्तीसगढ़ सुपरस्टार मान कुरैशी से '
            'मिलने के विशेष अवसर का आनंद लिया।\n\n'
            'आपकी प्रतिक्रिया हमारे लिए महत्वपूर्ण है। कृपया एक मिनट निकालकर '
            'अपना अनुभव साझा करें और हमारे भविष्य के कार्यक्रमों को और बेहतर बनाने में मदद करें।'
        ),
        'confirmation_message': (
            'आपकी प्रतिक्रिया के लिए धन्यवाद!\n\n'
            'हमें खुशी है कि आप एडमिशन फेस्ट 2026 का हिस्सा बने।\n\n'
            'आपकी प्रतिक्रिया हमें भविष्य में और बेहतर कार्यक्रम आयोजित करने में मदद करेगी।\n\n'
            'चैतन्य साइंस एंड आर्ट्स कॉलेज, पामगढ़\n'
            '✨ सीखें • बढ़ें • हासिल करें ✨'
        ),
        'event_name': 'एडमिशन फेस्ट 2026',
        'guest': 'मान कुरैशी',
        'institution_line': 'चैतन्य साइंस एंड आर्ट्स कॉलेज, पामगढ़',
        'accreditation_line': "स्वायत्त संस्था | NAAC ग्रेड 'A' मान्यता प्राप्त",
        'tagline': '✨ सीखें • बढ़ें • हासिल करें ✨',
    },
}


def normalize_lang(lang):
    if not lang:
        return DEFAULT_LANG
    lang = str(lang).lower().strip()
    if lang in ('hi', 'hindi', 'hin'):
        return 'hi'
    return 'en'


def get_ui(lang):
    lang = normalize_lang(lang)
    return UI.get(lang, UI['en'])


def translate_option(value, lang):
    """Return display label for an English option value."""
    lang = normalize_lang(lang)
    if lang != 'hi':
        return value
    return OPTION_HI.get(value, value)


def choice_pairs_localized(options, lang, hindi_labels=None):
    """
    [(english_value, display_label), ...]
    - options: English values (one per line from admin)
    - hindi_labels: optional parallel list from admin Hindi fields
    - falls back to OPTION_HI dict, then English
    """
    lang = normalize_lang(lang)
    hi_list = list(hindi_labels or [])
    pairs = []
    for idx, opt in enumerate(options):
        # Support "English||Hindi" legacy format in a single English line
        if '||' in opt:
            en, hi = opt.split('||', 1)
            en, hi = en.strip(), hi.strip()
            if not en:
                continue
            label = hi if lang == 'hi' and hi else en
            pairs.append((en, label))
            continue
        if lang == 'hi':
            if idx < len(hi_list) and hi_list[idx]:
                label = hi_list[idx]
            else:
                label = translate_option(opt, 'hi')
            pairs.append((opt, label))
        else:
            pairs.append((opt, opt))
    return pairs


def campaign_choice_pairs(campaign, options_field, lang):
    """Build choice pairs for a campaign option field (uses *_hi when lang=hi)."""
    en_opts = campaign.options(options_field)
    hi_opts = campaign.options_hi(options_field) if normalize_lang(lang) == 'hi' else []
    return choice_pairs_localized(en_opts, lang, hindi_labels=hi_opts)


def star_rating_choices(lang):
    lang = normalize_lang(lang)
    source = STAR_RATING_HI if lang == 'hi' else STAR_RATING_EN
    return [(k, v) for k, v in source.items()]


def field_label(key, lang, guest='', event=''):
    lang = normalize_lang(lang)
    template = FIELD_LABELS.get(lang, FIELD_LABELS['en']).get(key, key)
    return template.format(guest=guest, event=event)


def _hi_or_default(campaign, field_hi, defaults_key, english_value, defaults=None):
    """Prefer non-empty campaign Hindi field, then slug defaults, then English."""
    defaults = defaults or {}
    val = getattr(campaign, field_hi, None) or ''
    if str(val).strip():
        return val
    if defaults.get(defaults_key):
        return defaults[defaults_key]
    return english_value


def localized_campaign_copy(campaign, lang):
    """
    Return display dict for campaign header/messages in the selected language.
    Uses campaign Hindi DB fields if present, else DEFAULT_CAMPAIGN_HI by slug, else English.
    """
    lang = normalize_lang(lang)
    defaults = DEFAULT_CAMPAIGN_HI.get(campaign.slug, {})

    if lang == 'hi':
        title = _hi_or_default(campaign, 'title_hi', 'title', campaign.title, defaults)
        subtitle = _hi_or_default(campaign, 'subtitle_hi', 'subtitle', campaign.subtitle, defaults)
        intro = _hi_or_default(campaign, 'intro_text_hi', 'intro_text', campaign.intro_text, defaults)
        confirm = _hi_or_default(
            campaign, 'confirmation_message_hi', 'confirmation_message',
            campaign.confirmation_message, defaults,
        )
        institution = _hi_or_default(
            campaign, 'institution_line_hi', 'institution_line',
            campaign.institution_line or UI['hi']['institution_hi_fallback'], defaults,
        )
        accreditation = _hi_or_default(
            campaign, 'accreditation_line_hi', 'accreditation_line',
            campaign.accreditation_line or UI['hi']['accreditation_hi_fallback'], defaults,
        )
        tagline = _hi_or_default(campaign, 'tagline_hi', 'tagline', campaign.tagline, defaults)
        event_name = _hi_or_default(
            campaign, 'event_name_hi', 'event_name',
            title.replace(' – प्रतिक्रिया फॉर्म', '').replace(' – Feedback Form', ''),
            defaults,
        )
        guest = _hi_or_default(
            campaign, 'featured_guest_hi', 'guest', campaign.guest_display('hi'), defaults,
        )
    else:
        title = campaign.title
        subtitle = campaign.subtitle
        intro = campaign.intro_text
        confirm = campaign.confirmation_message
        institution = campaign.institution_line
        accreditation = campaign.accreditation_line
        tagline = campaign.tagline
        event_name = campaign.title.replace(' – Feedback Form', '').replace(' - Feedback Form', '')
        guest = campaign.guest_display('en')

    return {
        'title': title,
        'subtitle': subtitle,
        'intro_text': intro,
        'confirmation_message': confirm,
        'institution_line': institution,
        'accreditation_line': accreditation,
        'tagline': tagline,
        'event_name': event_name,
        'guest': guest,
    }


def resolve_lang_from_request(request):
    """GET ?lang=hi|en overrides session; otherwise session or default."""
    lang = request.GET.get('lang') or request.POST.get('lang')
    if lang:
        lang = normalize_lang(lang)
        request.session[SESSION_KEY] = lang
        return lang
    return normalize_lang(request.session.get(SESSION_KEY, DEFAULT_LANG))
