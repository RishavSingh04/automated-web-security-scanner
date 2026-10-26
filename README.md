# 🔐 Automated Web Security Scanner

### A Python-Based Tool for Basic Website Security Assessment

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Domain](https://img.shields.io/badge/Domain-Cybersecurity-0A7EA4)
![Testing](https://img.shields.io/badge/Tests-unittest-success)
![Output](https://img.shields.io/badge/Report-JSON-orange)

**Automated Web Security Scanner** is an educational Python command-line project that inspects selected HTTP response properties, checks common security headers, performs a preliminary CORS header observation, and exports findings to JSON.

Prepared for the **IBM SkillsBuild Cyber Security BootCamp 2026**, conducted by **BharatCares**.

> This is an educational prototype, not a comprehensive vulnerability scanner. Only scan systems you own or are explicitly authorized to assess.

## Author

- **Name:** Rishav Singh
- **Degree:** Bachelor of Technology (B.Tech.)
- **Branch:** Computer Engineering (CE)
- **Institution:** Aditya Silver Oak Institute of Technology

## Contents

- [Overview](#overview)
- [Objectives](#objectives)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture and Workflow](#architecture-and-workflow)
- [Checks Performed](#checks-performed)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [JSON Report](#json-report)
- [Analysis and Interpretation](#analysis-and-interpretation)
- [Limitations](#limitations)
- [Ethical Use](#ethical-use)
- [Future Enhancements](#future-enhancements)
- [References](#references)

## Overview

HTTP security headers influence how browsers handle content, framing, transport security, and referrer information. CORS response headers influence browser-based access to cross-origin resources. This project provides a small, repeatable way to observe selected response properties and save them in a structured report.

## Objectives

- Check whether the entered URL uses HTTPS.
- Record the HTTP status code returned by the target.
- Inspect five common HTTP security headers.
- Observe the `Access-Control-Allow-Origin` response header.
- Export scan metadata and findings to `scan_report.json`.
- Practise Python exception handling and JSON serialization.
- Run repeatable tests using `unittest` and mocked HTTP responses.

## Features

1. **HTTPS scheme check** — identifies whether the supplied URL uses HTTP or HTTPS.
2. **HTTP status capture** — records the status code when a response is received.
3. **Security header inspection** — checks header presence and explains the general purpose of missing headers.
4. **Basic CORS observation** — reports whether `Access-Control-Allow-Origin` is absent, wildcard, or another value.
5. **JSON report generation** — stores target, timestamp, status, and individual findings.
6. **Timeout and request error handling** — avoids waiting indefinitely on ordinary request operations and reports request exceptions.
7. **Automated tests** — tests selected paths with mock responses.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main implementation |
| Requests | HTTP requests and response inspection |
| JSON | Machine-readable findings report |
| pathlib | Report file path handling |
| datetime | Scan timestamp |
| unittest / unittest.mock | Automated tests and mock responses |
| Visual Studio Code | Development environment |

## Architecture and Workflow

```text
User enters URL
      |
      v
Basic URL parsing
      |
      v
HTTP request (timeout; redirects disabled)
      |
      v
Record status and inspect response headers
      |
      +--> HTTPS scheme check
      +--> Five security-header checks
      +--> Basic CORS observation
      |
      v
Collect findings
      |
      v
Write scan_report.json
```

## Checks Performed

| Check | Purpose | Important caveat |
|---|---|---|
| HTTPS scheme | Identifies whether the input URL uses HTTPS | Does not independently audit the full TLS configuration |
| HTTP status | Records the response status | A `200` status is not proof of security |
| `Content-Security-Policy` | Can constrain content sources and reduce certain injection risks | Directives are not fully validated |
| `Strict-Transport-Security` | Can tell supporting browsers to enforce HTTPS | Presence alone does not establish correct configuration |
| `X-Content-Type-Options` | Helps prevent MIME-type sniffing | Value and context are not deeply validated |
| `X-Frame-Options` | Can mitigate some framing/clickjacking risks | Does not perform a complete clickjacking assessment |
| `Referrer-Policy` | Controls referrer information | Policy value is not assessed in depth |
| Basic CORS | Observes `Access-Control-Allow-Origin` | One header is not enough to establish a CORS vulnerability |

Missing headers are observations for review, not automatically confirmed vulnerabilities. Likewise, a present header does not guarantee that the policy is effective.

## Project Structure

```text
automated-web-security-scanner/
├── automated_web_security_scanner.py
├── test_scanner.py
├── requirements.txt
├── README.md
├── scan_report.json          # created when scanner runs
└── .venv/                    # local environment; do not submit
```

The Jupyter Notebook version is also included in this submission bundle.

## Prerequisites

- Python 3.11 or a compatible version.
- Internet access for scanning an authorized public test target.
- Windows, macOS, or Linux.
- A terminal or Visual Studio Code.

## Installation

### 1. Open the project folder

Open a terminal in the folder containing `automated_web_security_scanner.py`.

### 2. Create a virtual environment

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```bat
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the scanner:

```bash
python automated_web_security_scanner.py
```

When prompted, enter a website you own or are explicitly authorized to test. For a basic demonstration, `https://example.com` may be used.

The scanner prints the HTTP status, HTTPS scheme observation, header results, and CORS observation. It then attempts to save `scan_report.json` beside the Python script.

## Testing

Run the automated tests:

```bash
python -m unittest -v test_scanner.py
```

The test suite includes a mocked successful HTTPS response, basic invalid URL handling, and a localhost rejection check. Always run tests against the final version of the source files before submission.

## JSON Report

The generated `scan_report.json` contains:

- Project name
- Target URL
- Timestamp
- HTTP status when a response is received
- A list of findings, each with a check name, status, and details

The current version writes to a fixed filename, so a new run may overwrite the previous report. Copy or archive reports if you need a history.

## Analysis and Interpretation

- **HTTP 200:** The server returned a successful HTTP response for that request; this does not certify the website as secure.
- **Missing security header:** Review the endpoint and application context before deciding whether remediation is required.
- **Wildcard CORS:** Review whether public cross-origin access is intended. A wildcard is not automatically a vulnerability.
- **HTTPS scheme:** The input uses HTTPS, but this check is not a full certificate or TLS configuration audit.
- **Test results:** Passing unit tests demonstrate only the paths covered by those tests, not comprehensive security coverage.

## Limitations

- URL validation is basic and does not provide complete SSRF protection.
- The code does not fully protect against DNS rebinding, private-network access, cloud metadata endpoints, or unsafe redirect destinations.
- Redirects are not automatically followed or comprehensively assessed.
- Header directives are not fully validated.
- CORS analysis is preliminary.
- The scanner does not test authentication, authorization, injection, or application logic.
- A small test suite cannot establish production readiness.

Do not expose this prototype as a public scanning service until strict destination validation, redirect checks, network egress controls, and additional security testing have been implemented.

## Ethical Use

- Scan only systems you own or have explicit permission to assess.
- Follow applicable laws, policies, and scope restrictions.
- Do not use the tool for exploitation, brute force, denial of service, or access-control bypass.
- Keep reports private if they contain sensitive target details.
- Use the scanner for educational and defensive purposes only.

## Future Enhancements

- Strict URL, hostname, and IP-address validation.
- Robust SSRF defenses, including DNS and redirect destination controls.
- More tests for timeout, connection failure, malformed input, and JSON structure.
- Header directive validation and context-aware findings.
- Timestamped report history.
- Optional Streamlit interface and HTML/PDF export.
- Improved logging and documented severity criteria.

These are proposed enhancements, not features claimed to be implemented in this version.

## References

- [Python Documentation](https://docs.python.org/3/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [Python unittest](https://docs.python.org/3/library/unittest.html)
- [MDN HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)

---

**Project:** Automated Web Security Scanner  
**Program:** IBM SkillsBuild Cyber Security BootCamp 2026  
**Conducted by:** BharatCares  
**Author:** Rishav Singh  
**Institution:** Aditya Silver Oak Institute of Technology
