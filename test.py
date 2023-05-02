from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

def scrape(site):
    # storing all visited urls in a set to prevent duplicates
    visited = set()
    status = 0

    # creating a queue to keep track of urls to scrape
    queue = [site]
    file = open("url.txt", "w")
    while queue:
        current_url = queue.pop(0)
        if current_url in visited:
            continue

        visited.add(current_url)
        file.write(current_url+","+str(status)+"\n")
        file.flush()


        try:
            # making a request to the current url
            r = requests.get(current_url, timeout=5)
            
            status=r.status_code
        except requests.exceptions.RequestException as e:
            # handling exceptions during request
            print(f"Error connecting to {current_url}: {e}")
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            full_url = urljoin(site, href)
            # checking if the url belongs to the same domain
            if site in full_url and full_url not in visited:
                queue.append(full_url)
                print(full_url)
   
       
if __name__ == "__main__":
    site = "https://example.com"
    scrape(site)