import smtplib
import csv
import time
import random
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date

# ─────────────────────────────────────────
#  CONFIG — edit these
# ─────────────────────────────────────────

MY_NAME = ""
MY_EMAIL = ""
MY_PASSWORD = ""
MY_PHONE_NUMBER = ""
MY_LINKEDIN_URL = ""
MY_GITHUB_URL = ""
MY_PORTFOLIO_URL = ""
DAILY_LIMIT_PER_ACCOUNT = 30   # emails per account per day
CSV_FILE = "good_companies.csv"
RESUME_PATH = "YASH_HARKAWAT_RESUME.pdf"   # keep resume in same folder as script



ACCOUNTS = [
    {"email": MY_EMAIL,  "password": MY_PASSWORD},
]

# ─────────────────────────────────────────
#  EMAIL TEMPLATE — edit the body
# ─────────────────────────────────────────

def build_email(from_email, to_email, company, recipient_name=None):
    subject = f"Software Engineer - {MY_NAME} | Open to Opportunities at {company}"

    greeting = f"Hi {recipient_name}," if recipient_name else "Hi,"
    body = f"""{greeting}

I hope you're doing well. I'm {MY_NAME}, reaching out regarding software development opportunities at {company}.

I currently work as a Full-Stack Developer at Pulse Energy Technologies, Bengaluru, specializing in React.js and Node.js. I graduated from IIT Kharagpur in 2023 with a B.Tech + M.Tech in Electrical Engineering, and have hands-on experience with React, Redux, TypeScript, Node.js, and AWS.

I've attached my resume for your reference. Please let me know if there are any suitable opportunities — I'd love to connect!

Best regards,
{MY_NAME}
{MY_PHONE_NUMBER}
{MY_EMAIL}
LinkedIn:  {MY_LINKEDIN_URL}
GitHub:    {MY_GITHUB_URL}
Portfolio: {MY_PORTFOLIO_URL}"""

    # Build multipart message (text + attachment)
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"]    = from_email
    msg["To"]      = to_email
    msg.attach(MIMEText(body, "plain"))

    # Attach resume if file exists
    if os.path.exists(RESUME_PATH):
        with open(RESUME_PATH, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="Yash_Harkawat_Resume.pdf"'
        )
        msg.attach(part)
    else:
        print(f"  ⚠️  Resume not found at '{RESUME_PATH}' — sending without attachment.")

    return msg

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────

def connect(account):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(account["email"], account["password"])
    print(f"  Logged in as {account['email']}")
    return server


def save(rows, fieldnames):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def count_sent_today(rows, account_email):
    today = str(date.today())
    return sum(
        1 for r in rows
        if r.get("sent_by") == account_email and r.get("sent_date") == today
    )

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────

def main():
    # Load CSV
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Add new columns if missing
    for col in ["status", "sent_by", "sent_date"]:
        if col not in fieldnames:
            fieldnames.append(col)
        for row in rows:
            row.setdefault(col, "")

    today = str(date.today())
    pending = [r for r in rows if r["status"] not in ("sent",)]

    print(f"\n📋 Total rows: {len(rows)}  |  Pending: {len(pending)}\n")

    if not pending:
        print("✅ Nothing left to send.")
        return

    for account in ACCOUNTS:
        sent_today = count_sent_today(rows, account["email"])
        remaining  = DAILY_LIMIT_PER_ACCOUNT - sent_today

        if remaining <= 0:
            print(f"⚠️  {account['email']} hit daily limit ({DAILY_LIMIT_PER_ACCOUNT}). Skipping.")
            continue

        print(f"\n📤 Using {account['email']}  |  Can send: {remaining} today\n")

        try:
            server = connect(account)
        except Exception as e:
            print(f"  ❌ Login failed for {account['email']}: {e}")
            continue

        sent_this_session = 0

        for row in rows:
            if row["status"] == "sent":
                continue
            if sent_this_session >= remaining:
                print(f"\n  Daily limit reached for {account['email']}.")
                break

            company = row.get("Company") or row.get("company", "the company")
            to      = row.get("mails") or row.get("Email") or row.get("email", "")
            name    = row.get("Name", "").strip() or None
            if not to:
                continue

            try:
                msg = build_email(account["email"], to, company, recipient_name=name)
                server.sendmail(account["email"], to, msg.as_string())

                row["status"]    = "sent"
                row["sent_by"]   = account["email"]
                row["sent_date"] = today

                print(f"  ✅ Sent → {to}")
                sent_this_session += 1

            except Exception as e:
                row["status"] = "failed"
                print(f"  ❌ Failed → {to}  ({e})")

            # Save progress after every email
            save(rows, fieldnames)

            # Human-like delay (120–180 seconds)
            delay = random.randint(120, 180)
            print(f"     Waiting {delay}s...")
            time.sleep(delay)

        server.quit()
        print(f"\n  Session done for {account['email']}. Sent: {sent_this_session}")

    # Summary
    total_sent   = sum(1 for r in rows if r["status"] == "sent")
    total_failed = sum(1 for r in rows if r["status"] == "failed")
    total_left   = sum(1 for r in rows if r["status"] not in ("sent", "failed"))

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━
📊 Summary
   Sent    : {total_sent}
   Failed  : {total_failed}
   Pending : {total_left}
━━━━━━━━━━━━━━━━━━━━━━
""")


if __name__ == "__main__":
    main()