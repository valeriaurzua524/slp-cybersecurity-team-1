# Always begin score at 100
ORIGINAL_SCORE = 100

test_risks = ["missing CSP", "no HTTPS", "missing HSTS"]

HIGH_RISK = ["missing CSP", "missing HSTS", "no HTTPS redirect"]
MEDIUM_RISK = ["missing X-Content-Type-Options"]
LOW_RISK = ["no HTTPS"]

def scoring_system(issues_list):
    score = ORIGINAL_SCORE

    for issue in issues_list:
        if issue in HIGH_RISK:
            score -= 10
        elif issue in MEDIUM_RISK:
            score -= 5
        else:
            score -= 1

    return score

print(scoring_system(test_risks))