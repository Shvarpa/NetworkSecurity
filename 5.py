from bs4 import BeautifulSoup
from requests import Session,get
import os
import re
from time import sleep

class Cloner:

    def __init__(self,site,basePath):
        self.basePath = basePath
        self.site = site
        self.baseSite = re.match("(https?://)?([^/]*)",site)[0] + "/"
        self.session = Session()

    def clone(self):
        html = self.download(self.site)
        self.linkGenerator(html)

    """
    return file's data made from url
    """
    def download(self, url):
        return self.session.get(url).content

    """
    create file from data and type of url in path
    """
    def save(self, data, path):
        if not path.startswith('/'):
            path = '/' + path
        path = os.path.relpath(self.basePath + path)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname) and dirname!="":
            os.makedirs(dirname)

        with open(path, "wb") as file:
            file.write(data)       

    """
    generate a path from url
    """
    def pathGenerator(self, url):
        path = re.match("(https?://)?([^?]*)([?].*)?",url)[2]
        return path
    
    """
    generate links from site, and make copies of them in local dir
    """
    def linkGenerator(self,html):
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("link")
        for link in links:
            url = link['href']
            dest = self.pathGenerator(url)

            if not url.startswith("http"):
                base = True
                url = self.baseSite + url
            else:
                base = False
            data = self.download(url)

            print(f'link:{link}\n dest={dest}')
            self.save(data,dest)
            link["href"] = dest if not base else "/"+dest

        scripts = soup.find_all("script")
        for script in scripts:
            if not script.get("src",None): 
                continue
            url = script['src']
            dest = self.pathGenerator(url)

            if not url.startswith("http"):
                base = True
                url = self.baseSite + url
            else:
                base = False
            data = self.download(url)
            print(f'script:{script}\n dest={dest}')
            self.save(data,dest)
            script["src"] = dest if not base else "/"+dest
        
        with open(self.basePath + "/index.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
    
# def main():
#     site = "https://store.steampowered.com/login/"
#     cloner = Cloner(site,"steam")
#     cloner.clone()

def main():
    # site = "https://friends.walla.co.il/login/"
    site = "https://store.steampowered.com/login/"
    cloner = Cloner(site,"steam")
    cloner.clone()

if __name__=="__main__":
    main()
