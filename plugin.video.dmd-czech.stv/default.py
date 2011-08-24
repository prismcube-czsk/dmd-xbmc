# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
from urlparse import urlparse
import xbmcplugin,xbmcgui,xbmcaddon
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.stv')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.stv')
__baseurl__ = 'http://www.stv.sk'
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

def OBSAH():
    doc = read_page(__baseurl__+'/online/archiv/')
    doc = doc.find('select', id='sel3')
    match = re.compile('<option value="(.+?)">(.+?)</option>').findall(str(doc))
    for link,name in match:
            print name,link
            addDir(name,__baseurl__+link,2,icon)    


def OBSAH_RELACE(url):
    doc = read_page(url)
    doc = doc.find('table')
    doc2 = doc.find('tbody')
    cast_url = urlparse(url)
    next = 1
    predchozi = re.compile('<a href="(.+?)" class="prew">.+?</a></th><th class="month" colspan="5">(.+?)</th><th class="arr"><a href="(.+?)" class="prew">.+?</a></th>').findall(str(doc))
    for starsical, nazevcal, dalsical in predchozi:
        continue
    if len(predchozi) < 1:
        predchozi = re.compile('<a href="(.+?)" class="prew">.+?</a></th><th class="month" colspan="5">(.+?)</th><th class="arr no-next">.+?</th>').findall(str(doc))
        next = 0
        for starsical, nazevcal in predchozi:
            continue
    porady = re.compile('<a href="(.+?)" class=".+?">(.+?)</a>').findall(str(doc2))    
    if len(porady) < 1:
        porady = re.compile('<a href="(.+?)" class=".+?" title=".+?">(.+?)</a>').findall(str(doc2))      
    print '<< Starší','http://' + cast_url[1] + cast_url[2] + starsical
    addDir('<< Starší','http://' + cast_url[1] + cast_url[2] + starsical,2,nexticon)   
    for poradlink, poradden in porady:
        poradlink = re.sub('&amp;','&',poradlink)
        poradden = poradden +' '+ nazevcal
        print poradlink,poradden
        addDir(poradden,'http://' + cast_url[1] + cast_url[2] + poradlink,10,icon)   
    if next == 1:
        print '>> Novější' ,'http://' + cast_url[1] + cast_url[2] + dalsical
        addDir('>> Novější','http://' + cast_url[1] + cast_url[2] + dalsical,2,nexticon)   
                
def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    playlist = re.compile('playlistfile=(.+?)&autostart').findall(httpdata)
    title = re.compile('<title>(.+?)</title>').findall(httpdata)
    streamxml = re.sub('%26','&',playlist[0])  
    req = urllib2.Request(streamxml)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    doc = response.read()
    response.close()
    location = re.compile('<location>(.+?)</location>').findall(str(doc))
    streamer = re.compile('<meta rel="streamer">(.+?)</meta>').findall(str(doc))
    print location[0], streamer[0]
    cesta = 'mp4:'+location[0]
    server = streamer[0]   
    title = title[0] + ' ' + name
    swfurl = 'http://www.stv.sk/online/player/player-licensed-sh.swf'
    rtmp_url = server+' playpath='+cesta+' pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true'  
    print rtmp_url
    addLink(title,rtmp_url,icon,name)



def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addLink(name,url,iconimage,popis):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": popis} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
params=get_params()
url=None
name=None
thumb=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        OBSAH()
       
elif mode==2:
        print ""+url
        OBSAH_RELACE(url)

      
elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
