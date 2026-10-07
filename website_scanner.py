import requests

url = ""
while url != "q":
    url = input("Please enter the URL you want to check: ")
    try:
        responce = requests.get(url)
        if responce.status_code == 200:
            print(f"{url} uses https")
        else:
            print(f"{url} not working")
    except Exception as e:
        print(f"{e}")

#Test cases
#https://google.com
#https://example.com
#https://yahoo.com
#https://bing.com