"""
Scholarship matching engine.
Matches students to scholarships based on eligibility criteria and preferences.
"""

import re
from decimal import Decimal
from models import Scholarship


def get_eligible_scholarships(student, exclude_zero_balance=True):
    """
    Return list of eligible scholarships for a student.

    Args:
        student: Student model instance
        exclude_zero_balance: If True, exclude scholarships with $0 available

    Returns:
        list of (Scholarship, match_score) tuples, sorted by match score descending
    """

    eligible = []

    for scholarship in Scholarship.query.all():
        # Check if scholarship has funds
        if exclude_zero_balance and scholarship.available_amount <= 0:
            continue

        # Check program level eligibility
        if student.program_level == 'UG' and not scholarship.ug_eligible:
            continue
        if student.program_level == 'MS' and not scholarship.ms_eligible:
            continue

        # Check restrictions (if any)
        if not _check_restrictions(student, scholarship):
            continue

        # Calculate match score
        match_score = _calculate_match_score(student, scholarship)

        eligible.append((scholarship, match_score))

    # Sort by match score descending (higher is better)
    eligible.sort(key=lambda x: x[1], reverse=True)

    return eligible


def _check_restrictions(student, scholarship):
    """
    Check if student meets scholarship restrictions.

    Returns:
        True if student is eligible, False otherwise
    """

    if not scholarship.restrictions:
        return True

    restrictions = scholarship.restrictions.lower()

    # Check GPA requirement if specified
    if 'gpa' in restrictions and student.gpa:
        # Parse GPA requirement (e.g., "3.0" or "minimum 3.0")
        gpa_match = re.search(r'(\d+\.\d+)', restrictions)
        if gpa_match:
            required_gpa = float(gpa_match.group(1))
            if float(student.gpa) < required_gpa:
                return False

    # Check financial need requirement
    if 'financial need' in restrictions and 'high' in restrictions.lower():
        if student.financial_need != 'H':
            return False
    elif 'financial need' in restrictions and 'medium' in restrictions.lower():
        if student.financial_need not in ('H', 'M'):
            return False

    # Check employer restrictions (e.g., "Deloitte only")
    employer_keywords = ['deloitte', 'pwc', 'ey', 'kpmg', 'bdo', 'grant thornton']
    for employer in employer_keywords:
        if employer in restrictions:
            # Student must have internship/position at this firm
            student_firms = (
                (student.permanent_position_at or '').lower() + ' ' +
                (student.internship_2025_at or '').lower() + ' ' +
                (student.internship_2026_at or '').lower()
            )
            if employer not in student_firms:
                return False

    return True


def _calculate_match_score(student, scholarship):
    """
    Calculate match score between student and scholarship.
    Higher score = better match.

    Returns:
        float score
    """

    score = 0.0

    # Base score for program level match
    if student.program_level == 'UG' and scholarship.ug_eligible:
        score += 10
    if student.program_level == 'MS' and scholarship.ms_eligible:
        score += 15  # Higher preference for MS scholarships to MS students

    # Check for employer preference match
    firms_in_restrictions = _extract_firms_from_restrictions(scholarship.restrictions)
    student_firms = _get_student_firms(student)

    for firm in firms_in_restrictions:
        if firm in student_firms:
            score += 20  # Employer match is highly valuable

    # Available funds score (prefer scholarships with more available funds)
    if scholarship.available_amount:
        score += min(float(scholarship.available_amount) / 1000, 20)

    # Financial need match (if scholarship mentions it)
    if scholarship.restrictions and 'financial need' in scholarship.restrictions.lower():
        if student.financial_need in ('H', 'M'):
            score += 5

    return score


def _extract_firms_from_restrictions(restrictions):
    """Extract firm names from restrictions text."""
    if not restrictions:
        return []

    firms = []
    firm_keywords = ['deloitte', 'pwc', 'ey', 'ernst & young', 'kpmg', 'bdo',
                     'grant thornton', 'crowe', 'plante moran', 'rehmann', 'rsm']

    restrictions_lower = restrictions.lower()
    for firm in firm_keywords:
        if firm in restrictions_lower:
            firms.append(firm)

    return firms


def _get_student_firms(student):
    """Get all firms associated with student."""
    firms = []
    if student.permanent_position_at:
        firms.append(student.permanent_position_at.lower())
    if student.internship_2025_at:
        firms.append(student.internship_2025_at.lower())
    if student.internship_2026_at:
        firms.append(student.internship_2026_at.lower())
    return firms


def suggest_awards(students_with_scores, available_scholarships_dict):
    """
    Suggest scholarship awards for students.

    Args:
        students_with_scores: list of (Student, Score) tuples
        available_scholarships_dict: dict of scholarship_id -> available_amount

    Returns:
        list of suggested awards: [(student_id, scholarship_id, amount), ...]
    """

    suggestions = []

    # Sort students by score (highest first)
    students_with_scores.sort(key=lambda x: x[1].total_score, reverse=True)

    # Track remaining balances
    remaining = available_scholarships_dict.copy()

    for student, score in students_with_scores:
        eligible_scholarships = get_eligible_scholarships(student)

        # Try to find a single scholarship with sufficient funds
        assigned = False

        for scholarship, match_score in eligible_scholarships:
            if remaining.get(scholarship.id, 0) > 0:
                # Suggest this award
                suggestions.append({
                    'student_id': student.id,
                    'scholarships': [
                        {
                            'scholarship_id': scholarship.id,
                            'scholarship_name': scholarship.sort_name,
                            'amount': remaining[scholarship.id]  # Full remaining amount
                        }
                    ],
                    'status': 'pending',
                    'admin_action_required': False
                })
                remaining[scholarship.id] = 0
                assigned = True
                break

        # If no single scholarship had funds, suggest multi-scholarship option
        if not assigned and eligible_scholarships:
            multi_scholarships = []
            remaining_award_amount = Decimal('5000')  # Default award amount

            for scholarship, match_score in eligible_scholarships:
                if remaining.get(scholarship.id, 0) > 0 and remaining_award_amount > 0:
                    allocation = min(
                        remaining[scholarship.id],
                        remaining_award_amount
                    )
                    multi_scholarships.append({
                        'scholarship_id': scholarship.id,
                        'scholarship_name': scholarship.sort_name,
                        'amount': allocation
                    })
                    remaining[scholarship.id] -= allocation
                    remaining_award_amount -= allocation

            if multi_scholarships:
                suggestions.append({
                    'student_id': student.id,
                    'scholarships': multi_scholarships,
                    'status': 'pending',
                    'admin_action_required': True  # Admin needs to approve multi-source
                })

    return suggestions
