import datetime
import risk_engine

test_risks = ["missing_csp", "no_https", "missing_hsts"]

def recommendations(issues_list):
    issue_count = 0
    for issue in issues_list:
        print("Issue " + str(issue_count) + ": " + issue)
        match issue:
            case "no_https":
                print("recommendation: get a TLS certificate and serve the site over HTTPS.")
            case "missing_csp":
                print("recommendation: add a Content-Security-Policy header to limit where scripts can load from.")
            case "missing_hsts":
                print("recommendation: add a Strict-Transport-Security (HSTS) header so browsers always use HTTPS.")
            case "no_https_redirect":
                print("Website lacks HTTPS redirect")
            case "missing_x_content_type_options":
                print("recommendation: add 'X-Content-Type-Options: nosniff' to stop browsers guessing file types.")
        print("\n")
        issue_count += 1

print("-----------------------------------")
print("Website Security Report")
print("-----------------------------------\n")

print("date: " + str(datetime.datetime.now()))
print("website: ")
print("score: " + str(risk_engine.scoring_system(test_risks)) + "/100")
print("risk level: ")
print("\n")

print("issues found: " + str(len(test_risks)))
print("\n")

recommendations(test_risks)
print("-----------------------------------")