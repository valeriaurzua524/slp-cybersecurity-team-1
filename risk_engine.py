# Always begin score at 100
ORIGINAL_SCORE = 100

test_risks = ["missing_csp", "no_https", "missing_hsts"]

HIGH_RISK = ["no_https", "no_https_redirect"]
MEDIUM_RISK = ["missing_hsts", "missing_csp"]
LOW_RISK = ["missing_x_content_type_options"]

def scoring_system(issues_list):
    score = ORIGINAL_SCORE

    for issue in issues_list:
        if issue in HIGH_RISK:
            score -= 10
        elif issue in MEDIUM_RISK:
            score -= 5
        elif issue in LOW_RISK:
            score -= 1

    return score

print(scoring_system(test_risks))