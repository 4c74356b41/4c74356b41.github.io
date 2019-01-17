import datetime
import requests
import argparse
from jinja2 import Template
from lxml import html

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--title", type=str)
parser.add_argument("-s", "--tags", type=lambda s: [str(item) for item in s.split(',')])
args = parser.parse_args()

datestr = datetime.date.today()
page = requests.get('http://4c74356b41.com')
webpage = html.fromstring(page.content)
post = webpage.xpath('//a/@href')[4].replace('/post','')

with open('new_post.j2') as file_:
    template = Template(file_.read())
x = template.render(id=(1 + int(post)), title=args.title, tags=args.tags, date=datestr)
with open('_posts/{}-{}.md'.format(
          datestr,
          args.title.replace(' ', '_').lower()
), 'w') as file_:
    print(x, file=file_, end='')
