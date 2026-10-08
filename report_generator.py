# takes scan results and generates and saves a readible security report
# will be replaced with real data

# shows when scan happened
from datetime import datetime

# dictionary to store info
fake_results = {
    "website": "https://example.com",       # website scanned
    "score": 45,                            # security score out of 100
    "risk_level": "high",                   # low/moderate/high
    #list of dictionaries of each security problem
    "issues": [
        {
            "issue": "no HTTPS",
            "severity": "high",
            "recommendation": "get a TLS certificate and serve the site over HTTPS.",
        },
        {
            "issue": "missing Content-Security-Policy header",
            "severity": "medium",
            "recommendation": "add a Content-Security-Policy header to limit where scripts can load from.",
        },
        {
            "issue": "missing Strict-Transport-Security header",
            "severity": "medium",
            "recommendation": "add a Strict-Transport-Security (HSTS) header so browsers always use HTTPS.",
        },
        {
            "issue": "missing X-Content-Type-Options header",
            "severity": "low",
            "recommendation": "add 'X-Content-Type-Options: nosniff' to stop browsers guessing file types.",
        },
    ],
}

# severity order to place issues in report, lower numbers = higher priority
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

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

    # score and risk level
    lines.append(f"score: {results['score']} / 100")
    lines.append(f"risk level:  {results['risk_level']}")
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
            issues, key=lambda item: SEVERITY_ORDER.get(item["severity"], 3)
        )
        # sorts and numbers issues
        for number, item in enumerate(sorted_issues, start=1):
            lines.append(f"{number}. {item['issue']}")
            lines.append(f" severity: {item['severity']}")
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