# takes scan results and generates and saves a readible security report
# will be replaced with real data

# shows when scan happened
from datetime import datetime

# dictionary for ids to point to readable names
ISSUE_NAMES = {
    "no_https": "No HTTPS",
    "missing_csp": "Missing Content-Security-Policy Header",
    "missing_hsts": "Missing Strict-Transport-Security Header",
    "missing_x_content_type_options": "Missing X-Content-Type-Options Header",
    "no_https_redirect": "No HTTP to HTTPS Redirect",
}

# lower numbers = higher priority
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# dictionary to store info
fake_results = {
    "website": "http://example.com",
    "score": 45,
    "risk_level": "High",
    "issues": [
        {
            "issue": "missing_x_content_type_options",
            "severity": "low",
            "recommendation": "Add 'X-Content-Type-Options: nosniff' to stop browsers guessing file types.",
        },
        {
            "issue": "no_https",
            "severity": "high",
            "recommendation": "Get a TLS certificate and serve the site over HTTPS.",
        },
        {
            "issue": "missing_csp",
            "severity": "medium",
            "recommendation": "Add a Content-Security-Policy header.",
        },
        {
            "issue": "missing_hsts",
            "severity": "medium",
            "recommendation": "Add a Strict-Transport-Security header so browsers always use HTTPS.",
        },
    ],
}

def get_display_name(issue_id):
    # turns id into readable name 
    return ISSUE_NAMES.get(issue_id, issue_id.replace("_", " ").title())


# generate report
def generate_report(results):
    lines = []

    # header
    lines.append("-" * 80)
    lines.append("")   
    lines.append("WEBSITE SECURITY REPORT")
    lines.append("")   
    lines.append("-" * 80)
    lines.append("")   

    # current date and time
    lines.append(f"date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # website info (or "unknown" if not found)
    lines.append(f"website: {results.get('website', 'Unknown')}")

    # failed scan, show error message and exit early
    if "error" in results:
        lines.append("")
        lines.append(f"scan failed: {results['error']}")
        lines.append("Please check the URL and try again.")
        lines.append("-" * 80)
        return "\n".join(lines)

    # score and risk level
    lines.append(f"score: {results.get('score', 'N/A')} / 100")
    lines.append(f"risk level: {results.get('risk_level', 'N/A')}")
    lines.append("")

    # issues (or empty list if not found)
    issues = results.get("issues", [])

    # if no issues found
    if not issues:
        lines.append("no issues found.")

    # list every issue
    else:
        lines.append(f"issues found ({len(issues)}):")
        # sort issues by severity
        sorted_issues = sorted(
            issues, key=lambda item: SEVERITY_ORDER.get(item["severity"].lower(), 3)
        )
        # sorts and numbers issues
        for number, item in enumerate(sorted_issues, start=1):
            lines.append(f"{number}. {get_display_name(item['issue'])}")
            lines.append(f" severity: {item['severity'].capitalize()}")
            lines.append(f" recommendation: {item['recommendation']}")
            # blank line between issues
            lines.append("")   

    # footer
    lines.append("-" * 80)

    # join every line into a single string and send it back
    return "\n".join(lines)

# save report to a file
def save_report(report_text, filename = "security_report.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_text)

    print(f"\nreport saved to {filename}")


# main program
# run "python3 report_generator.py"
if __name__ == "__main__":
    report = generate_report(fake_results)
    save_report(report)
