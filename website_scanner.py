import requests
from requests.exceptions import MissingSchema, InvalidSchema, InvalidURL, RequestException

def website_scanner(url):
    #Initialize lists
    results = []
    issues = []
    try:
        res = requests.get(url, allow_redirects= False, timeout= 5)

        #checks for security headers
        csp = res.headers.get("Content-Security-Policy")
        csp_ro = res.headers.get("Content-Security-Policy-Report-Only")
        hsts = res.headers.get("Strict-Transport-Security")
        xcto = res.headers.get("X-Content-Type-Options")

        #check if url uses http
        if res.url.startswith("http://"):
            print(f"This url '{url}' uses http")

            res = requests.get(url, allow_redirects= True)
            #checks if url redirects to https
            if res.status_code in (301, 302) and "https" in res.headers.get("Location", ""):
                print(f"This url '{url}' redirects to https")
            else:
                print(f"This url '{url}' does not redirect from http")
        else:
            #check is url uses https
            print(f"This url '{url}' uses https")

        if csp is None:
            issues.append("missing_csp")
        if csp_ro is None:
            issues.append("missing_csp_report-only")
        if hsts is None:
            issues.append("missing_hsts")
        if xcto is None:
            issues.append("missing_xcto")
        
        results.append(url)
        results.append(issues)
        
    except MissingSchema as e:
        print(f"{e}")
        new_url = input("Please re-enter url: ")
        website_scanner(new_url)
    except InvalidSchema as e:
        print(f"{e}")
        new_url = input("Please re-enter url: ")
        website_scanner(new_url)
    except InvalidURL as e:
        print(f"{e}")
        new_url = input("Please re-enter url: ")
        website_scanner(new_url)
    except RequestException as e:
        print(f"{e}")
        new_url = input("Please re-enter url: ")
        website_scanner(new_url)

    #returns results lis with the url at index 0 and issues list at index 1    
    return results

def main():
    #main function for testing
    while True:
        url = input("\nPlease enter the url you wish to scan: ")
        print()
        print(website_scanner(url))
        print()

        print("Enter another url?")
        another = input("\tyes(y) or no(n): ")
        if another == 'y':
            continue
        else:
            break


main()
    

'''
Test cases
amazon.com – redirects http://amazon.com to https://amazon.com

apple.com – enforces HTTPS and redirects HTTP traffic

facebook.com – HTTP version redirects to HTTPS

google.com – HTTP requests are redirected to HTTPS

instagram.com – HTTP to HTTPS redirect in place

linkedin.com – HTTP redirect to HTTPS

netflix.com – HTTP to HTTPS redirect

paypal.com – HTTP redirect to HTTPS

reddit.com – HTTP to HTTPS redirect

twitter.com – HTTP redirect to HTTPS

wikipedia.org – HTTP to HTTPS redirect

yahoo.com – HTTP redirect to HTTPS

http://www.socialstudieshelp.com/

http://www.grose.us

http://www.southcn.com/

http://www.china.com.cn/

http://dedecms.com/

http://www.faqs.org/faqs/

http://www.360doc.com/index.html

http://icio.us/

http://soso.com/

http://people.com.cn/

Examples from Davey Barfoot’s “List of HTTP Websites” 
daveybarfoot.wordpress.com
daveybarfoot.wordpress.com
This blog maintains a curated list of “decent” HTTP‑only sites:

http://info.cern.ch

http://www.friendsbricks.com

http://thebrickblogger.com

http://slither.io

http://ftp.mozilla.org

http://feeds.feedburner.com

http://www.aiohq.com

http://www.dantan.net

http://www.scottbarfoot.com

http://nginx.org

http://www.rfreitas.com
'''