from .models import ExamAssessment

def calculate_yearly_grade(student, subject, classroom):
    ms_scores = ExamAssessment.objects.filter(student=student, subject=subject, classroom=classroom, type='MS').values_list('score', flat=True)
    bs_scores = ExamAssessment.objects.filter(student=student, subject=subject, classroom=classroom, type='BS').values_list('score', flat=True)

    if not ms_scores or not bs_scores:
        return None

    ms_avg = sum(ms_scores) / len(ms_scores)
    bs_avg = sum(bs_scores) / len(bs_scores)

    return round((ms_avg * 0.4 + bs_avg * 0.6), 2)
