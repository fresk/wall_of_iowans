import json
import requests
import hashlib
import os.path
import os
import unicodedata


import HTMLParser
_htmlparser = HTMLParser.HTMLParser()
unescape_html = _htmlparser.unescape

def clean_text(text):
    if type(text) == bool:
        return ""

    text = text.encode('ascii','ignore')
    text = unescape_html(text)
    text = text.replace("<br/>", "\n\n")
    text = text.replace("<br />", "\n\n")
    text = text.replace("\r", "")
    text = text.replace("\\r", "\n")
    text = text.replace("\\n", "\n")
    text = text.replace("<p>", "\n")
    text = text.replace("</p>", "\n")
    
    return text



def parse_number(s):
    numbers = [int(s) for s in str.split(" ") if s.isdigit()]
    if len(numbers) == 1: 
        return [int(s) for s in str.split(" ") if s.isdigit()][0]
    else:
        return 0
    



def save_image(image_data, group):
    if not (image_data and image_data.get('url')):
        return {'file': 'img/anon.jpg', 'image_id': 'anon'}

    url = image_data['url']

    fileid = group +"-"+ hashlib.md5(url).hexdigest()
    fname = './cache/original/' + fileid + "."+url.split(".")[-1]
    
    if not os.path.exists(fname):
        print "fetching:", url
        req = requests.get(url)
        with open(fname, 'wb') as fout:
            fout.write(req.content)
    else:
        print 'using cached file:'
        print '   ', url
        print '   ', fname

    image_data['file'] = fname
    image_data['image_id'] = fileid

    return image_data #"atlas://data/atlas/"+fileid






iowans = json.load(open('_iowans.json', 'r'))

for p in iowans:

    p['image'] = save_image(p['image'], 'primary')
    p['locationimg'] = save_image(p['locationimg'], 'location')
    p['image_alt'] = save_image(p['image_alt'], 'alt')
    p['artifactimg'] = save_image(p['artifactimg'], 'artifact')


    p['image_source'] = "atlas://data/cache/512atlas/"+p['image']['image_id']
    p['locationimg_source'] = "atlas://data/cache/512atlas/"+p['locationimg']['image_id']
    p['image_alt_source'] = "atlas://data/cache/512atlas/"+p['image_alt']['image_id']
    p['artifactimg_source'] = "atlas://data/cache/512atlas/"+p['artifactimg']['image_id']

    p['bio'] = clean_text(p['bio'])
    

    
    p['yearofdeath'] = clean_text(p['yearofdeath'])
    p['yearofbirth'] = clean_text(p['yearofbirth'])

    p['birth_to_death'] =  str(p['yearofbirth']) + " - " + str(p['yearofdeath'])


    try:
        p['yearofdeath'] = int(p['yearofdeath'])
    except:
        p['yearofdeath'] = 9999

    try:
        p['yearofbirth'] = int(p['yearofbirth'])
    except:
        p['yearofbirth'] = -9999



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





