# Award Approval & Notification Guide

## How Award Approval Works

### The Approve Awards Process

#### 1. **Access Approve Awards Page**
- Only **Program Managers** can access this page
- Go to: **✅ Approve Awards** from the dashboard
- Shows all pending awards that need approval

#### 2. **Award Information Shown**
For each award, you'll see:
- **Student Name** - Full name of the recipient
- **Student Score** - Automatic scoring based on qualifications
- **Program Level** - UG (Undergraduate) or MS (Master's)
- **Financial Need** - H (High), M (Medium), L (Low)
- **Suggested Scholarship** - Which scholarship they matched to
- **Suggested Amount** - Default award amount (editable)

#### 3. **Review & Adjust Amount**
- Dollar amounts are shown formatted: `$5,000.00`
- You can **edit the amount** before approval
- Valid formats accepted:
  - `$5000.00` (with $ and commas)
  - `5000.00` (plain number)
  - `5000` (integer)
- **Validation**: Amount must be greater than $0

#### 4. **Approve or Reject**
**✓ Approve Button**:
- Sets award status to "approved"
- Records approval timestamp
- Amount is locked in

**✗ Reject Button**:
- Requires confirmation before proceeding
- Sets award status to "rejected"
- Award won't be included in notifications

#### 5. **Real-Time Feedback**
When you click Approve or Reject:
- Page shows: "Processing..."
- Upon success: "✓ Approved! Reloading..." or "✗ Rejected! Reloading..."
- Page automatically refreshes after 1.5 seconds
- Approved awards remain in "Approved" section
- Rejected awards are removed from this view

---

## Send Award Notifications

### What Are Award Notifications?
Award notification emails are sent to students to inform them:
- They have been selected for a scholarship
- The scholarship name and amount
- Instructions on next steps (varies by configuration)

### When to Send Notifications

**Best Practice**:
1. Review all pending awards first
2. Approve the awards you want to send notifications for
3. Reject any awards you don't want to proceed with
4. Once all decisions are made, scroll to bottom
5. Click **📧 Send Award Notification Emails**

### The Send Notifications Section

Located at the bottom of the Approve Awards page:

```
📧 Send Award Notifications
Once you've approved all awards above, click the button to 
send notification emails to students.

[📧 Send Award Notification Emails]
```

### How It Works

When you click the send button:

1. **System Checks**:
   - Finds all awards with status = "approved"
   - Verifies each award has a valid student email
   - Checks email configuration

2. **Sends Emails**:
   - Sends to each approved award recipient
   - Records email sent timestamp
   - Logs any failures

3. **Shows Results**:
   - **"Results: X sent, Y failed"**
   - Lists each student with status:
     - ✓ = Email sent successfully
     - ✗ = Email failed to send
   - Shows any error messages

### Example Results Output

```
Results: 15 sent, 1 failed

✓ John Smith: Sent
✓ Sarah Johnson: Sent
✓ Michael Chen: Sent
✗ Emily Rodriguez: Error - Invalid email address
✓ David Patel: Sent
```

---

## Email Configuration

### Current Mode: Mock (Testing)
The system is currently set to **Mock mode** - emails are logged but NOT actually sent.

### To Enable Real Emails

1. **Update Configuration**:
   - Edit `config.py`
   - Change: `MAIL_MODE = 'mock'` to `MAIL_MODE = 'smtp'`

2. **Configure SMTP Settings**:
   ```python
   MAIL_SERVER = 'your_smtp_server'
   MAIL_PORT = 587
   MAIL_USERNAME = 'your_email@example.com'
   MAIL_PASSWORD = 'your_password'
   MAIL_FROM = 'noreply@example.com'
   ```

3. **Test Email Sending**:
   - Upload a test student
   - Create an award
   - Approve it
   - Send notification
   - Verify recipient receives it

---

## Troubleshooting Award Approval

### Problem: Approve Button Doesn't Work

**Symptom**: Clicking "✓ Approve" does nothing

**Solutions**:
1. ✅ **Check Amount Field**:
   - Ensure an amount is entered
   - Amount must be greater than $0
   - Clear any invalid characters

2. ✅ **Check Browser Console**:
   - Press `F12` to open developer tools
   - Click **Console** tab
   - Look for error messages
   - Common errors:
     - "CSRF token missing" - Session may have expired
     - "Award not found" - Try refreshing page

3. ✅ **Try Again**:
   - Refresh the page (F5)
   - Log out and log back in
   - Clear browser cache

### Problem: Amount Shows as $0.00 But Won't Approve

**Solution**: Even if formatted as $0.00, validation requires > $0
- Change to: `$1.00` or higher
- This is intentional - prevents accidental $0 awards

### Problem: Send Awards Button Doesn't Work

**Symptom**: Clicking send button results in errors

**Solutions**:
1. ✅ **Verify Awards Approved**:
   - Go back to top of page
   - Confirm you have awarded any awards with "Approved" status
   - At least one award must be approved to send

2. ✅ **Check Email Configuration**:
   - In mock mode: emails still "send" (just logged)
   - Check application logs for output
   - Look for: "Award notification for [student] - mock mode"

3. ✅ **Browser/Network Issues**:
   - Wait a few seconds after clicking
   - Don't click multiple times
   - Check internet connection

### Problem: "No Pending Awards" Message

**What This Means**:
- All awards have either been approved or rejected
- No pending awards waiting for action

**What To Do**:
1. Go to **Review Matches** page
2. Check if there are students who need to be awarded
3. Click the "Suggest Award" or create new awards
4. Return to Approve Awards

---

## Award Status Lifecycle

```
PENDING (awaiting approval)
   ↓
   ├─→ APPROVED (ready to send notification) ✅
   │        ↓
   │   NOTIFIED (email sent to student)
   │
   └─→ REJECTED (not proceeding) ❌
```

### Status Definitions

| Status | Meaning | Shown On Approve Page? |
|--------|---------|----------------------|
| **pending** | Awaiting manager review | ✅ Yes |
| **approved** | Confirmed, ready to notify | ❌ No |
| **rejected** | Manager rejected | ❌ No |
| **notified** | Email sent to student | ❌ No |

---

## Awards & Financial Records

### Award Information Captured

When an award is approved, the system records:
- **Student ID & Name**
- **Scholarship Name & ID**
- **Award Amount** (as approved)
- **Approval Status** (approved/rejected)
- **Approved By** (username)
- **Approved At** (timestamp)
- **Email Sent At** (timestamp, if notified)
- **Email Sent To** (student email address)

### Exporting Award Data

1. Go to **Reports** page
2. Click **⬇️ Export to Excel**
3. Opens Excel file with full allocation report
4. Includes:
   - All approved awards
   - Student details
   - Award amounts
   - Approval dates
   - Summary statistics

---

## Best Practices

✅ **DO**:
- Review each award carefully before approving
- Verify student information is correct
- Ensure award amounts are appropriate
- Send notifications once all approvals are finalized
- Export and backup award data regularly

❌ **DON'T**:
- Approve awards with $0 amounts
- Approve awards for wrong students without rejecting first
- Click buttons multiple times too quickly
- Change amounts after approving (reject and re-approve instead)

---

## Questions?

If something doesn't work:
1. Refresh the page
2. Check browser developer console (F12)
3. Log out and back in
4. Contact system administrator

**Note**: The system is designed to prevent data loss - all actions are recorded and can be reviewed in the reports section.
