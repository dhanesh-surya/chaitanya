"""
Participation certificate PDF for event feedback submissions.
College header: logos, name, affiliation & address from SiteSettings.

Typography: English (Helvetica) is always used for a clean printable layout.
Optional Devanagari (Nirmala / system fonts) is used only when registered successfully.
"""

from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.http import HttpResponse
from django.utils import timezone


# Registered once per process
_FONT_CACHE = {
    'regular': 'Helvetica',
    'bold': 'Helvetica-Bold',
    'italic': 'Helvetica-Oblique',
    'hindi': None,  # optional Devanagari-capable face
    'ready': False,
}


def _safe_path(file_field):
    if not file_field:
        return None
    try:
        path = file_field.path
        if path and Path(path).is_file():
            return path
    except (ValueError, NotImplementedError, OSError):
        pass
    return None


def _static_path(relative):
    try:
        found = find(relative)
        if found and Path(found).is_file():
            return found
    except Exception:
        pass
    for base in (
        Path(settings.BASE_DIR) / 'static',
        Path(settings.BASE_DIR) / 'staticfiles',
    ):
        candidate = base / relative
        if candidate.is_file():
            return str(candidate)
    return None


def _register_fonts():
    """Register English + optional Hindi TTF/TTC fonts."""
    if _FONT_CACHE['ready']:
        return _FONT_CACHE

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    # Prefer common Windows Latin faces for slightly richer look; else Helvetica.
    latin_candidates = [
        (r'C:\Windows\Fonts\arial.ttf', 'CertArial', 'CertArialBold', r'C:\Windows\Fonts\arialbd.ttf'),
        (r'C:\Windows\Fonts\calibri.ttf', 'CertCalibri', 'CertCalibriBold', r'C:\Windows\Fonts\calibrib.ttf'),
    ]
    for regular_path, reg_name, bold_name, bold_path in latin_candidates:
        if Path(regular_path).is_file():
            try:
                if reg_name not in pdfmetrics.getRegisteredFontNames():
                    pdfmetrics.registerFont(TTFont(reg_name, regular_path))
                _FONT_CACHE['regular'] = reg_name
                if Path(bold_path).is_file():
                    if bold_name not in pdfmetrics.getRegisteredFontNames():
                        pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                    _FONT_CACHE['bold'] = bold_name
                else:
                    _FONT_CACHE['bold'] = reg_name
                _FONT_CACHE['italic'] = reg_name
                break
            except Exception:
                continue

    # Devanagari-capable fonts (Windows Nirmala is usually .ttc)
    hindi_candidates = [
        # (path, subfontIndex or None)
        (str(Path(settings.BASE_DIR) / 'static' / 'fonts' / 'NotoSansDevanagari-Regular.ttf'), None),
        (str(Path(settings.BASE_DIR) / 'feedback' / 'fonts' / 'NotoSansDevanagari-Regular.ttf'), None),
        (r'C:\Windows\Fonts\Nirmala.ttc', 0),
        (r'C:\Windows\Fonts\nirmala.ttc', 0),
        (r'C:\Windows\Fonts\Nirmala.ttf', None),
        (r'C:\Windows\Fonts\Mangal.ttf', None),
        (r'C:\Windows\Fonts\mangal.ttf', None),
        ('/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf', None),
        ('/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf', None),
        ('/usr/share/fonts/truetype/freefont/FreeSans.ttf', None),
    ]
    hindi_name = 'CertHindi'
    for path, sub_idx in hindi_candidates:
        if not Path(path).is_file():
            continue
        try:
            if hindi_name not in pdfmetrics.getRegisteredFontNames():
                if sub_idx is not None:
                    pdfmetrics.registerFont(TTFont(hindi_name, path, subfontIndex=sub_idx))
                else:
                    pdfmetrics.registerFont(TTFont(hindi_name, path))
            # Smoke-test: width of a Devanagari character must be > 0
            from reportlab.pdfbase.pdfmetrics import stringWidth
            w = stringWidth('चैतन्य', hindi_name, 12)
            if w and w > 1:
                _FONT_CACHE['hindi'] = hindi_name
                break
        except Exception:
            continue

    _FONT_CACHE['ready'] = True
    return _FONT_CACHE


def get_site_branding():
    """Load SiteSettings branding for the certificate header."""
    try:
        from core.models import SiteSettings
        site = SiteSettings.objects.first()
    except Exception:
        site = None

    defaults = {
        'name_en': 'Chaitanya Science and Arts College',
        'name_hi': 'चैतन्य विज्ञान एवं कला महाविद्यालय, पामगढ़',
        'tagline': "An Autonomous College, Approved by UGC | Accredited with Grade 'A' by NAAC",
        'address1': 'PAMGARH, JANJGIR-CHAMPA (C.G.), 495554',
        'address2': 'Affiliated to Shaheed Nandkumar Patel Vishwavidyalaya, Raigarh',
        'phone': '',
        'email': '',
        'established': 2001,
        'logo': _static_path('assets/csac_pmg.svg'),
        'logo_naac': _static_path('assets/images/logo_naac_a.png'),
        'logo3': _static_path('assets/images/logo_2.png'),
        'logo4': _static_path('assets/images/logo_3.png'),
        'logo5': _static_path('assets/images/logo_4.png'),
    }

    if not site:
        return defaults

    return {
        'name_en': site.college_name_en or defaults['name_en'],
        'name_hi': site.college_name_hi or defaults['name_hi'],
        'tagline': site.tagline or defaults['tagline'],
        'address1': site.address_line1 or defaults['address1'],
        'address2': site.address_line2 or defaults['address2'],
        'phone': site.phone or '',
        'email': site.email or '',
        'established': site.established_year or 2001,
        'logo': _safe_path(site.college_logo) or defaults['logo'],
        'logo_naac': _safe_path(site.logo2) or defaults['logo_naac'],
        'logo3': _safe_path(site.logo3) or defaults['logo3'],
        'logo4': _safe_path(site.logo4) or defaults['logo4'],
        'logo5': _safe_path(site.logo5) or defaults['logo5'],
    }


def certificate_number(response):
    """Human-readable certificate ID, e.g. CSAC-ADMISSIONFE-00042-2026."""
    year = timezone.localtime(response.submitted_at).year if response.submitted_at else timezone.now().year
    slug = (response.campaign.slug if response.campaign_id else 'event')[:12].upper().replace('-', '')
    return f'CSAC-{slug}-{response.pk:05d}-{year}'


def _draw_image(c, path, center_x, center_y, max_w, max_h):
    """Draw raster image centered at (center_x, center_y). Skip SVG."""
    if not path:
        return False
    p = Path(path)
    if not p.is_file() or p.suffix.lower() == '.svg':
        return False
    try:
        from reportlab.lib.utils import ImageReader
        img = ImageReader(str(p))
        iw, ih = img.getSize()
        if not iw or not ih:
            return False
        scale = min(max_w / float(iw), max_h / float(ih))
        w, h = iw * scale, ih * scale
        c.drawImage(
            img,
            center_x - w / 2,
            center_y - h / 2,
            width=w,
            height=h,
            mask='auto',
            preserveAspectRatio=True,
        )
        return True
    except Exception:
        return False


def _has_devanagari(text):
    if not text:
        return False
    return any('\u0900' <= ch <= '\u097F' for ch in text)


def _draw_centred(c, text, x, y, font_en, font_hi, size, color_hex):
    """
    Draw centred text. Uses Hindi font only when text has Devanagari and font works.
    Falls back to English-safe rendering (skips pure Devanagari if no font).
    Returns True if something was drawn.
    """
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase.pdfmetrics import stringWidth

    if not text:
        return False
    text = str(text).strip()
    if not text:
        return False

    use_hi = font_hi and _has_devanagari(text)
    font = font_hi if use_hi else font_en

    # If text is pure/mostly Devanagari and we have no Hindi font, skip (avoid tofu boxes)
    if _has_devanagari(text) and not font_hi:
        return False

    try:
        c.setFillColor(HexColor(color_hex))
        c.setFont(font, size)
        c.drawCentredString(x, y, text)
        return True
    except Exception:
        try:
            c.setFont(font_en, size)
            c.drawCentredString(x, y, text)
            return True
        except Exception:
            return False


def build_participation_certificate_pdf(response, lang='en'):
    """
    Build a landscape A4 participation certificate PDF.
    Always renders a clean English certificate. Hindi is optional when fonts exist.
    College name is printed directly under the participant's name.
    """
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase.pdfmetrics import stringWidth

    fonts = _register_fonts()
    f_reg = fonts['regular']
    f_bold = fonts['bold']
    f_italic = fonts['italic']
    f_hi = fonts['hindi']

    brand = get_site_branding()
    campaign = response.campaign
    cert_no = certificate_number(response)

    submitted = response.submitted_at
    if submitted and timezone.is_aware(submitted):
        submitted = timezone.localtime(submitted)
    date_str = submitted.strftime('%d %B %Y') if submitted else timezone.now().strftime('%d %B %Y')

    # Always use English event/guest titles for reliable PDF text (no broken glyphs)
    event_title = (
        (campaign.title or '')
        .replace(' – Feedback Form', '')
        .replace(' - Feedback Form', '')
        .strip()
        or 'College Event'
    )
    guest = (campaign.featured_guest or '').strip()
    college_name = brand['name_en']

    buffer = BytesIO()
    page_w, page_h = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    # Outer border
    margin = 10 * mm
    c.setStrokeColor(HexColor('#E61013'))
    c.setLineWidth(2.5)
    c.rect(margin, margin, page_w - 2 * margin, page_h - 2 * margin)

    # Inner decorative border
    c.setLineWidth(0.6)
    c.setStrokeColor(HexColor('#C9A227'))
    inset = 13 * mm
    c.rect(inset, inset, page_w - 2 * inset, page_h - 2 * inset)

    # Corner ornaments
    c.setFillColor(HexColor('#C9A227'))
    for cx, cy in [
        (inset, inset),
        (page_w - inset - 4 * mm, inset),
        (inset, page_h - inset - 4 * mm),
        (page_w - inset - 4 * mm, page_h - inset - 4 * mm),
    ]:
        c.rect(cx, cy, 4 * mm, 4 * mm, fill=1, stroke=0)

    # ---------- Header ----------
    header_top = page_h - 18 * mm
    logo_size = 22 * mm
    left_x = 20 * mm
    right_logos_x = page_w - 20 * mm
    center_x = page_w / 2

    logo_drawn = _draw_image(
        c, brand['logo'],
        left_x + logo_size / 2,
        header_top - logo_size / 2 - 2 * mm,
        logo_size, logo_size,
    )
    if not logo_drawn:
        c.setFillColor(HexColor('#E61013'))
        c.setFont(f_bold, 14)
        c.drawCentredString(left_x + logo_size / 2, header_top - 12 * mm, 'CSAC')

    rlogo_size = 14 * mm
    rx = right_logos_x - rlogo_size / 2
    for path in (brand.get('logo_naac'), brand.get('logo3'), brand.get('logo4')):
        if path and _draw_image(c, path, rx, header_top - 10 * mm, rlogo_size, rlogo_size):
            rx -= rlogo_size + 3 * mm

    y = header_top - 2 * mm
    c.setFillColor(HexColor('#E61013'))
    c.setFont(f_bold, 15)
    c.drawCentredString(center_x, y, college_name)
    y -= 5 * mm

    c.setFillColor(HexColor('#333333'))
    c.setFont(f_reg, 8)
    c.drawCentredString(center_x, y, brand['tagline'])
    y -= 3.8 * mm
    c.setFont(f_italic, 8)
    c.drawCentredString(center_x, y, brand['address2'])
    y -= 3.5 * mm
    c.setFont(f_reg, 8)
    c.drawCentredString(center_x, y, brand['address1'])
    if brand.get('established'):
        y -= 3.3 * mm
        c.setFillColor(HexColor('#666666'))
        c.setFont(f_reg, 7)
        c.drawCentredString(center_x, y, f'Established {brand["established"]}')

    # Divider
    y -= 4 * mm
    c.setStrokeColor(HexColor('#E61013'))
    c.setLineWidth(1.2)
    c.line(25 * mm, y, page_w - 25 * mm, y)
    c.setStrokeColor(HexColor('#C9A227'))
    c.setLineWidth(0.5)
    c.line(25 * mm, y - 1.5 * mm, page_w - 25 * mm, y - 1.5 * mm)

    # ---------- Title ----------
    y -= 12 * mm
    c.setFillColor(HexColor('#E61013'))
    c.setFont(f_bold, 20)
    c.drawCentredString(center_x, y, 'CERTIFICATE OF PARTICIPATION')
    y -= 5 * mm
    c.setFillColor(HexColor('#C9A227'))
    c.setFont(f_reg, 9)
    c.drawCentredString(center_x, y, '*  *  *')

    # ---------- Body ----------
    y -= 11 * mm
    c.setFillColor(HexColor('#444444'))
    c.setFont(f_reg, 11)
    c.drawCentredString(center_x, y, 'This is to certify that')

    # Participant name
    y -= 10 * mm
    name = (response.name or 'Participant').strip()
    c.setFillColor(HexColor('#111111'))
    c.setFont(f_bold, 20)
    c.drawCentredString(center_x, y, name)
    name_w = stringWidth(name, f_bold, 20)
    c.setStrokeColor(HexColor('#E61013'))
    c.setLineWidth(0.9)
    c.line(center_x - name_w / 2 - 4, y - 2.2 * mm, center_x + name_w / 2 + 4, y - 2.2 * mm)

    # Visitor details just below student name (e.g. Graduate / Postgraduate · GRD College · Pamgarh)
    participant_meta = []
    if response.visitor_type:
        participant_meta.append(str(response.visitor_type).strip())
    if response.institution_name:
        participant_meta.append(str(response.institution_name).strip())
    if response.city_village:
        participant_meta.append(str(response.city_village).strip())
    if participant_meta:
        y -= 7 * mm
        c.setFillColor(HexColor('#555555'))
        c.setFont(f_reg, 10)
        c.drawCentredString(center_x, y, ' · '.join(participant_meta))

    # Host college name below participant details
    y -= 8 * mm
    c.setFillColor(HexColor('#E61013'))
    c.setFont(f_bold, 12)
    c.drawCentredString(center_x, y, college_name)
    y -= 4.5 * mm
    c.setFillColor(HexColor('#555555'))
    c.setFont(f_italic, 9)
    c.drawCentredString(center_x, y, brand['address1'])

    y -= 9 * mm
    c.setFillColor(HexColor('#333333'))
    c.setFont(f_reg, 11)
    c.drawCentredString(
        center_x, y,
        'has participated in / shared valuable feedback for',
    )

    y -= 8 * mm
    c.setFillColor(HexColor('#E61013'))
    c.setFont(f_bold, 13)
    c.drawCentredString(center_x, y, event_title)

    if guest:
        y -= 6 * mm
        c.setFillColor(HexColor('#444444'))
        c.setFont(f_italic, 11)
        c.drawCentredString(center_x, y, f'Special Meet & Greet with {guest}')

    y -= 9 * mm
    c.setFillColor(HexColor('#333333'))
    c.setFont(f_reg, 10)
    c.drawCentredString(
        center_x, y,
        'We appreciate your presence and valuable contribution to making this event a success.',
    )

    # ---------- Footer ----------
    footer_y = 28 * mm
    c.setStrokeColor(HexColor('#CCCCCC'))
    c.setLineWidth(0.5)
    c.line(30 * mm, footer_y + 14 * mm, page_w - 30 * mm, footer_y + 14 * mm)

    c.setFillColor(HexColor('#333333'))
    c.setFont(f_reg, 9)
    c.drawString(30 * mm, footer_y + 6 * mm, f'Date: {date_str}')
    c.drawRightString(page_w - 30 * mm, footer_y + 6 * mm, f'Certificate No: {cert_no}')

    contact = ' | '.join(p for p in [brand.get('phone'), brand.get('email')] if p)
    if contact:
        c.setFont(f_italic, 8)
        c.setFillColor(HexColor('#666666'))
        c.drawCentredString(center_x, footer_y - 1 * mm, contact)

    c.setFont(f_bold, 8)
    c.setFillColor(HexColor('#E61013'))
    c.drawCentredString(
        center_x, footer_y - 6 * mm,
        f'{college_name}  ·  Learn · Grow · Achieve',
    )

    # Signature
    sig_x = page_w - 70 * mm
    c.setStrokeColor(HexColor('#333333'))
    c.setLineWidth(0.6)
    c.line(sig_x - 25 * mm, footer_y + 6 * mm, sig_x + 25 * mm, footer_y + 6 * mm)
    c.setFont(f_reg, 8)
    c.setFillColor(HexColor('#333333'))
    c.drawCentredString(sig_x, footer_y + 1 * mm, 'Authorized Signatory')

    c.setTitle(f'Participation Certificate – {name}')
    c.setAuthor(college_name)
    c.setSubject(f'Certificate of Participation – {event_title}')
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def certificate_http_response(response, lang='en'):
    # lang kept for API compatibility; certificate body is English for font reliability
    pdf_bytes = build_participation_certificate_pdf(response, lang=lang)
    cert_no = certificate_number(response)
    safe_name = ''.join(ch if ch.isalnum() or ch in '-_' else '_' for ch in (response.name or 'participant'))[:40]
    filename = f'Participation_Certificate_{safe_name}_{cert_no}.pdf'
    http = HttpResponse(pdf_bytes, content_type='application/pdf')
    http['Content-Disposition'] = f'inline; filename="{filename}"'
    return http
