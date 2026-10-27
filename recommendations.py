# This program doesn't have website since the scanner will have that.
# Original component: Brett
# Integration/compatibility updates: Valeria

import datetime
import risk_engine

HIGH_RISK_LIST = risk_engine.HIGH_RISK
MEDIUM_RISK_LIST = risk_engine.MEDIUM_RISK
LOW_RISK_LIST = risk_engine.LOW_RISK

def recommendations(scan_results):

    # get website and issues from scanner results
    website = scan_results.get("website")
    issues_list = scan_results.get("issues", [])

    # if scanner returned an error, pass it through
    if "error" in scan_results:
        return {
            "date": str(datetime.datetime.now()),
            "website": website,
            "error": scan_results.get("error"),
            "message": scan_results.get("message"),
            "issues": [],
        }

    # create a new dictionary for every scan
    risk_dictionary = {
        "date": str(datetime.datetime.now()),
        "website": website,
        "final_url": scan_results.get("final_url"),
        "status_code": scan_results.get("status_code"),
        "uses_https": scan_results.get("uses_https"),
        "redirects_to_https": scan_results.get("redirects_to_https"),
        "score": 100,
        "risk_level": None,
        "issue_count": 0,
        "issues": [],
    }

    # update score
    risk_dictionary.update({
        "score": risk_engine.scoring_system(issues_list)
    })

    # update issue count
    risk_dictionary.update({
        "issue_count": len(issues_list)
    })

    # update risk level
    if set(issues_list) & set(HIGH_RISK_LIST):
        risk_dictionary.update({"risk_level": "high"})

    elif set(issues_list) & set(MEDIUM_RISK_LIST):
        risk_dictionary.update({"risk_level": "moderate"})

    elif set(issues_list) & set(LOW_RISK_LIST):
        risk_dictionary.update({"risk_level": "low"})

    else:
        risk_dictionary.update({"risk_level": "none"})

    # update issues
    for issue in issues_list:

        # create a NEW dictionary for each issue
        temporary_issue = {
            "issue": issue,
            "severity": None,
            "recommendation": None,
        }

        # severity
        if issue in HIGH_RISK_LIST:
            temporary_issue.update({"severity": "high"})

        elif issue in MEDIUM_RISK_LIST:
            temporary_issue.update({"severity": "medium"})

        elif issue in LOW_RISK_LIST:
            temporary_issue.update({"severity": "low"})

        # recommendation
        match issue:

            case "no_https":
                temporary_issue.update({
                    "recommendation":
                    "contact website owner or proceed at your own risk"
                })

            case "no_https_redirect":
                temporary_issue.update({
                    "recommendation":
                    "redirect all HTTP traffic to HTTPS"
                })

            case "missing_hsts":
                temporary_issue.update({
                    "recommendation":
                    "ensure connection is over HTTPS"
                })

            case "missing_csp":
                temporary_issue.update({
                    "recommendation":
                    "use caution when interacting with the website"
                })

            case "missing_x_content_type_options":
                temporary_issue.update({
                    "recommendation":
                    "use caution when interacting with the website"
                })

        risk_dictionary["issues"].append(temporary_issue)

    return risk_dictionary