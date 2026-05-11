import argparse
import difflib
import ipaddress
import re
from pathlib import Path
from urllib.parse import urlparse


URL_PATTERN = re.compile(r"https?://[^\s<>'\"]+")
FROM_PATTERN = re.compile(r"^From:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")

UNCOMMON_TLDS = {".xyz", ".top", ".click", ".zip", ".review", ".country", ".stream"}
LEGITIMATE_DOMAINS = {"example.com", "upwind.io", "company.com"}
URGENT_KEYWORDS = {"urgent", "immediately", "action required", "verify now", "account suspended"}


def read_email_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Input path is not a file: {file_path}")

    return path.read_text(encoding="utf-8")


def extract_urls(email_content: str) -> list[str]:
    return URL_PATTERN.findall(email_content)


def extract_sender_email(email_content: str) -> str | None:
    from_match = FROM_PATTERN.search(email_content)

    if not from_match:
        return None

    email_match = EMAIL_PATTERN.search(from_match.group(1))
    return email_match.group(0).lower() if email_match else None


def extract_domain(email_address: str) -> str:
    return email_address.split("@", 1)[1].lower()


def is_ip_address(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def detect_ip_based_urls(urls: list[str]) -> list[str]:
    findings = []

    for url in urls:
        hostname = urlparse(url).hostname

        if hostname and is_ip_address(hostname):
            findings.append(f"IP address used in URL: {url}")

    return findings


def detect_uncommon_domain_urls(urls: list[str]) -> list[str]:
    findings = []

    for url in urls:
        hostname = urlparse(url).hostname or ""

        if any(hostname.endswith(tld) for tld in UNCOMMON_TLDS):
            findings.append(f"Uncommon domain used in URL: {url}")

    return findings


def detect_spoofed_sender(sender_email: str | None) -> list[str]:
    if not sender_email:
        return []

    sender_domain = extract_domain(sender_email)
    findings = []

    for legitimate_domain in LEGITIMATE_DOMAINS:
        similarity = difflib.SequenceMatcher(None, sender_domain, legitimate_domain).ratio()

        if sender_domain != legitimate_domain and similarity >= 0.82:
            findings.append(
                f"Possible spoofed sender: {sender_email} looks similar to {legitimate_domain}"
            )

    return findings


def detect_urgent_language(email_content: str) -> list[str]:
    content_lower = email_content.lower()
    return [
        f"Urgent language detected: {keyword}"
        for keyword in sorted(URGENT_KEYWORDS)
        if keyword in content_lower
    ]


def analyze_email(email_content: str) -> list[str]:
    urls = extract_urls(email_content)
    sender_email = extract_sender_email(email_content)

    findings = []
    findings.extend(detect_ip_based_urls(urls))
    findings.extend(detect_uncommon_domain_urls(urls))
    findings.extend(detect_spoofed_sender(sender_email))
    findings.extend(detect_urgent_language(email_content))

    return findings


def print_summary(findings: list[str]) -> None:
    is_phishing = bool(findings)

    print("=== Email Phishing Detection Summary ===")
    print(f"Likely phishing attempt: {'YES' if is_phishing else 'NO'}")
    print(f"Detected indicators: {len(findings)}")

    if findings:
        for finding in findings:
            print(f"- {finding}")
    else:
        print("- No suspicious indicators detected.")


def main():
    parser = argparse.ArgumentParser(description="Email phishing detector")
    parser.add_argument("email_file", help="Path to a text file containing email content")
    args = parser.parse_args()

    email_content = read_email_file(args.email_file)
    findings = analyze_email(email_content)
    print_summary(findings)


if __name__ == "__main__":
    main()
