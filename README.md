# Cybersecurity Vulnerability & Network Safety Scanner

A beginner-friendly cybersecurity tool developed by **sheCodes SLP Cybersecurity Team #1**.

This project combines website security checks, network information, risk scoring, recommendations, and report generation into one Streamlit application.

## Features

### Website Security Scanner

Checks a website for:

- HTTPS support
- HTTP → HTTPS redirects
- Content-Security-Policy
- Strict-Transport-Security
- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Permissions-Policy

The website scanner provides:

- Security score out of 100
- Overall risk level
- Severity for each finding
- Security recommendations
- Downloadable security report

### Network Security Scanner

Collects information about the user's current device and network, including:

- Operating system and version
- Primary network interface
- Connection type (Wi-Fi or Ethernet)
- Local IPv4 address
- Subnet mask
- Active IPv4 interfaces
- Firewall status

The network scanner has been tested on **macOS** and **Windows 11**.

## Risk Scoring

Website scores begin at **100 points**.

- High-risk finding: **-20 points**
- Medium-risk finding: **-10 points**
- Low-risk finding: **-5 points**

The score is based only on the security indicators checked by this application and should not be considered a complete security assessment.

## Technologies Used

- Python
- Streamlit
- Requests
- psutil
- pandas
- socket
- platform
- subprocess
- Git
- GitHub

## Project Structure

```text
app.py
main.py
website_scanner.py
network_scanner.py
wifi_safety.py
risk_engine.py
recommendations.py
report_generator.py
cyber_team_logo.png
```

### Component Overview

- `app.py` — Streamlit frontend and user interface
- `main.py` — connects the project components
- `website_scanner.py` — website security checks
- `network_scanner.py` — device and network information
- `wifi_safety.py` — firewall status checks
- `risk_engine.py` — security scoring
- `recommendations.py` — severity levels and security recommendations
- `report_generator.py` — generates the downloadable security report

## How to Run

Clone the repository:

```bash
git clone https://github.com/valeriaurzua524/slp-cybersecurity-team-1.git
```

Move into the project folder:

```bash
cd slp-cybersecurity-team-1
```

Install the required packages:

```bash
pip install streamlit requests psutil pandas
```

Run the application:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Team

**Valeria Urzua**  
Team Lead / Integration

**Heaven Neumann**  
Website Security Scanner

**Brett Lam**  
Risk Scoring & Recommendations

**Elizabeth Arellano**  
Network & Device Security

**Ayla Santos**  
Testing, Firewall & Security Report

**Alina Avramenko**  
Frontend / User Interface

## Future Improvements

- Expand firewall support
- Add deeper network vulnerability checks
- Improve scoring with additional security indicators
- Deploy the application online
- Expand reporting and personalized recommendations
