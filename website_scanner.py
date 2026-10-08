import requests

url = ""
while url != "q":
    url = input("Please enter the URL you want to check: ")
    try:
        res = requests.get(url)

        csp = res.headers.get("Content-Security-Policy")
        csp_ro = res.headers.get("Content-Security-Policy-Report-Only")
        hsts = res.headers.get("Strict-Transport-Security")
        xcto = res.headers.get("X-Content-Type-Options")

        if res.status_code == 200:
            print(f"This url '{url}' uses https")
        else:
            res =  requests.get(url, allow_redirects = True)

            if res.url.startswith("https://"):
                print(f"This url '{url}' redirects to https")
            else:
                print(f"This url '{url}' not working")

        print("CSP: ", csp)
        print("CSP Report-Only:", csp_ro)
        print("HSTS: ", hsts)
        print("X-Content-Type-Options: ", xcto)
        print()
        
    except Exception as e:
        print(f"{e}")

#Test cases
#https://google.com
#https://example.com
#https://yahoo.com
#https://bing.com