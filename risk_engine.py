# Risk scoring
# Original component: Brett
# Integration/compatibility updates: Valeria

ORIGINAL_SCORE = 100

HIGH_RISK = ["no_https", "no_https_redirect"]
MEDIUM_RISK = ["missing_hsts", "missing_csp", "missing_x_frame_options"]
LOW_RISK = ["missing_x_content_type_options", "missing_referrer_policy", "missing_permissions_policy"]

def scoring_system(issues_list):
    """
    Calculates a security score starting from 100.
    """

    score = ORIGINAL_SCORE

    for issue in issues_list:
        if issue in HIGH_RISK:
            score -= 30
        elif issue in MEDIUM_RISK:
            score -= 15
        elif issue in LOW_RISK:
            score -= 5

    return max(score, 0)