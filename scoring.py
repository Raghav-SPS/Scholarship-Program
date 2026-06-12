"""
Scoring engine for scholarship applications.
Scores based on:
- Accounting-related work experience
- Leadership and extracurricular activities
- Financial need and GPA
"""

import re
from decimal import Decimal

# Keywords for identifying accounting-related work/internships
ACCOUNTING_FIRMS = {
    'deloitte', 'pwc', 'ernst & young', 'ey', 'kpmg', 'bdo', 'grant thornton',
    'crowe', 'baker tilly', 'moss adams', 'plante moran', 'rehmann', 'rsm',
    'weiser', 'foley', 'moss', 'ernst', 'young', 'accounting', 'audit', 'tax'
}

ACCOUNTING_JOB_TITLES = {
    'accounting', 'auditor', 'tax', 'audit intern', 'tax intern', 'business analyst',
    'financial analyst', 'controller', 'accountant', 'accounts payable', 'accounts receivable'
}

LEADERSHIP_KEYWORDS = {
    'president', 'vice president', 'treasurer', 'secretary', 'chair', 'chairman',
    'board', 'officer', 'director', 'leader', 'founder', 'lead'
}


def score_student(student, application):
    """
    Calculate score for a student based on their application.

    Args:
        student: Student model instance
        application: Application model instance

    Returns:
        dict with component scores and total score
    """

    scores_dict = {
        'accounting_experience_score': Decimal('0'),
        'work_experience_score': Decimal('0'),
        'leadership_score': Decimal('0'),
        'total_score': Decimal('0'),
        'notes': []
    }

    # Score work experience
    if application.work_experience:
        scores_dict['work_experience_score'] = _score_work_experience(
            application.work_experience,
            student
        )
        scores_dict['notes'].append(f"Work experience: {scores_dict['work_experience_score']} pts")

    # Score activities
    if application.college_activities:
        scores_dict['leadership_score'] = _score_activities(
            application.college_activities,
            application.extracurricular_activities
        )
        scores_dict['notes'].append(f"Activities/Leadership: {scores_dict['leadership_score']} pts")

    # Calculate total (you can adjust weights as needed)
    scores_dict['total_score'] = (
        scores_dict['accounting_experience_score'] +
        scores_dict['work_experience_score'] +
        scores_dict['leadership_score']
    )

    return scores_dict


def _score_work_experience(work_text, student):
    """Score based on work experience quality and accounting relevance."""
    score = Decimal('0')
    text_lower = work_text.lower()

    # Check for internship/permanent position with accounting firms
    has_accounting_firm = False
    has_accounting_title = False

    if student.permanent_position_at:
        if _is_accounting_firm(student.permanent_position_at):
            score += Decimal('25')
            has_accounting_firm = True

    if student.internship_2025_at:
        if _is_accounting_firm(student.internship_2025_at):
            score += Decimal('20')
            has_accounting_firm = True

    if student.internship_2026_at:
        if _is_accounting_firm(student.internship_2026_at):
            score += Decimal('20')
            has_accounting_firm = True

    # Scan work experience text for accounting keywords
    accounting_keyword_count = sum(1 for keyword in ACCOUNTING_JOB_TITLES if keyword in text_lower)

    if accounting_keyword_count > 0:
        score += Decimal(min(accounting_keyword_count * 5, 15))
        has_accounting_title = True

    # Points for work experience duration and variety
    internship_count = text_lower.count('intern')
    work_experience_count = len(re.findall(r'\d+\s*(year|month)', text_lower, re.IGNORECASE))

    if internship_count >= 2:
        score += Decimal('5')
    if work_experience_count >= 3:
        score += Decimal('5')

    # Cap the score
    score = min(score, Decimal('50'))

    return score


def _score_activities(activities_text, extracurricular_text=''):
    """Score based on leadership activities and involvement."""
    score = Decimal('0')
    all_text = (activities_text + ' ' + (extracurricular_text or '')).lower()

    # Leadership positions
    leadership_count = sum(1 for keyword in LEADERSHIP_KEYWORDS if keyword in all_text)
    if leadership_count > 0:
        score += Decimal(min(leadership_count * 5, 20))

    # Accounting student orgs
    accounting_org_keywords = {'accounting student', 'asa', 'delta sigma pi', 'vita', 'business'}
    org_count = sum(1 for keyword in accounting_org_keywords if keyword in all_text)
    if org_count > 0:
        score += Decimal(min(org_count * 5, 20))

    # Duration and involvement (estimate from text length and frequency)
    if len(activities_text) > 200:
        score += Decimal('5')
    if all_text.count('-') >= 3:  # Multiple entries with date ranges
        score += Decimal('5')

    # Cap the score
    score = min(score, Decimal('40'))

    return score


def _is_accounting_firm(firm_name):
    """Check if firm is accounting-related."""
    if not firm_name:
        return False
    firm_lower = firm_name.lower()
    return any(keyword in firm_lower for keyword in ACCOUNTING_FIRMS)


def parse_activities_text(text):
    """
    Parse activities text to extract structured data.

    Returns:
        list of dicts with activity info
    """
    if not text:
        return []

    activities = []
    # Split by line breaks and bullets
    entries = re.split(r'\n|•|-', text)

    for entry in entries:
        if entry.strip():
            activity = {
                'text': entry.strip(),
                'dates': _extract_dates(entry)
            }
            activities.append(activity)

    return activities


def _extract_dates(text):
    """Extract date ranges from text."""
    # Look for patterns like "Aug 2022 - Dec 2023" or "2022-2024"
    date_pattern = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{4}|^\d{4})\s*(?:to|-)\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{4}|^\d{4})?'
    matches = re.findall(date_pattern, text, re.IGNORECASE)
    return matches if matches else []
