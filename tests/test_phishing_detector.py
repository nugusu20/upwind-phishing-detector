import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phishing_detector import analyze_email


def test_legitimate_email_has_no_findings():
    email_content = """
From: support@example.com
Subject: Account Update

This is a regular account update.
"""

    findings = analyze_email(email_content)

    assert findings == []


def test_combined_phishing_email_detects_multiple_indicators():
    email_content = """
From: security@examp1e.com
Subject: Urgent Action Required

Please verify now immediately.

http://192.168.1.50/login
https://secure-login-update.xyz/account
"""

    findings = analyze_email(email_content)

    assert any("IP address used in URL" in finding for finding in findings)
    assert any("Uncommon domain used in URL" in finding for finding in findings)
    assert any("Possible spoofed sender" in finding for finding in findings)
    assert any("Urgent language detected" in finding for finding in findings)
