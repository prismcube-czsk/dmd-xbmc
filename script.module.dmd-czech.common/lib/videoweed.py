# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videoweed
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Modify: 2011-07-31, by Ivo Brhel
#
#------------------------------------------------------------

import re, urlparse, urllib, urllib2
import os

_UserAgent_ =  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'

# Obtiene la URL que hay detrás de un enlace a linkbucks
def getURL(url):

    # Descarga la página de linkbucks
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    data = response.read()
    #data = scrapertools.cachePage(url)
    # Extrae la URL real
    patronvideos  = 'flashvars.file="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)A
    print matches
    devuelve = "";
    if len(matches)>0:
    	devuelve = matches[0]
    return devuelve
