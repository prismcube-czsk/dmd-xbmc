# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videozer.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Modify: 2011-08-15, by Ivo Brhel
#
#------------------------------------------------------------

import re, urlparse, urllib, urllib2
import os


_VALID_URL = r'^((?:http://)?(?:\w+\.)?videozer\.com/(?:(?:e/|embed/|video/)|(?:(?:flash/|f/)))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
_UserAgent_ =  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'



def getURL(url):
	
    #logger.info("[videozer.py] url="+url)
    # El formato de la URL de la página es
    # http://videozer.com/video/Tnfs1OI
    # El formato de la URL del vídeo es
    # http://video33.videozer.com:80/video?v=Tnfs1OI&t=1303649554&u=&c=c6bffc4fa689297273cf2a04658ca435&r=1
    code = Extract_id(url)
    
    controluri = "http://www.videozer.com/player_control/settings.php?v=%s&em=TRUE&fv=v1.1.12" %code
    #
    req = urllib2.Request(controluri)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    datajson=response.read()
    response.close()
    #
    #datajson = scrapertools.cachePage(controluri)
    datajson = datajson.replace("false","False").replace("true","True")
    datajson = datajson.replace("null","None")
    datadict = eval("("+datajson+")")
    formatos = datadict["cfg"]["quality"]
    longitud = len(formatos)
    uri = formatos[longitud-1]["u"]
    import base64
    
    devuelve = base64.decodestring(uri)
    return devuelve

def Extract_id(url):
    # Extract video id from URL
    mobj = re.match(_VALID_URL, url)
    if mobj is None:
        print 'ERROR: invalid URL: %s' % url
        
        return ""
    id = mobj.group(2)
    return id
