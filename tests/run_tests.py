# runs all 5 test cases from test_cases.md automatically
# run (from main project folder): "python test/run_tests.py"

import os
import sys

# tells python to look at report_generator.py (one folder up) so the import works
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from report_generator import generate_report

# same 5 test cases and fake results as test_cases.md
TESTS = [
    {
        "name": "test case 1: normal HTTPS website (without issues)",
        "results": {
            "website": "https://secure-example.com",
            "score": 100,
            "risk_level": "low",
            "issues": [],
        },
        "should_have": ["score: 100 / 100", "risk level: low", "no issues found."],
        "should_not": ["issues found (", "scan failed"],
    },
    {
        "name": "test case 2: HTTP website (without HTTPS)",
        "results": {
            "website": "http://example.com",
            "score": 55,
            "risk_level": "high",
            "issues": [
                {
                    "issue": "no_https",
                    "severity": "high",
                    "recommendation": "get a TLS certificate and serve the site over HTTPS.",
                },
                {
                    "issue": "no_https_redirect",
                    "severity": "medium",
                    "recommendation": "redirect all HTTP traffic to HTTPS.",
                },
            ],
        },
        "should_have": ["1. No HTTPS", "2. No HTTP to HTTPS Redirect",
                        "risk level: high", "serve the site over HTTPS."],
        # raw ids should not show in the report
        "should_not": ["scan failed", "no_https"],
    },
    {
        "name": "test case 3: missing security headers",
        "results": {
            "website": "https://example.com",
            "score": 80,
            "risk_level": "moderate",
            "issues": [
                {
                    "issue": "missing_csp",
                    "severity": "medium",
                    "recommendation": "add a Content-Security-Policy header to limit where scripts can load from.",
                },
                {
                    "issue": "missing_x_content_type_options",
                    "severity": "low",
                    "recommendation": "add 'X-Content-Type-Options: nosniff' to stop browsers guessing file types.",
                },
            ],
        },
        "should_have": ["Missing Content-Security-Policy Header",
                        "Missing X-Content-Type-Options Header",
                        "issues found (2):", "risk level: moderate"],
        # HTTPS should not be listed as an issue
        "should_not": ["No HTTPS", "scan failed"],
    },
    {
        "name": "test case 4: invalid URL",
        "results": {
            "website": "not-a-real-website",
            "error": "invalid URL or website could not be reached.",
        },
        "should_have": ["scan failed: invalid URL or website could not be reached.",
                        "not-a-real-website"],
        # no score or risk level on a failed scan
        "should_not": ["score:", "risk level:"],
    },
    {
        "name": "test case 5: multiple issues",
        "results": {
            "website": "http://example.com",
            "score": 45,
            "risk_level": "high",
            # out of order on purpose to check sorting
            "issues": [
                {
                    "issue": "missing_x_content_type_options",
                    "severity": "low",
                    "recommendation": "add 'X-Content-Type-Options: nosniff' to stop browsers guessing file types.",
                },
                {
                    "issue": "no_https",
                    "severity": "high",
                    "recommendation": "get a TLS certificate and serve the site over HTTPS.",
                },
                {
                    "issue": "missing_csp",
                    "severity": "medium",
                    "recommendation": "add a Content-Security-Policy header to limit where scripts can load from.",
                },
                {
                    "issue": "missing_hsts",
                    "severity": "medium",
                    "recommendation": "add a Strict-Transport-Security (HSTS) header so browsers always use HTTPS.",
                },
            ],
        },
        # high first, low last
        "should_have": ["issues found (4):", "1. No HTTPS",
                        "4. Missing X-Content-Type-Options Header", "risk level: high"],
        "should_not": ["scan failed"],
    },
]

# run every test and print pass or fail
def run_all_tests():
    passed = 0

    for test in TESTS:
        # if the report crashes, count it as a fail and keep going
        try:
            report = generate_report(test["results"])
        except Exception as error:
            print(f"FAIL  {test['name']}  (crashed: {error})")
            continue

        # collect anything that went wrong
        problems = []
        for text in test["should_have"]:
            if text not in report:
                problems.append(f"missing '{text}'")
        for text in test["should_not"]:
            if text in report:
                problems.append(f"should not show '{text}'")

        if problems:
            print(f"FAIL  {test['name']}")
            for problem in problems:
                print(f"        - {problem}")
        else:
            print(f"PASS  {test['name']}")
            passed += 1

    print(f"\n{passed} / {len(TESTS)} tests passed")


# main program
# run "python test/run_tests.py"
if __name__ == "__main__":
    run_all_tests()