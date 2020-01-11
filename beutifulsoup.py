from urllib.request import urlopen
from bs4 import BeautifulSoup

# specify the url
quote_page = 'http://example.com/'
# query the website and return the html to the variable ‘page’
page = urlopen(quote_page)
# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, "html.parser")

print(soup)