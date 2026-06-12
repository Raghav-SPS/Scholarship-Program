# MSA Scholarship Matching System - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies (3 min)
```bash
pip install -r requirements.txt
```

### 2. Run the Application (2 min)
```bash
python app.py
```

**Output should show:**
```
Creating database...
Loading scholarships...
Running on http://0.0.0.0:5000
```

## Testing the System

### 1. Open Application
- Go to: http://localhost:5000

### 2. Login
- Password: `admin` (or set via `ADMIN_PASSWORD` environment variable)

### 3. Upload Sample Data
1. Click "Upload Applications"
2. Select `sample_applications.csv`
3. Click "Upload & Process"
4. You should see: "Successfully uploaded and processed 5 applications"

### 4. Review Matches
1. Click "Review Matches"
2. You'll see all 5 students with:
   - Automatically calculated scores
   - List of eligible scholarships
   - Match rankings

### 5. Approve Awards
1. Click "Approve Awards"
2. For each student, you can:
   - View suggested scholarship
   - Modify award amount
   - Click "Approve" or "Reject"
3. Once approved, click "Send Award Notifications"
4. Check `email_log.txt` to see logged emails

### 6. View Reports
1. Click "Reports"
2. See fund distribution and scholarship utilization

## Workflow Example

```
Upload CSV
    ↓
System Scores Students (automatically)
    ↓
System Matches to Scholarships (automatically)
    ↓
Admin Reviews Scores & Matches
    ↓
Admin Approves Awards (with adjustments if needed)
    ↓
System Sends Notifications (logged to email_log.txt)
    ↓
Done! Students receive awards
```

## Sample Data

`sample_applications.csv` includes 5 students with:
- Various program levels (UG/MS)
- Different financial needs (H/M/L)
- Different work experiences (accounting firms, internships)
- Leadership activities

This lets you test the full scoring and matching process.

## Key Features Demonstrated

✅ **Scoring**: Students automatically scored on experience and activities  
✅ **Matching**: Matched to appropriate scholarships based on eligibility  
✅ **Allocation**: Awards assigned from available scholarship funds  
✅ **Approval Workflow**: Admin reviews and approves before notification  
✅ **Email Logging**: Award notifications logged (not actually sent in test mode)  

## Troubleshooting

### Port 5000 already in use?
```bash
export FLASK_PORT=5001
python app.py
```

### Need to reset data?
```bash
# Delete database
rm scholarship.db

# Reinitialize
python app.py
```

### Want to use different password?
```bash
export ADMIN_PASSWORD="your-password"
python app.py
```

## What Happens Behind the Scenes

1. **Scoring Engine** (`scoring.py`):
   - Reads work experience and activities
   - Scores accounting-related experience
   - Scores leadership and involvement
   - Produces total score

2. **Matching Engine** (`matcher.py`):
   - Checks student eligibility for each scholarship
   - Filters by program level, GPA, financial need
   - Matches to employer-specific scholarships if applicable
   - Ranks scholarships by fit

3. **Fund Allocation**:
   - Ensures available funds exist
   - Assigns awards sorted by student score
   - Handles multi-scholarship allocation when needed

4. **Notifications** (`notifications.py`):
   - Creates professional award emails
   - In mock mode: logs to `email_log.txt`
   - Can be enabled for real SMTP sending

## Next Steps

- [ ] Test with your own student data
- [ ] Upload full applicant pool
- [ ] Adjust default award amounts (currently $5,000)
- [ ] Configure real email (SMTP) for production
- [ ] Fine-tune scoring weights if needed
- [ ] Export reports for committee review

## Support

For detailed documentation, see `README.md`

---
**Ready to go!** Your application should now be running on http://localhost:5000
