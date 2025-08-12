from .models import ExamAssessment, SemesterChoices
from django.db.models import Avg

def calculate_yekun_illik(student, subject):
    results = {}

    for semester in [SemesterChoices.FIRST, SemesterChoices.SECOND]:
        ms_qiymetler = ExamAssessment.objects.filter(
            student=student,
            subject=subject,
            semester=semester,
            exam_type='MS'
        ).aggregate(avg_ms=Avg('score'))['avg_ms']

        bs_qiymet = ExamAssessment.objects.filter(
            student=student,
            subject=subject,
            semester=semester,
            exam_type='BS'
        ).first()

        if ms_qiymetler is not None and bs_qiymet:
            semester_total = round((ms_qiymetler * 0.4) + (bs_qiymet.score * 0.6), 2)
            results[semester] = semester_total

    if SemesterChoices.FIRST in results and SemesterChoices.SECOND in results:
        yekun_illik = round((results[SemesterChoices.FIRST] + results[SemesterChoices.SECOND]) / 2, 2)
        return yekun_illik

    return None
