import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests


def check_website(url):
    """Perform basic, educational checks on an authorized website."""
    url = url.strip()

    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    parsed = urlparse(url)

    # Basic syntax checks only; this is not complete SSRF protection.
    if (
        parsed.scheme not in ("https", "http")
        or not parsed.hostname
        or any(char.isspace() for char in parsed.netloc)
    ):
        print("Error: Please enter a valid HTTP or HTTPS URL.")
        return

    # Prevent a few common local targets in this educational prototype.
    # This is NOT sufficient protection for a public scanning service.
    if parsed.hostname.lower() in ("localhost", "127.0.0.1", "::1"):
        print("Error: Localhost scanning is disabled.")
        return

    report = {
        "project": "Automated Web Security Scanner",
        "target": url,
        "scan_time": datetime.now().astimezone().isoformat(),
        "http_status": None,
        "findings": [],
    }

    def add_finding(check, status, details):
        report["findings"].append({
            "check": check,
            "status": status,
            "details": details,
        })

    print("\n=== Automated Web Security Scanner ===")
    print(f"Target: {url}")

    response = None
    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=False,
            stream=True,
            headers={"User-Agent": "EducationalSecurityScanner/1.0"},
        )

        report["http_status"] = response.status_code
        print(f"HTTP Status: {response.status_code}")

        if parsed.scheme == "https":
            add_finding("HTTPS", "PASS", "Target URL uses HTTPS.")
            print("[PASS] Target URL uses HTTPS")
        else:
            add_finding("HTTPS", "WARNING", "Target URL uses HTTP.")
            print("[WARNING] Target URL uses HTTP, not HTTPS")

        headers = response.headers
        security_headers = {
            "Content-Security-Policy":
                "Helps reduce certain content injection risks.",
            "Strict-Transport-Security":
                "Helps supporting browsers enforce HTTPS.",
            "X-Content-Type-Options":
                "Helps prevent MIME-type sniffing.",
            "X-Frame-Options":
                "Can help mitigate clickjacking.",
            "Referrer-Policy":
                "Controls referrer information.",
        }

        print("\n--- Security Header Checks ---")
        for header, purpose in security_headers.items():
            if header in headers:
                status = "PASS"
                details = "Header is present."
            else:
                status = "WARNING"
                details = f"Header is missing. {purpose}"

            add_finding(header, status, details)
            print(f"[{status}] {header}: {details}")

        print("\n--- Basic CORS Check ---")
        cors = headers.get("Access-Control-Allow-Origin")
        if cors is None:
            add_finding(
                "CORS", "INFO",
                "CORS header was not present in this response.",
            )
            print("[INFO] No Access-Control-Allow-Origin header in this response.")
        elif cors.strip() == "*":
            add_finding(
                "CORS", "REVIEW",
                "Wildcard origin detected; assess whether it is appropriate.",
            )
            print("[REVIEW] CORS allows any origin; assess whether this is appropriate.")
        else:
            add_finding("CORS", "INFO", f"Access-Control-Allow-Origin: {cors}")
            print(f"[INFO] CORS origin configured as: {cors}")

    except requests.RequestException as error:
        add_finding("Connection", "ERROR", str(error))
        print(f"Scan failed: {error}")
    finally:
        if response is not None:
            response.close()

    report_path = Path(__file__).resolve().parent / "scan_report.json"
    try:
        with report_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4, ensure_ascii=False)
        print(f"\nReport saved to: {report_path}")
    except OSError as error:
        print(f"Could not save JSON report: {error}")

    print("Scan completed.")
    print("Note: Missing headers alone do not prove a vulnerability.")


if __name__ == "__main__":
    target = input(
        "Enter a website URL you own or are authorized to test: "
    ).strip()
    check_website(target)
