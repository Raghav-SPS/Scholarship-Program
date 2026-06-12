# MSA Scholarship Matching System

## Overview

Automated scholarship matching and award allocation system for the Michigan State University Master of Science in Accounting program. The system automatically scores student applications based on defined rubrics, matches eligible students to scholarships based on criteria, and allows administrators to review and approve awards.

## Features

- **Automatic Scoring**: Scores applications based on accounting experience, work history, and leadership
- **Smart Matching**: Matches students to scholarships based on eligibility criteria and preferences
- **Fund Allocation**: Intelligently allocates funds considering GPA, financial need, and scholarship restrictions
- **Admin Dashboard**: Web-based interface for uploading, reviewing, and approving awards
- **Email Notifications**: Sends award notifications to approved students (currently in mock/test mode)
- **Reporting**: Generates reports on scholarship distribution and fund utilization

## Project Structure

```
Scholarship Program/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── models.py                       # SQLAlchemy database models
├── scoring.py                      # Scoring engine
├── matcher.py                      # Scholarship matching logic
├── notifications.py                # Email notification system
├── requirements.txt                # Python dependencies
├── MASTER Scholarship Spreadsheet 2025-2026.xlsx  # Scholarship data
├── FY26 Available Funds for Committee.xlsx        # Available funding
├── ms rubric.docx                  # Master's scoring rubric
├── undergrad rubric.docx           # Undergraduate scoring rubric
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── login.html                  # Login page
│   ├── dashboard.html              # Admin dashboard
│   ├── upload.html                 # Application upload
│   ├── review.html                 # Match review
│   ├── approve.html                # Award approval
│   └── reports.html                # Reports page
└── static/                         # Static files (CSS, JS)
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export FLASK_ENV=development
export ADMIN_PASSWORD=your-secure-password
```

On Windows (Command Prompt):
```cmd
set FLASK_ENV=development
set ADMIN_PASSWORD=your-secure-password
```

### 3. Initialize Database

```bash
python app.py
```

This will:
- Create the SQLite database
- Create all tables
- Load scholarships from Excel files

### 4. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## Usage Workflow

### Step 1: Login
- Navigate to `http://localhost:5000`
- Enter the admin password

### Step 2: Upload Applications
1. Go to "Upload Applications"
2. Prepare a CSV file with student data (see CSV Format below)
3. Upload the CSV
4. System will automatically:
   - Create student records
   - Score applications
   - Match to scholarships

### Step 3: Review Matches
1. Go to "Review Matches"
2. View system-generated scores and scholarship matches
3. Verify the matching logic worked correctly

### Step 4: Approve Awards
1. Go to "Approve Awards"
2. Review each suggested award
3. Modify award amounts if needed
4. Approve or reject individual awards
5. Click "Send Award Notifications" to send emails

### Step 5: View Reports
- Go to "Reports" to see:
  - Fund utilization
  - Award status
  - Scholarship breakdown

## CSV Format

The uploaded CSV must contain these columns:

| Column | Format | Example |
|--------|--------|---------|
| Student First Name | String | John |
| Student Middle Name | String | Michael |
| Student Last Name | String | Doe |
| Student ID | String | 12345678 |
| Email | String | john@msu.edu |
| GPA | Decimal | 3.8 |
| Program Level | 'UG' or 'MS' | MS |
| Financial Need | 'H', 'M', or 'L' | H |
| Permanent Position At | Firm name | Deloitte |
| Internship 2025 At | Firm name | PwC |
| Internship 2026 At | Firm name | KPMG |
| Extracurricular Activities | Multi-line text | VITA member\nCase competition |
| College Activities | Multi-line with dates | Accounting Student Assoc - Aug 2022 - Present |
| Work Experience | Multi-line with details | Deloitte Intern - Jun 2024 - Aug 2024 |

## Scoring Rubric

### Work Experience Scoring
- Accounting firm position/internship: +25 points
- Accounting-related job titles: +5 points each (max 15)
- 2+ internships: +5 points
- 3+ work experiences: +5 points
- **Maximum: 50 points**

### Activities & Leadership Scoring
- Leadership position: +5 points each (max 20)
- Accounting student org involvement: +5 points each (max 20)
- Multiple involvement activities: +10 points
- **Maximum: 40 points**

### Total Possible Score: 90 points

## Scholarship Matching Algorithm

The system matches students using these criteria (in order):

1. **Program Level Eligibility** - Match UG/MS requirements
2. **GPA Requirements** - Check if student meets minimum GPA
3. **Financial Need** - Match if scholarship requires specific need level
4. **Employer Restrictions** - Match to relevant firm scholarships
5. **Available Funds** - Ensure scholarship has remaining balance

For students needing multiple scholarships, the admin can combine multiple sources on the Approve Awards page.

## Email Notifications

Currently in **mock mode** for testing:
- Emails are logged to `email_log.txt` instead of being sent
- Can be updated to use real SMTP in production

To configure real SMTP:
1. Update `notifications.py` with your SMTP server details
2. Change `MAIL_MODE` in `config.py` from 'mock' to 'smtp'

## Data Files

### Loading Data
- Scholarships are automatically loaded from `MASTER Scholarship Spreadsheet 2025-2026.xlsx`
- Available funds are loaded from `FY26 Available Funds for Committee.xlsx`
- Rubric documents (`ms rubric.docx`, `undergrad rubric.docx`) provide scoring guidelines

### Database
- SQLite database is created as `scholarship.db`
- Uploaded files are stored in `uploads/` directory

## Troubleshooting

### Database Issues
```bash
# Reset database (delete existing data)
rm scholarship.db
python app.py
```

### Excel File Not Found
- Ensure Excel files are in the same directory as `app.py`
- Check file names match exactly (case-sensitive on Linux)

### Port Already in Use
```bash
# Use different port
export FLASK_PORT=5001
python app.py
```

## Development Notes

- **Testing Mode**: System is in mock email mode. Emails are logged to `email_log.txt`
- **Database**: SQLite is fine for development; upgrade to PostgreSQL for production
- **Security**: Change default admin password and use environment variables
- **Scaling**: Current design supports hundreds of students; optimize queries for thousands+

## Future Enhancements

- [ ] Multi-scholarship allocation with admin UI picker
- [ ] Manual scoring override capability
- [ ] Historical data and year-over-year comparisons
- [ ] Real SMTP email integration
- [ ] PDF award letters generation
- [ ] REST API for integration with MSU systems
- [ ] Audit logging for all administrative actions
- [ ] Multi-factor authentication for admin access
- [ ] Role-based access control

## Support

For issues or questions, please contact the MSA Program office.

---

**System Version**: 1.0  
**Last Updated**: 2026-04-14  
**Created for**: Michigan State University MSA Program
