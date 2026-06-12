"""
Email notification system for scholarship awards.
Currently mocked for testing - can be enhanced for real SMTP.
"""

import os
from datetime import datetime
from models import Award


def send_award_notification(award, environment='mock'):
    """
    Send award notification to student.

    Args:
        award: Award model instance
        environment: 'mock' or 'smtp'

    Returns:
        dict with status and result
    """

    if not award.student or not award.scholarship:
        return {'success': False, 'error': 'Award missing student or scholarship'}

    email_content = _generate_email_content(award)

    if environment == 'mock':
        return _send_mock_email(award, email_content)
    else:
        return _send_smtp_email(award, email_content)


def _generate_email_content(award):
    """Generate email content for award notification."""

    student = award.student
    scholarship = award.scholarship
    scholarships_list = _get_award_scholarships(award)

    subject = f"Congratulations! You've Received an MSA Scholarship Award"

    scholarship_details = _format_scholarships(scholarships_list)

    body = f"""Dear {student.full_name()},

Congratulations! You have been selected to receive a scholarship award from the Michigan State University Master of Science in Accounting program.

AWARD DETAILS:
==============
Total Award Amount: ${award.amount:,.2f}
Scholarship(s): {', '.join([s['name'] for s in scholarships_list])}

{scholarship_details}

Your award will help support your academic journey. Thank you for your dedication to excellence in accounting.

Please contact the MSA Program office if you have any questions.

Best regards,
MSA Program Scholarship Committee
Michigan State University
"""

    return {'subject': subject, 'body': body}


def _format_scholarships(scholarships_list):
    """Format scholarship details for email."""
    details = ""
    for scholarship in scholarships_list:
        details += f"• {scholarship['name']}: ${scholarship['amount']:,.2f}\n"
    return details


def _get_award_scholarships(award):
    """Get all scholarships for an award (in case of multi-source awards)."""
    # Awards table links to single scholarship, but we can track multi-source via notes
    return [{
        'name': award.scholarship.official_name,
        'amount': award.amount
    }]


def _send_mock_email(award, email_content):
    """Log email instead of sending (for testing)."""

    from config import Config
    log_file = Config.MAIL_LOG_FILE

    # Ensure uploads directory exists
    os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log_entry = f"""
{'='*80}
Email Log Entry - {timestamp}
{'='*80}
To: {award.student.email or 'NO_EMAIL_PROVIDED'}
Subject: {email_content['subject']}

Body:
{email_content['body']}

Award ID: {award.id}
Student: {award.student.full_name()}
Scholarship: {award.scholarship.sort_name}
Amount: ${award.amount}
{'='*80}
"""

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    return {
        'success': True,
        'message': f'Email logged to {log_file}',
        'email_sent_at': award.email_sent_at.isoformat()
    }


def _send_smtp_email(award, email_content):
    """Send real email via SMTP."""
    # TODO: Implement SMTP sending
    raise NotImplementedError('SMTP email sending not yet implemented')


def log_email(recipient, subject, body):
    """Utility to log any email."""

    from config import Config
    log_file = Config.MAIL_LOG_FILE

    os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"""
{'='*80}
Email - {timestamp}
To: {recipient}
Subject: {subject}

{body}
{'='*80}
"""

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)
