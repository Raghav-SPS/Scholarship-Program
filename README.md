# MSA Scholarship Matching System

Automated scholarship matching and award allocation system for the Michigan State University Master of Science in Accounting (MSA) program. The system scores student applications, matches eligible students to scholarships, and lets administrators review and approve awards through a web interface.

## Features

- **Automatic Scoring** — Scores applications based on accounting experience, work history, and leadership
- **Smart Matching** — Matches students to scholarships based on eligibility criteria
- **Fund Allocation** — Allocates funds considering GPA, financial need, and scholarship restrictions
- **Two-Role Access** — Separate Admin and Evaluator dashboards
- **Excel/CSV Upload** — Upload student applications in bulk
- **Export Reports** — Download allocation reports as formatted Excel files
- **Email Notifications** — Sends award notifications (mock mode by default)

## Quick Start

### 1. Clone the repo and install dependencies

```bash
git clone https://github.com/Raghav-SPS/Scholarship-Program.git
cd Scholarship-Program
pip install -r requirements.txt
```

### 2. Run the app

**Option A — Double-click** `start.bat` (Windows only, recommended)

**Option B — Terminal**
```bash
python app.py
```

The app will start at `http://localhost:5000`.

On first run, 6 sample scholarships are automatically loaded so the program works out of the box with no extra files needed.

## Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Evaluator | `evaluator@msu.edu` | `evaluator123` |
| Admin | `admin@msu.edu` | `admin123` |

**Evaluator** — uploads applications, reviews matches, approves awards, sends notifications  
**Admin** — manages scholarships, views reports, exports data

To change credentials, set environment variables before running:
```bash
# Windows
set EVALUATOR_USERNAME=your@email.com
set EVALUATOR_PASSWORD=yourpassword
set ADMIN_USERNAME=admin@email.com
set ADMIN_PASSWORD=adminpassword
```

## Sharing the App (ngrok)

To share the app with people outside your network (e.g., for demos):

1. Sign up free at [ngrok.com](https://ngrok.com) and get your authtoken
2. Run once to authenticate:
   ```bash
   .\ngrok.exe authtoken YOUR_TOKEN
   ```
3. From then on, `start.bat` launches both Flask and ngrok together. Copy the `https://....ngrok-free.app` link from the ngrok window and share it — anyone can open it in their browser.

> Note: The ngrok link changes each time you restart it (free tier). Your laptop must stay on while others are using it.

## Usage Workflow

### Step 1 — Upload Applications (Evaluator)
1. Go to **Upload Applications**
2. Upload a CSV or Excel file with student data (download the sample format from the upload page)
3. The system automatically scores each student and suggests scholarship matches

### Step 2 — Review Matches (Evaluator)
1. Go to **Review Matches**
2. See system-generated scores and suggested scholarship pairings

### Step 3 — Approve Awards (Evaluator)
1. Go to **Approve Awards**
2. Set award amounts, approve or reject each suggestion
3. Manually assign scholarships to unmatched students if needed
4. Click **Send Award Notifications** to email students

### Step 4 — Reports (Admin or Evaluator)
- Go to **Reports** to view fund utilization and award breakdowns
- Export a formatted Excel report with full allocation details

## Application File Format

Upload a CSV or Excel file with these columns:

| Column | Format | Example |
|--------|--------|---------|
| Student ID | String | 20240001 |
| Student First Name | String | John |
| Student Middle Name | String | Michael |
| Student Last Name | String | Smith |
| Email | Email | john@msu.edu |
| GPA | Decimal | 3.85 |
| Program Level | `UG` or `MS` | MS |
| Financial Need | `H`, `M`, or `L` | H |
| Permanent Position At | Firm name | Deloitte |
| Internship 2025 At | Firm name | EY |
| Internship 2026 At | Firm name | KPMG |
| Extracurricular Activities | Text | Student Government, Accounting Club |
| College Activities | Text | Finance Committee Chair |
| Work Experience | Text | Auditor at Big 4 (2 years) |

Download a pre-formatted sample from the **Upload Applications** page.

## Scholarship Data

The system comes with 6 sample scholarships pre-loaded for demo purposes. To use real scholarship data, place your own Excel files in the project root:

- `MASTER Scholarship Spreadsheet 2025-2026.xlsx` — scholarship details
- `FY26 Available Funds for Committee.xlsx` — available fund amounts

If these files are present, they are loaded on startup and override the sample data.

> These files are excluded from the repository to protect sensitive information.

## Scoring Rubric

### Work Experience (max 50 pts)
- Accounting firm position or internship: +25 pts
- Accounting-related job titles: +5 pts each (max 15)
- 2+ internships: +5 pts
- 3+ work experiences: +5 pts

### Activities & Leadership (max 40 pts)
- Leadership position: +5 pts each (max 20)
- Accounting student org involvement: +5 pts each (max 20)
- Multiple activities: +10 pts

**Total possible: 90 points**

## Project Structure

```
Scholarship Program/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models.py               # Database models
├── scoring.py              # Scoring engine
├── matcher.py              # Scholarship matching logic
├── notifications.py        # Email notification system
├── requirements.txt        # Python dependencies
├── start.bat               # One-click launcher (Flask + ngrok)
├── sample_applications.csv # Sample upload file for testing
├── ngrok.exe               # ngrok tunnel binary (Windows)
└── templates/              # HTML templates
```

## Troubleshooting

**Excel files not found** — This is expected when running without real data files. The app auto-loads sample scholarships instead.

**Port already in use** — Another process is on port 5000. Stop it or restart your machine.

**ngrok authentication error** — Run `.\ngrok.exe authtoken YOUR_TOKEN` once (get token from ngrok.com dashboard).

**Reset the database** — Delete `scholarship.db` and restart `app.py`. Sample data will re-seed automatically.

---

**Created for:** Michigan State University MSA Program  
**Last Updated:** June 2026
