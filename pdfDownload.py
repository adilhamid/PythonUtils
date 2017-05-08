from bs4 import BeautifulSoup
from tqdm import tqdm
import urllib2
import requests
import os.path

# Sources
# http://stackoverflow.com/questions/24844729/download-pdf-using-urllib

def getFileFromUrl(site, file_type):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    req = urllib2.Request(site, headers=hdr)

    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print e.fp.read()

    content = page.read()
    soup = BeautifulSoup(content, "html.parser")
    links = soup.findAll('a')
    for link in links:
        hrflinks = link.get('href')
        if hrflinks.endswith(file_type):
            if hrflinks.startswith("/"):
                hrflinks = site + hrflinks[1:]
            elif hrflinks.startswith("./"):
                hrflinks = site + hrflinks[2:]

            print hrflinks
            download_file(hrflinks)


def download_file(link):
    file_name = link.split('/')[-1]
    if not os.path.exists(file_name):
        a = requests.get(link, stream=True)
        total_size = int(a.headers.get('content-length', 0))
        with open(file_name, 'wb') as f:
            for block in tqdm(a.iter_content(512), total=total_size, unit='B', desc="Downloading "+ file_name):
                if not block:
                    break
                f.write(block)
    print

if __name__ == "__main__":
    site= "http://www.nseindia.com/"
    file_type= ".pdf"
    getFileFromUrl(site, file_type)
