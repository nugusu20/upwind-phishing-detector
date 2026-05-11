# Upwind Email Phishing Detector

## 1. Project Overview

This project was built as part of the Upwind home assignment.

The goal is to implement an Email Phishing Detector that scans email content, detects common phishing indicators, and alerts the user when a message looks suspicious.

The solution includes:

- A command-line phishing detection script.
- Sample email files for testing different phishing indicators.
- A web UI for uploading email content and viewing scan results.
- A Gmail Add-on prototype for scanning messages directly from Gmail.

---

## 2. Assignment Scope

### Required Scope

The assignment required building a script that accepts an email text file and scans it for common phishing indicators.

The required indicators are:

- Suspicious links:
  - URLs with uncommon domains.
  - URLs that use IP addresses.
- Spoofed sender addresses.
- Urgent language such as `urgent`, `immediately`, and `action required`.

The script also needs to print a clear summary that shows whether the email is likely a phishing attempt and list the detected indicators.

### Bonus Scope

The official bonus requirements are:

- A user interface for uploading email content and displaying the results.
- A Gmail Add-on that allows users to scan emails directly from their inbox.

---

## 3. What I Built

I built a local phishing detection tool in Python.

The core detection logic is implemented in:

```text
src/phishing_detector.py
```

The web UI bonus is implemented in:

```text
src/web_app.py
src/templates/index.html
```

The Gmail Add-on prototype is implemented in:

```text
gmail-addon/Code.gs
gmail-addon/appsscript.json
gmail-addon/README.md
```

---

## 4. Why I Built It This Way

I started with the required command-line script first, because the assignment specifically asks for a script that accepts a text file containing email content.

After the required logic was working, I added the official UI bonus using Flask. This allows a user to upload an email text file from the browser and see the phishing detection results.

Finally, I added a Gmail Add-on prototype using Google Apps Script to address the second bonus requirement. This part is designed to integrate with Gmail and scan the currently opened email message.

This approach keeps the solution aligned with the assignment while also showing practical DevOps, system, and security thinking.

---

## 5. Detection Logic

The detector checks for the following indicators:

### IP Address Used in URL

Example:

```text
http://192.168.1.50/login
```

This is suspicious because phishing emails sometimes use raw IP addresses instead of trusted domains.

### Uncommon Domain in URL

Example:

```text
https://secure-login-update.xyz/account
```

The detector flags uncommon top-level domains such as `.xyz`, `.top`, `.click`, `.zip`, `.review`, `.country`, and `.stream`.

### Possible Spoofed Sender

Example:

```text
security@examp1e.com
```

This looks similar to:

```text
example.com
```

The detector compares the sender domain against known legitimate domains and flags similar-looking domains.

### Urgent Language

Examples:

```text
urgent
immediately
action required
verify now
account suspended
```

These terms are commonly used in phishing attempts to pressure the user into acting quickly.

---

## 6. How to Run the CLI Detector

Run the detector on a sample email:

```bash
python3 src/phishing_detector.py samples/phishing_combined.txt
```

Expected example output:

```text
=== Email Phishing Detection Summary ===
Likely phishing attempt: YES
Detected indicators: 7
- IP address used in URL: http://192.168.1.50/login
- Uncommon domain used in URL: https://secure-login-update.xyz/account
- Possible spoofed sender: security@examp1e.com looks similar to example.com
- Urgent language detected: action required
- Urgent language detected: immediately
- Urgent language detected: urgent
- Urgent language detected: verify now
```

Run the detector on a legitimate sample:

```bash
python3 src/phishing_detector.py samples/sample_email.txt
```

Expected example output:

```text
=== Email Phishing Detection Summary ===
Likely phishing attempt: NO
Detected indicators: 0
- No suspicious indicators detected.
```

---

## 7. How to Run the Web UI

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the Flask web application:

```bash
python3 src/web_app.py
```

Open the browser:

```text
http://127.0.0.1:5000
```

Upload one of the sample files from the `samples/` folder and scan it.

---

## 8. Gmail Add-on Prototype

The Gmail Add-on prototype is stored under:

```text
gmail-addon/
```

It includes:

- `appsscript.json` - Google Apps Script manifest.
- `Code.gs` - Gmail Add-on logic.
- `README.md` - Explanation of the add-on prototype.

The purpose of this prototype is to scan the currently opened Gmail message and display phishing detection results inside the Gmail interface.

This part is not executed from Linux or WSL. It is designed to run in Google Apps Script as part of Google Workspace.

---

## 9. Project Structure

```text
.
├── gmail-addon/
│   ├── Code.gs
│   ├── README.md
│   └── appsscript.json
├── samples/
│   ├── phishing_combined.txt
│   ├── phishing_ip_url.txt
│   ├── phishing_spoofed_sender.txt
│   ├── phishing_uncommon_domain.txt
│   ├── phishing_urgent_language.txt
│   └── sample_email.txt
├── src/
│   ├── phishing_detector.py
│   ├── web_app.py
│   └── templates/
│       └── index.html
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 10. Security Notes

This project is a safe local prototype.

It does not attack external systems, does not send emails, does not scan real inboxes without user interaction, and does not perform offensive activity.

All phishing examples are local sample text files created only for demonstration and testing.

---

## 11. Professional Enhancements

In addition to the official assignment requirements, the project includes:

- Clean project structure.
- Python virtual environment support.
- `.gitignore` for clean Git usage.
- Sample email files for repeatable testing.
- Clear README documentation for technical review and presentation.

---

## Environment Setup

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

This keeps the project dependencies isolated from the system Python environment.
