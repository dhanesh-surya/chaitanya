from django.core.management.base import BaseCommand
from courses.models import ProgramCourse

NEP_COURSES = [
    # B.A. (CCBA01)
    {"dept": "Hindi", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "HNSC-01", "name": "Hindi Sahitya Ka Itihas (Aadikaal se Ritikaal )", "paper": "I", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Sociology", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "SOSC-01", "name": "Introduction to Sociology", "paper": "II", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Political Science", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "PSSC-01", "name": "Introduction to Political Theory", "paper": "III", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Economics", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "ECSC-01", "name": "Basics of Economics", "paper": "IV", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "History", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "HISC-01", "name": "Ancient Indian History (From the Beginning to Satvahan dynasty)", "paper": "V", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Geography", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "GOSC- 01T", "name": "Fundamental of Physical Geography", "paper": "VI", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Music", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "MUSC- 01T", "name": "Introduction to Indian Music", "paper": "VII", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Hindi", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "AEC-03", "name": "Hindi Language", "paper": "", "type_1": "Theory", "type_2": "AEC"},
    {"dept": "Forestry  And Wild Life", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "FOGE-01T", "name": "Introduction to Forests & Forestry", "paper": "", "type_1": "Theory", "type_2": "GE"},
    {"dept": "Political Science", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "PSVAC- 01", "name": "Constitutional Values", "paper": "", "type_1": "Theory", "type_2": "VAC"},
    {"dept": "Forestry", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "FOGE- 01P", "name": "Lab Course: Forests & Forestry", "paper": "", "type_1": "Practical", "type_2": "GE"},
    {"dept": "Geography", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "GOSC- 01P", "name": "Geography Lab - Cartography- Tools and Techniques", "paper": "", "type_1": "Practical", "type_2": "DSC"},
    {"dept": "Music", "sem": "I", "program": "B.A. First Semester", "prog_code": "CCBA01", "code": "MUSC- 01P", "name": "Practical Music", "paper": "", "type_1": "Practical", "type_2": "DSC"},

    # B.Sc. Bio (CCBS01)
    {"dept": "Chemistry", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "CHSC- 01T", "name": "Fundamental Chemistry-I", "paper": "I", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Botany", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "BOSC- 01T", "name": "Elementary Botany", "paper": "II", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Zoology", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "ZOSC- 01T", "name": "Life on Earth and Unique Attributes of Animal Kingdom", "paper": "III", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Forestry", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "FOSC- 01T", "name": "Introduction to Forests & Forestry", "paper": "IV", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Computer Science", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "CAGE- 01T", "name": "Computer Fundamental and MS Office", "paper": "", "type_1": "Theory", "type_2": "GE"},
    {"dept": "English", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS02", "code": "AEC-02", "name": "English Language", "paper": "", "type_1": "Theory", "type_2": "AEC"},
    {"dept": "Chemistry", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "CHVAC- 01", "name": "Chemistry in Daily Life", "paper": "", "type_1": "Theory", "type_2": "VAC"},
    {"dept": "Botany", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "BOSC- 01P", "name": "Botany Lab-I (Elementary Botany)", "paper": "", "type_1": "Practical", "type_2": "DSC"},
    {"dept": "Zoology", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "ZOSC- 01P", "name": "Zoology Lab-I (Life on Earth)", "paper": "", "type_1": "Practical", "type_2": "DSC"},
    {"dept": "Forestry", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS02", "code": "FOSC- 01P", "name": "Lab Course: Forests & Forestry", "paper": "", "type_1": "Practical", "type_2": "DSC"},
    {"dept": "Computer Science", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "CAGE- 01P", "name": "Lab 1: MS Office", "paper": "", "type_1": "Practical", "type_2": "GE"},
    {"dept": "Chemistry", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS01", "code": "CHSC- 01P", "name": "Chemistry Lab Course-I", "paper": "", "type_1": "Practical", "type_2": "DSC"},

    # B.Sc. Math Group (CCBS03 / CCBS04)
    {"dept": "Computer Science", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS03", "code": "CSSC- 01T", "name": "Computer Fundamental and Operating System", "paper": "IV", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Physics", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS03", "code": "PHSC- 01T", "name": "Mechanics", "paper": "II", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Mathematics", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS03", "code": "MASC-01", "name": "Elementary Calculus", "paper": "I", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Mathematics", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS03", "code": "MAVAC- 01", "name": "Basic Mathematics and logic", "paper": "", "type_1": "Theory", "type_2": "VAC"},
    {"dept": "Computer Science", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS03", "code": "CSSC-01P", "name": "Lab 1: Operating System (DOS, Windows, Linux)", "paper": "", "type_1": "Practical", "type_2": "DSC"},
    {"dept": "Physics", "sem": "I", "program": "B.Sc. First Semester", "prog_code": "CCBS03", "code": "PHSC- 01P", "name": "Physics Lab", "paper": "", "type_1": "Practical", "type_2": "DSC"},

    # BCA (CCBC01)
    {"dept": "Computer Science", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "CASC-01", "name": "Discrete Mathematics", "paper": "I", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Computer Science", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "CASC- 02T", "name": "Computer Fundamental and MS-Office", "paper": "II", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Computer Science", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "CASC- 03T", "name": "Operating System", "paper": "II", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Geography", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "GOGE-01T", "name": "Fundamental of Physical Geography", "paper": "", "type_1": "Theory", "type_2": "GE"},
    {"dept": "Computer Science", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "AEC-02", "name": "English Language", "paper": "", "type_1": "Theory", "type_2": "AEC"},
    {"dept": "Computer Science", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "CAVAC- 01", "name": "Artificial Intelligence", "paper": "", "type_1": "Theory", "type_2": "VAC"},
    {"dept": "Computer Science", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "CASC- 02P", "name": "Lab 1: MS-Office", "paper": "", "type_1": "Practical", "type_2": "DSC"},
    {"dept": "Computer Science", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "CASC- 03P", "name": "Lab 2: Operating System", "paper": "", "type_1": "Practical", "type_2": "DSC"},
    {"dept": "Geography", "sem": "I", "program": "BCA First Semester", "prog_code": "CCBC01", "code": "GOSC- 01P", "name": "Geography Lab - Cartography- Tools and Techniques", "paper": "", "type_1": "Practical", "type_2": "GE"},

    # B.COM (CCBCOM)
    {"dept": "Commerce", "sem": "I", "program": "B.COM First Semester", "prog_code": "CCBCOM", "code": "COSC-01T", "name": "Fundamental of Accounting", "paper": "I", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Commerce", "sem": "I", "program": "B.COM First Semester", "prog_code": "CCBCOM", "code": "COSC-02T", "name": "Business Law", "paper": "II", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Commerce", "sem": "I", "program": "B.COM First Semester", "prog_code": "CCBCOM", "code": "COSC-03T", "name": "Business Economics", "paper": "III", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Computer Science", "sem": "I", "program": "B.COM First Semester", "prog_code": "CCBCOM", "code": "CAGE- 01T", "name": "Computer Fundamental and MS Office", "paper": "", "type_1": "Theory", "type_2": "GE"},
    {"dept": "Commerce", "sem": "I", "program": "B.COM First Semester", "prog_code": "CCBCOM", "code": "AEC-01", "name": "Environmental Studies", "paper": "", "type_1": "Theory", "type_2": "AEC"},
    {"dept": "Commerce", "sem": "I", "program": "B.COM First Semester", "prog_code": "CCBCOM", "code": "COVAC- 01", "name": "Concept of Business", "paper": "", "type_1": "Theory", "type_2": "VAC"},
    {"dept": "Computer Science", "sem": "I", "program": "B.COM First Semester", "prog_code": "CCBCOM", "code": "CAGE- 01P", "name": "Lab 1: MS Office", "paper": "", "type_1": "Practical", "type_2": "GE"},

    # BBA (CCBB01)
    {"dept": "Management", "sem": "I", "program": "BBA First Semester", "prog_code": "CCBB01", "code": "BBSC-01T", "name": "Principles of Management", "paper": "I", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Management", "sem": "I", "program": "BBA First Semester", "prog_code": "CCBB01", "code": "BBSC-02T", "name": "Business Mathematics", "paper": "II", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Management", "sem": "I", "program": "BBA First Semester", "prog_code": "CCBB01", "code": "BBSC-03T", "name": "Financial Accounting", "paper": "III", "type_1": "Theory", "type_2": "DSC"},
    {"dept": "Computer Science", "sem": "I", "program": "BBA First Semester", "prog_code": "CCBB01", "code": "CAGE-01T", "name": "Computer Application", "paper": "", "type_1": "Theory", "type_2": "GE"},
    {"dept": "Management", "sem": "I", "program": "BBA First Semester", "prog_code": "CCBB01", "code": "AEC-01", "name": "Environmental Studies", "paper": "", "type_1": "Theory", "type_2": "AEC"},
    {"dept": "Management", "sem": "I", "program": "BBA First Semester", "prog_code": "CCBB01", "code": "BBVAC- 01", "name": "Social Media Marketing", "paper": "", "type_1": "Theory", "type_2": "VAC"},
    {"dept": "Computer Science", "sem": "I", "program": "BBA First Semester", "prog_code": "CCBB01", "code": "CAGE- 01P", "name": "Lab: Computer Application (MS Office)", "paper": "", "type_1": "Practical", "type_2": "GE"},
]

THEORY_PRACTICAL_PAIRS = [
    ("B.A. First Semester", "GOSC- 01T", "GOSC- 01P"),
    ("B.A. First Semester", "MUSC- 01T", "MUSC- 01P"),
    ("B.A. First Semester", "FOGE-01T", "FOGE- 01P"),
    ("B.Sc. First Semester", "CHSC- 01T", "CHSC- 01P"),
    ("B.Sc. First Semester", "BOSC- 01T", "BOSC- 01P"),
    ("B.Sc. First Semester", "ZOSC- 01T", "ZOSC- 01P"),
    ("B.Sc. First Semester", "FOSC- 01T", "FOSC- 01P"),
    ("B.Sc. First Semester", "CAGE- 01T", "CAGE- 01P"),
    ("B.Sc. First Semester", "CSSC- 01T", "CSSC-01P"),
    ("B.Sc. First Semester", "PHSC- 01T", "PHSC- 01P"),
    ("BCA First Semester", "CASC- 02T", "CASC- 02P"),
    ("BCA First Semester", "CASC- 03T", "CASC- 03P"),
    ("BCA First Semester", "GOGE-01T", "GOSC- 01P"),
    ("B.COM First Semester", "CAGE- 01T", "CAGE- 01P"),
    ("BBA First Semester", "CAGE-01T", "CAGE- 01P"),
]

class Command(BaseCommand):
    help = 'Seed or update curriculum courses with official NEP course codes and paper numbers.'

    def handle(self, *args, **options):
        all_entries = list(NEP_COURSES)
        for entry in NEP_COURSES:
            short_prog = entry['program'].replace(' First Semester', '').strip()
            if short_prog != entry['program']:
                alias_entry = dict(entry)
                alias_entry['program'] = short_prog
                all_entries.append(alias_entry)

        course_objects = {}
        created_count = 0
        updated_count = 0

        for data in all_entries:
            prog_type = data['program']
            code = data['code']
            name = data['name']
            dept = data['dept']
            paper = data['paper']
            t1 = data['type_1']
            t2 = data['type_2']

            course = ProgramCourse.objects.filter(program_type=prog_type, course_code=code).first()
            if not course:
                course = ProgramCourse.objects.filter(program_type=prog_type, department=dept, course_name=name).first()

            if course:
                course.course_code = code
                course.paper_no = paper
                course.course_type_1 = t1
                course.course_type_2 = t2
                course.semester = 'I'
                course.save()
                updated_count += 1
            else:
                course = ProgramCourse.objects.create(
                    program_type=prog_type,
                    department=dept,
                    course_name=name,
                    course_code=code,
                    paper_no=paper,
                    semester='I',
                    course_type_1=t1,
                    course_type_2=t2,
                )
                created_count += 1

            course_objects[(prog_type, code)] = course

        linked_count = 0
        for prog, theory_code, practical_code in THEORY_PRACTICAL_PAIRS:
            theory_course = course_objects.get((prog, theory_code)) or ProgramCourse.objects.filter(program_type=prog, course_code=theory_code).first()
            practical_course = course_objects.get((prog, practical_code)) or ProgramCourse.objects.filter(program_type=prog, course_code=practical_code).first()

            if theory_course and practical_course:
                theory_course.auto_select_course = practical_course
                theory_course.save(update_fields=['auto_select_course'])
                linked_count += 1

            short_prog = prog.replace(' First Semester', '').strip()
            t_short = course_objects.get((short_prog, theory_code)) or ProgramCourse.objects.filter(program_type=short_prog, course_code=theory_code).first()
            p_short = course_objects.get((short_prog, practical_code)) or ProgramCourse.objects.filter(program_type=short_prog, course_code=practical_code).first()
            if t_short and p_short:
                t_short.auto_select_course = p_short
                t_short.save(update_fields=['auto_select_course'])

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded NEP courses: {created_count} created, {updated_count} updated, {linked_count} auto-select lab linkages established.'))
