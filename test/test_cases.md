test cases - security scanner report

these test cases describe what the scanner and report generator should do in different situations. for now, each one can be tested by changing fake_results in report_generator.py to match the input below and running:
    python3 report_generator.py

test case 1: normal HTTPS website (without issues)
    input: https://secure-example.com, uses HTTPS, has all three security headers, redirects HTTP to HTTPS
    
    fake results to use: 
        fake_results = {
            "website": "https://secure-example.com",
            "score": 100,
            "risk_level": "Low",
            "issues": [],
        }

    expected output:
        score: 100/100
        risk level: low
        report says "no issues found"
        security_report.txt is created


test case 2: HTTP website (without HTTPS)
    input: http://example.com, does not use HTTPS and does not redirect
    
    fake results to use: 
        fake_results = {
            "website": "http://example.com",
            "score": 55,
            "risk_level": "Moderate",
            "issues": [
                {
                    "issue": "No HTTPS",
                    "severity": "High",
                    "recommendation": "Get a TLS certificate and serve the site over HTTPS.",
                },
                {
                    "issue": "No HTTP to HTTPS redirect",
                    "severity": "Medium",
                    "recommendation": "Redirect all HTTP traffic to HTTPS.",
                },
            ],
        }

    expected output:
        issues listed: "no HTTPS" (high) and "not HTTP to HTTPS redirect"
        score: lower than 100
        risk level: moderate or high
        recommendation: enable HTTPS


test case 3: missing security headers
    input: HTTPS website missing Content-Security-Policy and X-Content-Type-Options
    
    fake results to use: 
        fake_results = {
            "website": "https://example.com",
            "score": 80,
            "risk_level": "Low",
            "issues": [
                {
                    "issue": "missing Content-Security-Policy header",
                    "severity": "medium",
                    "recommendation": "add a Content-Security-Policy header to limit where scripts can load from.",
                },
                {
                    "issue": "missing X-Content-Type-Options header",
                    "severity": "low",
                    "recommendation": "add 'X-Content-Type-Options: nosniff' to stop browsers guessing file types.",
                },
            ],
        }

    expected output:
        both missing headers are listed as separate issues
        each issue has its own severity and recommendation
        HTTPS is not listed as an issue


test case 4: invalid URL
    input: not-a-real-website (or typo)

    fake results to use:
        fake_results = {
            "website": "not-a-real-webiste",
            "error": invalid URL or website could not be reached",
        }

    expected output:
        program does not crash
        report says "scan failed" with the error message
        no score or risk level is shown


test case 5: multiple issues
    input: http://example.com with no HTTPS and all three headers missing

    fake results to use: 
        fake_results = {
            "website": "http://example.com",
            "score": 45,
            "risk_level": "High",
            "issues": [
                {
                    "issue": "Missing X-Content-Type-Options header",
                    "severity": "Low",
                    "recommendation": "Add 'X-Content-Type-Options: nosniff' to stop browsers guessing file types.",
                },
                {
                    "issue": "No HTTPS",
                    "severity": "High",
                    "recommendation": "Get a TLS certificate and serve the site over HTTPS.",
                },
                {
                    "issue": "Missing Content-Security-Policy header",
                    "severity": "Medium",
                    "recommendation": "Add a Content-Security-Policy header to limit where scripts can load from.",
                },
                {
                    "issue": "Missing Strict-Transport-Security header",
                    "severity": "Medium",
                    "recommendation": "Add a Strict-Transport-Security (HSTS) header so browsers always use HTTPS.",
                },
            ],
        }

    expected output: 
        all issues sorted, listed and numbered
        every issue has a recommendation
        risk level is high



these should all be tested with real websited instead of fake data.
