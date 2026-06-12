# Scholarship Allocation Program - Setup Guide

## Program Overview

The **Scholarship Allocation Program** is now a role-based system with two types of users:

### User Roles

#### 1. **Program Manager** 👤
- **Primary Role**: Execute the scholarship allocation workflow
- **Responsibilities**:
  - Upload student applications (CSV/Excel)
  - Review automatic scholarship matches
  - Approve/Reject awards with specific amounts
  - Send award notification emails
  - View allocation reports

- **Accessible Pages**:
  - Dashboard (Manager view)
  - Upload Applications
  - Review Matches
  - Approve Awards
  - Reports & Export

#### 2. **Administrator** ⚙️
- **Primary Role**: System management and configuration
- **Responsibilities**:
  - Add/Edit/Delete scholarships
  - Manage scholarship eligibility and availability
  - View system reports and allocations
  - Monitor overall fund utilization

- **Accessible Pages**:
  - Dashboard (Admin view)
  - Manage Scholarships
  - Reports & Export

---

## How to Access the Program

### Login Steps

1. **Open the application** - Go to the login page
2. **Select Your Role**:
   - Select **Manager** if you're processing applications and approving awards
   - Select **Admin** if you're managing scholarships and system configuration
3. **Enter Password** - Default: `admin`
4. **Click Login**

---

## Program Manager Workflow

### Step 1: Upload Applications
- Click **📤 Upload Applications** on the dashboard
- Download the sample format template (optional but recommended)
- Upload CSV or Excel file with student data
- System validates and processes all students

### Step 2: Review Matches
- Click **👁️ Review Matches**
- View suggested scholarship matches
- See automatic scoring and student information
- System ranks students by score

### Step 3: Approve Awards
- Click **✅ Approve Awards**
- Review each pending award
- **Adjust the award amount** if needed
- Click **✓ Approve** or **✗ Reject**
- Status updates immediately after each action

### Step 4: Send Notifications
- After approving awards, scroll to bottom
- Click **📧 Send Award Notification Emails**
- System sends emails to all award recipients
- View delivery status and any errors

### Step 5: Generate Reports
- Click **📊 Reports**
- View allocation summaries
- Click **⬇️ Export to Excel** to download data

---

## Administrator Workflow

### Manage Scholarships
1. Click **📋 Manage Scholarships** on the dashboard
2. View all scholarships with:
   - Available funds
   - Total allocated
   - Remaining balance
3. **Add New**: Click **➕ Add New Scholarship**
4. **Edit**: Click **✏️ Edit** on any scholarship
5. **Delete**: Click **🗑️ Delete** (only if no awards exist)

### View System Reports
1. Click **📊 Reports**
2. See fund utilization statistics
3. Export allocation data to Excel

---

## File Format Requirements

### Sample CSV/Excel Format

**Required Columns**:
- Student ID (unique identifier)
- Student First Name
- Student Middle Name (optional)
- Student Last Name (REQUIRED)
- Email
- GPA (numeric, 0.00 - 4.00)
- Program Level (UG or MS)
- Financial Need (H, M, or L)
- Permanent Position At (optional - employer)
- Internship 2025 At (optional - company name)
- Internship 2026 At (optional - company name)
- Extracurricular Activities (optional - comma-separated)
- College Activities (optional - comma-separated)
- Work Experience (optional - comma-separated)

### Example Row
```
20240001 | John | Michael | Smith | john.smith@msu.edu | 3.85 | MS | H | Deloitte | EY | KPMG | VITA, Accounting Club | Student Gov | Auditor (2 yrs)
```

---

## Troubleshooting

### Approve Button Not Working
✅ **Fixed**: Button now properly parses dollar amounts with commas
- Format supported: $5,000.00 or 5000.00
- Validation prevents zero amounts

### Send Notifications Not Working
✅ Make sure to:
1. First approve some awards (they must have status='approved')
2. Click the refresh button if needed
3. Check browser console (F12) for any errors

### Manager Can't See Scholarship Section
✅ This is correct! Only Admins can manage scholarships
- Managers can only view reports

### Admin Can't Upload Applications
✅ This is correct! Only Managers can upload
- Admins should have a manager account for processing

---

## Password Management

- **Default Password**: `admin`
- **To Change**: Set `ADMIN_PASSWORD` environment variable
- Example:
  ```
  export ADMIN_PASSWORD="your_secure_password"
  ```

---

## Awards and Notifications

### Award Statuses
- **Pending**: Awaiting manager approval
- **Approved**: Approved and ready for notification
- **Rejected**: Manager rejected the award
- **Notified**: Notification email sent to student

### Email Mode
- Currently set to **Mock (Testing)**
- Emails are logged but not actually sent
- To enable real emails, change `MAIL_MODE` in config.py to `'smtp'`

---

## Database & Data

- **Database Type**: SQLite
- **File Location**: `scholarship.db` (created automatically)
- **Data Reset**: Delete the `.db` file to start fresh
- **Backup**: Copy the `scholarship.db` file to backup your data

---

## Rebranding Note

The program has been rebranded from "MSA Scholarship Matcher" to **"Scholarship Allocation Program"** throughout the interface for better general applicability.

---

## Support

For issues or questions:
1. Check browser console (F12) for error messages
2. Review application logs
3. Verify file format matches requirements
4. Ensure role-appropriate user is logged in
