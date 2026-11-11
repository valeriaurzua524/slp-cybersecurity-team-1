# Website security scanner
# Original component: Heaven Neumann
# Integration/compatibility updates: Valeria

import requests
from urllib.parse import urlparse


def website_scanner(website):
    """
    Scans a website for basic security indicators.

    Checks:
    - HTTPS support
    - HTTP -> HTTPS redirect
    - Content-Security-Policy
    - Strict-Transport-Security
    - X-Content-Type-Options
    - X-Frame-Options
    - Referrer-Policy
    - Permissions-Policy

    Returns a dictionary containing scan results.
    """

    # -------------------------------------------------
    # Normalize URL
    # -------------------------------------------------
    website = website.strip()

    if not website.startswith(("http://", "https://")):
        website = "http://" + website

    parsed_url = urlparse(website)

    hostname = parsed_url.netloc

    if not hostname:
        return {
            "website": website,
            "error": "invalid_url",
            "message": "Please enter a valid website URL.",
            "issues": [],
        }

    # Create HTTP and HTTPS versions of the website
    http_url = f"http://{hostname}"
    https_url = f"https://{hostname}"

    issues = []

    uses_https = False
    redirects_to_https = False

    final_url = website
    status_code = None
    response = None

    # -------------------------------------------------
    # Check HTTPS support
    # -------------------------------------------------
    try:

        https_response = requests.get(
            https_url,
            timeout=10,
            allow_redirects=True
        )

        final_https_url = https_response.url

        if final_https_url.startswith("https://"):
            uses_https = True
            response = https_response
            final_url = final_https_url
            status_code = https_response.status_code

    except requests.RequestException:
        uses_https = False

    if not uses_https:
        issues.append("no_https")

    # -------------------------------------------------
    # Check HTTP -> HTTPS redirect
    # -------------------------------------------------
    try:

        http_response = requests.get(
            http_url,
            timeout=10,
            allow_redirects=True
        )

        if http_response.url.startswith("https://"):
            redirects_to_https = True

        # If HTTPS scan failed, use HTTP response
        # so headers/status can still be inspected
        if response is None:
            response = http_response
            final_url = http_response.url
            status_code = http_response.status_code

    except requests.RequestException:
        pass

    if not redirects_to_https:
        issues.append("no_https_redirect")

    # -------------------------------------------------
    # If no response could be obtained
    # -------------------------------------------------
    if response is None:

        return {
            "website": website,
            "error": "connection_error",
            "message": "The website could not be reached. Please check the URL and try again.",
            "issues": [],
        }

    # -------------------------------------------------
    # Security header checks
    # -------------------------------------------------
    headers = response.headers

    # Content-Security-Policy
    if not headers.get("Content-Security-Policy"):
        issues.append("missing_csp")

    # Strict-Transport-Security
    if not headers.get("Strict-Transport-Security"):
        issues.append("missing_hsts")

    # X-Content-Type-Options
    if not headers.get("X-Content-Type-Options"):
        issues.append("missing_x_content_type_options")

    # X-Frame-Options
    if not headers.get("X-Frame-Options"):
        issues.append("missing_x_frame_options")

    # Referrer-Policy
    if not headers.get("Referrer-Policy"):
        issues.append("missing_referrer_policy")

    # Permissions-Policy
    if not headers.get("Permissions-Policy"):
        issues.append("missing_permissions_policy")

    # -------------------------------------------------
    # Return scan results
    # -------------------------------------------------
    return {
        "website": website,
        "final_url": final_url,
        "status_code": status_code,
        "uses_https": uses_https,
        "redirects_to_https": redirects_to_https,
        "issues": issues,
    }


def main():
    """
    Used only for testing this file by itself.
    """

    website = input("Enter a website URL: ")

    results = website_scanner(website)

    print("\nWEBSITE SECURITY SCAN")
    print("---------------------")

    if "error" in results:

        print("Scan failed.")
        print(results.get("message"))

    else:

        print(f"Website: {results['website']}")
        print(f"Final URL: {results['final_url']}")
        print(f"Status Code: {results['status_code']}")
        print(f"HTTPS Supported: {results['uses_https']}")
        print(
            f"HTTP -> HTTPS Redirect: "
            f"{results['redirects_to_https']}"
        )

        print("\nIssues:")

        if not results["issues"]:
            print("No issues found.")

        else:
            for issue in results["issues"]:
                print(f"- {issue}")


if __name__ == "__main__":
    main()