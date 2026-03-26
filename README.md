# 📧 Cold Email Sender — Setup & Usage Guide

A simple Python script to send personalized cold emails with your resume attached, across multiple Gmail accounts, with daily limits and resume tracking.

---

## 📁 Folder Structure

Make sure all these files are in the **same folder**:

```
📁 your-folder/
   send_emails.py
   emails.csv
   YASH_HARKAWAT_RESUME.pdf
   README.md
```

---

## ✅ Step 1 — Install Python

Check if Python is installed:

```bash
python3 --version
```

If not installed, download from: https://www.python.org/downloads/

> On Mac, you can also run: `brew install python`

---

## ✅ Step 2 — Create a Gmail App Password

Your regular Gmail password won't work. You need an **App Password**.

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** (required)
3. Go to https://myaccount.google.com/apppasswords
4. Type any name (e.g. `email script`) → click **Create**
5. Copy the **16-character password** shown

> Repeat this for each Gmail account you want to use.

---

## ✅ Step 3 — Configure the Script

Open `send_emails.py` and edit the **CONFIG** section at the top:

```python
ACCOUNTS = [
    {"email": "your_email@gmail.com", "password": "xxxx xxxx xxxx xxxx"},
    # Add more accounts if needed
]

DAILY_LIMIT_PER_ACCOUNT = 80   # max emails per account per day
```

> Replace `xxxx xxxx xxxx xxxx` with the App Password from Step 2.

---

## ✅ Step 4 — Prepare Your Email List (CSV)

Open `emails.csv` and fill in your contacts. The format is:

```
name,email,company,status,sent_by,sent_date
Praveen,praveen@goldman.com,Goldman Sachs,,,
Rahul,rahul@example.com,Google,,,
```

**Rules:**
- `status` column — leave blank for new contacts. The script fills this in automatically (`sent` / `failed`)
- Do **not** delete the header row
- Close the file before running the script (Excel/Numbers locks it)

---

## ✅ Step 5 — Run the Script

Open terminal, navigate to your folder, and run:

```bash
cd /path/to/your-folder
python3 send_emails.py
```

**Example output:**
```
📋 Total rows: 50  |  Pending: 48

📤 Using your_email@gmail.com  |  Can send: 80 today

  ✅ Sent → praveen@goldman.com
     Waiting 87s...
  ✅ Sent → rahul@example.com
     Waiting 103s...

━━━━━━━━━━━━━━━━━━━━━━
📊 Summary
   Sent    : 2
   Failed  : 0
   Pending : 46
━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔁 Resuming After Stopping

You can **stop the script anytime** (Ctrl+C) and run it again later.

It automatically skips emails already marked as `sent` in the CSV and continues from where it left off.

---

## ⚠️ Important Rules (Don't Skip)

| Rule | Why |
|------|-----|
| Max 80–100 emails/day per account | Gmail bans accounts that send too many |
| Don't remove the delay in the script | Looks human, avoids spam detection |
| Don't send the same message to 500 people at once | Triggers spam filters |
| Warm up new Gmail accounts slowly | Start with 20/day → increase gradually |

---

## 🛠️ Troubleshooting

**`python: command not found`**
→ Use `python3` instead of `python`

**`Login failed: Application-specific password required`**
→ You used your regular Gmail password. Go back to Step 2 and create an App Password.

**`Resume not found`**
→ Make sure `YASH_HARKAWAT_RESUME.pdf` is in the same folder as the script, with the exact same filename.

**`Permission denied` on CSV**
→ Close the CSV file in Excel/Numbers before running the script.

---

## 📬 Daily Workflow

1. Add new contacts to `emails.csv`
2. Run `python3 send_emails.py`
3. Script sends up to 80 emails, then stops
4. Run again the next day — it continues automatically
