from bs4 import BeautifulSoup
import pprint
import sys
import urllib2

pp = pprint.PrettyPrinter(indent=4)

if len(sys.argv) < 2:
    print("Usage: python store-catalog.py <username>")
    sys.exit()

username = sys.argv[1]

response = urllib2.urlopen("https://www.redbubble.com/people/%s/shop" % (username))
page_source = response.read()

links = dict()

soup = BeautifulSoup(page_source, "html.parser")

for link in soup.find_all(class_="grid-item"):
    img = link.find(class_="thumbnail")
    price = link.find(class_="d").text+link.find(class_="c").text 
    links[link['id']] = {
        'id': link['id'],
        'title': link['title'],
        'link': 'https://www.redbubble.com'+link['href'],
        'image_link': img['src'],
        'condition': 'new',
        'availability': 'in stock',
        'price': price+' USD',
    }

headers = [
    'id', 'title', 'description', 'link', 'image_link', 'condition', 'availability', 'price'
    ]

print(','.join(headers))

for item in links:
    response = urllib2.urlopen(links[item]['link'])
    page_source = response.read()
    soup = BeautifulSoup(page_source, "html.parser")
    description = soup.find(class_="description_content").text
    links[item]['description'] = description.rstrip('\n').lstrip('\n')
    print("%s,\"%s\",\"%s\",%s,%s,%s,%s,%s" % (
        links[item]['id'],
        links[item]['title'].replace('"', '""'),
        links[item]['description'].replace('"', '""'),
        links[item]['link'],
        links[item]['image_link'],
        links[item]['condition'],
        links[item]['availability'],
        links[item]['price']
        ))