# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
from stats import *
from urlparse import urlparse
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__='http://jaknato.centrum.cz'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.jaknato')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.jaknato')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

def OBSAH():
    #self.core.setSorting('NONE')
    req = urllib2.Request(__baseurl__)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<li class=".+?"><a href="(.+?)">(.+?)</a></li>').findall(httpdata)
    for url,name in match:
        addDir(name,__baseurl__+url,1,icon)    

            
def INDEX(url):
    doc = read_page(url)
    items = doc.find('div', id='main')
    for item in items.findAll('div','item'):
        name = item.find('h3')
        name = name.find('a')
        name = name.getText(" ").encode('utf-8')
        link = __baseurl__+str(item.a['href']) 
        thumb = str(item.img['src'])  
        #print name,thumb,link
        playlist = link+'playlist/'
        playdoc = read_page(playlist)
        cesta = playdoc.find('path')
        cesta = cesta.getText(" ").encode('utf-8')
        popis = playdoc.find('description')
        popis = popis.getText(" ").encode('utf-8')
        #print name,popis,cesta,thumb
        addLink(name,cesta,thumb,popis)
    try:
        items = doc.find('p', 'pager')
        for item in items.findAll('a'):
            page = item.text.encode('utf-8') 
            if re.match('další', page, re.U):
                next_url = item['href'].replace('.','')
                cast_url = urlparse(url)
                #print 'htttp://'+cast_url[1]+cast_url[2]+next_url
                addDir('= Další strana =','http://'+cast_url[1]+cast_url[2]+next_url,1,nexticon)
    except:
        print 'strankovani nenalezeno'        

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
        STATS("OBSAH", "Function")
        OBSAH()
       
elif mode==1:
        print ""
        STATS(name, "Item")
        INDEX(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
