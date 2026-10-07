test_risks = ["missing CSP", "no HTTPS", "missing HSTS"]

def recommendations(issues_list):
    for issue in issues_list:
        match issue:
            case "no HTTPS":
                print("Connect with HTTPS")
            case "missing CSP":
                print("Website lacks CSP")
            case "missing HSTS":
                print("Website lacks HSTS")
            case "no HTTPS redirect":
                print("Website lacks HTTPS redirect")
            case "missing X-Content-Type-Options":
                print("Website lacks missing X-Content-Type-Options")

recommendations(test_risks)