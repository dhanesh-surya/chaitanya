from django.shortcuts import render
from .models import NAACDocument, IQACMember, NAACCriteria, NAACInfo


def naac_home(request):
    naac_info = NAACInfo.objects.first()
    general_docs = NAACDocument.objects.filter(doc_type='naac')
    metrics = NAACCriteria.objects.all().order_by('order', 'criterion_number')

    criteria_groups = [
        {'id': 'I', 'key': '1', 'name': 'Criterion I – Curricular Aspects', 'metrics': []},
        {'id': 'II', 'key': '2', 'name': 'Criterion II – Teaching-Learning and Evaluation', 'metrics': []},
        {'id': 'III', 'key': '3', 'name': 'Criterion III – Research, Innovations and Extension', 'metrics': []},
        {'id': 'IV', 'key': '4', 'name': 'Criterion IV – Infrastructure and Learning Resources', 'metrics': []},
        {'id': 'V', 'key': '5', 'name': 'Criterion V – Student Support and Progression', 'metrics': []},
        {'id': 'VI', 'key': '6', 'name': 'Criterion VI – Governance, Leadership and Management', 'metrics': []},
        {'id': 'VII', 'key': '7', 'name': 'Criterion VII – Institutional Values and Best Practices', 'metrics': []},
    ]

    group_map = {g['key']: g for g in criteria_groups}
    for metric in metrics:
        if metric.criterion in group_map:
            group_map[metric.criterion]['metrics'].append(metric)

    context = {
        'naac_info': naac_info,
        'general_docs': general_docs,
        'criteria_groups': criteria_groups,
        'page_title': 'NAAC',
        'breadcrumb': 'NAAC Accreditation',
    }
    return render(request, 'naac/naac.html', context)


def iqac(request):
    members = IQACMember.objects.all()
    aqar_docs = NAACDocument.objects.filter(doc_type='aqar')
    context = {
        'members': members,
        'aqar_docs': aqar_docs,
        'page_title': 'IQAC',
        'breadcrumb': 'Internal Quality Assurance Cell (IQAC)',
    }
    return render(request, 'naac/iqac.html', context)


def iiqa(request):
    docs = NAACDocument.objects.filter(doc_type='iiqa')
    context = {
        'docs': docs,
        'page_title': 'IIQA',
        'breadcrumb': 'Institutional Information for Quality Assessment (IIQA)',
    }
    return render(request, 'naac/iiqa.html', context)


def ssr(request):
    docs = NAACDocument.objects.filter(doc_type='ssr')
    context = {
        'docs': docs,
        'page_title': 'SSR',
        'breadcrumb': 'Self Study Report (SSR)',
    }
    return render(request, 'naac/ssr.html', context)


def dvv(request):
    docs = NAACDocument.objects.filter(doc_type='dvv')
    context = {
        'docs': docs,
        'page_title': 'DVV',
        'breadcrumb': 'Data Validation and Verification (DVV)',
    }
    return render(request, 'naac/dvv.html', context)


def atr(request):
    docs = NAACDocument.objects.filter(doc_type='atr')
    context = {
        'docs': docs,
        'page_title': 'ATR',
        'breadcrumb': 'Action Taken Report (ATR)',
    }
    return render(request, 'naac/atr.html', context)
