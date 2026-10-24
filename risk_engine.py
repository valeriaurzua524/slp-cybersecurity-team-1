# Risk scoring
# Original component: Brett
# Integration/compatibility updates: Valeria

ORIGINAL_SCORE = 100

HIGH_RISK = ["no_https", "no_https_redirect"]
MEDIUM_RISK = ["missing_hsts", "missing_csp"]
LOW_RISK = ["missing_x_content_type_options"]


def scoring_system(issues_list):
    """
    Calculates a security score starting from 100.
    """

    score = ORIGINAL_SCORE

    for issue in issues_list:
        if issue in HIGH_RISK:
            score -= 10
        elif issue in MEDIUM_RISK:
            score -= 5
        elif issue in LOW_RISK:
            score -= 1

    return max(score, 0)