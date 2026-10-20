# This program doesn't have website since the scanner will have that.
import datetime
import risk_engine

test_risks = ["missing_csp", "no_https", "missing_hsts"]
HIGH_RISK_LIST = risk_engine.HIGH_RISK
MEDIUM_RISK_LIST = risk_engine.MEDIUM_RISK
LOW_RISK_LIST = risk_engine.LOW_RISK


EMPTY_DICTIONARY = {
    "date": None,
    "website": None,
    "score": 100,
    "risk_level": None,
    "issue_count": 0,
    "issue_list": [],
}

EMPTY_ISSUE = {
    "issue": None,
    "severity": None,
    "recommendation": None,
}

def recommendations(issues_list):
    risk_dictionary = EMPTY_DICTIONARY

    # update date
    risk_dictionary.update({"date": str(datetime.datetime.now())})

    # update score
    risk_dictionary.update({"score": risk_engine.scoring_system(issues_list)})

    # update issue_count
    risk_dictionary.update({"issue_count": len(issues_list)})

    # update risk_level
    if set(issues_list) & set(HIGH_RISK_LIST):
        risk_dictionary.update({"risk_level": "high"})
    elif set(issues_list) & set(MEDIUM_RISK_LIST):
        risk_dictionary.update({"risk_level": "medium"})
    elif set(issues_list) & set(LOW_RISK_LIST):
        risk_dictionary.update({"risk_level": "low"})
    else:
        risk_dictionary.update({"risk_level": "none"})

    # update issue_list
    for issue in issues_list:
        # creates the issue to be added
        temporary_issue = EMPTY_ISSUE

        temporary_issue.update({"issue": issue})

        if issue in HIGH_RISK_LIST:
            temporary_issue.update({"severity": "high"})
        elif issue in MEDIUM_RISK_LIST:
            temporary_issue.update({"severity": "medium"})
        elif issue in LOW_RISK_LIST:
            temporary_issue.update({"severity": "low"})

        match issue:
            case "no_https":
                temporary_issue.update({"recommendation": "contact website owner or proceed at your own risk"})
            case "no_https_redirect":
                temporary_issue.update({"recommendation": "redirect all HTTP traffic to HTTPS"})
            case "missing_hsts":
                temporary_issue.update({"recommendation": "ensure connection is over HTTPS"})
            case "missing_csp":
                temporary_issue.update({"recommendation": "use caution when interacting with the website"})
            case "missing_x_content_type_options":
                temporary_issue.update({"recommendation": "use caution when interacting with the website"})

        risk_dictionary["issue_list"].append(temporary_issue)

    return risk_dictionary

print(recommendations(test_risks))