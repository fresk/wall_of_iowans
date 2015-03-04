import json
import requests
import hashlib
import os.path

import HTMLParser
_htmlparser = HTMLParser.HTMLParser()
unescape_html = _htmlparser.unescape

def clean_text(text):
    if not isinstance(text, basestring):
        return text
    text = unescape_html(text)
    text = text.replace("<br/>", "\n\n")
    text = text.replace("<br />", "\n\n")
    text = text.replace("\r", "")
    text = text.replace("\\r", "\n")
    text = text.replace("\\n", "\n")
    text = text.replace("<p>", "\n")
    text = text.replace("</p>", "\n")
    
    return text

def save_image(url):
    fname = "cache/"+hashlib.md5(url).hexdigest()+".jpg"
    if not os.path.isfile(fname):
        print "fetching:", url
        req = requests.get(url)
        with open(fname, 'wb') as fout:
            fout.write(req.content)
    return "data/"+fname





iowans = json.load(open('_iowans.json', 'r'))

for p in iowans:
    print p['title']

    if p['image']:
        p['image']['file'] =  save_image(p['image']['url']) 

    if p['locationimg']:
        p['locationimg']['file'] = save_image(p['locationimg']['url'])

    if p['artifactimg']:
        p['artifactimg']['file'] = save_image(p['artifactimg']['url'])

    if p['image_alt']:
        p['image_alt']['file'] = save_image(p['image_alt']['url'])

    p['bio'] = clean_text(p['bio'])
    p['overview'] = clean_text(p['overview'])
    p['artifactshort'] = clean_text(p['artifactshort'])
    p['artifactlong'] = clean_text(p['artifactlong'])
    p['locationshort'] = clean_text(p['locationlong'])

    p['locationgeo'] = p['locationgeo'] or "0,0"
    if not ',' in p['locationgeo']:
        p['locationgeo'] = p['locationgeo'].replace('\t', ',')
    if not ',' in p['locationgeo']:
        p['locationgeo'] = p['locationgeo'].replace(' ', ',')
    p['locationgeo'] = map(float, p['locationgeo'].split(','))



json.dump(iowans, open('iowans.json', 'w'), indent=4)





