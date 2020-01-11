from urllib.request import urlopen, URLopener, urlretrieve
from shutil import copyfileobj
# url = "http://www.ynet.co.il"
url = "https://friends.walla.co.il/login"

# testfile = URLopener()
# testfile.retrieve(url, "site.html")

html = urlopen(url)


with open("temp.txt","w+b") as htmlfile:
    copyfileobj(html.fp,htmlfile)



# html = urlretrieve(url, copy_path + "temp.html")


