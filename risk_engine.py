# Risk scoring
# Original component: Brett
# Integration/compatibility updates: Valeria

ORIGINAL_SCORE = 100

# High-risk issues
HIGH_RISK = [
    "no_https",
    "no_https_redirect",
]

# Medium-risk issues
MEDIUM_RISK = [
    "missing_hsts",
    "missing_csp",
    "missing_x_frame_options",
]

# Low-risk issues
LOW_RISK = [
    "missing_x_content_type_options",
    "missing_referrer_policy",
    "missing_permissions_policy",
]


def scoring_system(issues_list):
    """
    Calculates a security score starting from 100.

    High-risk issue:   -20 points
    Medium-risk issue: -10 points
    Low-risk issue:    -5 points
    """

    score = ORIGINAL_SCORE

    for issue in issues_list:

        if issue in HIGH_RISK:
            score -= 20

        elif issue in MEDIUM_RISK:
            score -= 10

        elif issue in LOW_RISK:
            score -= 5

    return max(score, 0)