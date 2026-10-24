import requests
from requests.exceptions import MissingSchema, InvalidSchema, InvalidURL, RequestException


# Website scanner
# Original component: Heaven
# Integration/compatibility updates: Valeria


def website_scanner(url):

    issues = []

    try:
        # add http:// if the user does not include a scheme
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        # get the hostname so we can test both HTTP and HTTPS
        hostname = url.replace("http://", "").replace("https://", "").split("/")[0]

        http_url = "http://" + hostname
        https_url = "https://" + hostname

        # -----------------------------------
        # check whether HTTPS works
        # -----------------------------------

        try:
            https_res = requests.get(
                https_url,
                allow_redirects=True,
                timeout=5
            )

            uses_https = https_res.url.startswith("https://")

        except RequestException:
            https_res = None
            uses_https = False

        if not uses_https:
            issues.append("no_https")

        # -----------------------------------
        # check HTTP -> HTTPS redirect
        # -----------------------------------

        try:
            http_res = requests.get(
                http_url,
                allow_redirects=True,
                timeout=5
            )

            redirects_to_https = http_res.url.startswith("https://")

        except RequestException:
            redirects_to_https = False

        if not redirects_to_https:
            issues.append("no_https_redirect")

        # -----------------------------------
        # check security headers
        # -----------------------------------

        # use the HTTPS response when available
        if https_res is not None:
            res = https_res
        else:
            res = requests.get(
                url,
                allow_redirects=True,
                timeout=5
            )

        csp = res.headers.get("Content-Security-Policy")
        hsts = res.headers.get("Strict-Transport-Security")
        xcto = res.headers.get("X-Content-Type-Options")

        if csp is None:
            issues.append("missing_csp")

        if hsts is None:
            issues.append("missing_hsts")

        if xcto is None:
            issues.append("missing_x_content_type_options")

        # return structured results for integration
        return {
            "website": url,
            "final_url": res.url,
            "status_code": res.status_code,
            "uses_https": uses_https,
            "redirects_to_https": redirects_to_https,
            "issues": issues,
        }

    except (MissingSchema, InvalidSchema, InvalidURL) as e:
        return {
            "website": url,
            "error": "Invalid URL",
            "message": str(e),
            "issues": [],
        }

    except RequestException as e:
        return {
            "website": url,
            "error": "Website scan failed",
            "message": str(e),
            "issues": [],
        }


def main():
    # main function for testing
    while True:

        url = input("\nPlease enter the url you wish to scan: ")

        print()
        print(website_scanner(url))
        print()

        print("Enter another url?")
        another = input("\tyes(y) or no(n): ")

        if another == "y":
            continue
        else:
            break


if __name__ == "__main__":
    main()