'''
Created on Mar 25, 2010

@author: ivan
'''

import re,urllib2,urllib, types
from bs4 import BeautifulSoup, BeautifulStoneSoup

HTML="html"
XML="xml"
AGENT='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def read_page(url, type=HTML, data=None):
    if isinstance(url, types.StringTypes):
        req = urllib2.Request(url)
        req.add_header('User-Agent', AGENT)
        if data:
            encoded_data=urllib.urlencode(data) 
        else:
            encoded_data=None
        response = urllib2.urlopen(req, encoded_data)
    elif hasattr(url, 'read') and hasattr(url, 'close'):
        response=url
    else:
        raise ValueError('Invalid url object')
    html_source=response.read()
    response.close()
    def parse():
        if type==HTML:
            doc=BeautifulSoup(html_source, "html5lib")
        elif type==XML:
            #probably not used...also not tested
            doc=BeautifulSoup(html_source, "xml")
        return doc
    try:
        return parse()
    except TypeError, e:
        #might have problem with encoding, try UTF-8 with error tolerance
        html_source=unicode(html_source, 'UTF-8', 'ignore')
        return parse()

RE_NUMBER_VAR=r'var (%s)\s*=\s*(\d+)\s*;'
RE_STR_VAR=r'var (%s)\s*=\s*["\'](.+?)["\']\s*;'
VAR_TYPE_INT='I'
VAR_TYPE_STR='S'
def var_re(name, type):
    if type==VAR_TYPE_INT:
        exp=RE_NUMBER_VAR
    elif type==VAR_TYPE_STR:
        exp=RE_STR_VAR
    else:
        raise ValueError("Invalid var type")
    return re.compile(exp % name)


def parse_vars(doc, vars_re):
    out={}
    txt=doc.find(text=vars_re[0])
    for var_re in vars_re:
        m=var_re.search(txt)
        if not m:
            raise RuntimeError("Required var is missing for re %s" %str(var_re))
        out[m.group(1)]=m.group(2)
        
    return out

class BaseScraper(object):
    def __init__(self, url, page=None, data=None):
        self.url=url
        self.doc=read_page(url, HTML, data)
        self.page=page
        self.items=iter(self.get_items()) 
    def get_items(self):
        raise NotImplemented()    
    def __iter__(self):
        return self   
    def next(self):
        raise NotImplemented()    
    def next_page(self):
        return None
    