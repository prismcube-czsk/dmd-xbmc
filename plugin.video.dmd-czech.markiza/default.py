# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://video.markiza.sk'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.markiza')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.markiza')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

def OBSAH():
    addDir('Archív TV Markiza',__baseurl__+'/archiv-tv-markiza',1,icon)
    addDir('Archív Doma','http://doma.markiza.sk/archiv-doma',2,icon)
    addDir('FUN TV',__baseurl__+'/fun-tv',3,icon)    

    
def CAT_M(url):
    #self.core.setSorting('NONE')
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<div class="image"><a href="(.+?)"><img src="(.+?)" width="152" height="85" title="(.+?)"></a></div>').findall(httpdata)
    for link,thumb,name in match:
        if re.search('superstar', link, re.U):
            addDir(name,__baseurl__+link,5,thumb)
            continue
        addDir(name,__baseurl__+link,4,thumb)

def CAT_D(url):
    #self.core.setSorting('NONE')
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<div class="image"><a href="(.+?)"><img src="(.+?)" width="152" height="85" title="(.+?)"></a></div>').findall(httpdata)
    for link,thumb,name in match:
        addDir(name,'http://doma.markiza.sk'+link,4,thumb)


def CAT_F(url):
    doc = read_page(url)
    items = doc.find('div', id='VagonFunContent')
    for item in items.findAll('div', 'item'):
        name_a = item.find('div','text')
        name_a = name_a.find('a')
        name_a = name_a.getText(" ").encode('utf-8')
        link = str(item.a['href']) 
        thumb = str(item.img['src'])  
        addDir(name_a,__baseurl__+link,4,thumb)


def LIST_MDF(url):
    doc = read_page(url)
    items = doc.find('div', id='VagonContent')
    for item in items.findAll('div', 'item'):
        name_a = item.find('div','title')
        name_a = name_a.find('a')
        name_a = name_a.getText(" ").encode('utf-8')
        name = item.find('span')
        name = name.getText(" ").encode('utf-8')
        url = str(item.a['href']) 
        id_video = re.compile('/([0-9]+)$').findall(url)
        url = 'http://www.markiza.sk/xml/video/parts.rss?ID_entity='+id_video[0]
        thumb = str(item.img['src'])  
        title = name_a + ' ' + name 
        addDir(title,url,10,thumb)
    try:
        pager = doc.find('div', 'right')
        next_item = pager.find('a')
        dalsi = next_item.text.encode('utf-8') 
        if re.match('staršie', dalsi, re.U):
            next_url = next_item['href']
            #print next_url
            addDir('Další strana',next_url,4,nexticon)
    except:
        print 'STRANKOVANI NENALEZENO'

def SUPERSTAR(url):
    doc = read_page(url)
    items = doc.find('div', 'entry-content')
    for item in items.findAll('li', 'item_'):
        name_a = item.find('h3')
        name_a = name_a.find('a')
        name_a = name_a.getText(" ").encode('utf-8')
        name = item.find('div','date')
        name = name.getText(" ").encode('utf-8')
        url = str(item.a['href']) 
        id_video = re.compile('/([0-9]+)$').findall(url)
        url = 'http://www.markiza.sk/xml/video/parts.rss?ID_entity='+id_video[0]
        thumb = str(item.img['src'])  
        title = name_a + ' ' + name 
        #print title,url,thumb
        addDir(title,url,10,thumb)
    try:
        pager = doc.find('div', 'more_video')
        next_item = pager.find('a')
        dalsi = next_item.text.encode('utf-8') 
        if re.match('ďalšie', dalsi, re.U):
            next_url = next_item['href']
            #print next_url
            addDir('Další strana',next_url,4,nexticon)
    except:
        print 'STRANKOVANI NENALEZENO'
               
def VIDEOLINK(url,name):
    doc = read_page(url)
    title_main = doc.find('title')
    title_main = title_main.getText(" ").encode('utf-8')
    items = doc.find('channel')
    for item in items.findAll('item'):
        title = item.find('title')
        title = title.getText(" ").encode('utf-8')
        #url = re.compile('player url="(.+?)"').findall(str(item))
        #thumb = re.compile('thumbnail url="(.+?)"').findall(str(item))
        url = item.find('media:player')
        url = url['url']
        thumb = item.find('media:thumbnail')
        thumb = thumb['url']
        title = title + ' ' + title_main
        #print title+title_main, url[0],thumb[0]
        addLink(title,url,thumb,name)
        #addLink(title,url[0],thumb[0],name)



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
       
elif mode==1:
        print ""+url
        CAT_M(url)

elif mode==2:
        print ""+url
        CAT_D(url)

elif mode==3:
        print ""+url
        CAT_F(url)

elif mode==4:
        print ""+url
        LIST_MDF(url)

elif mode==5:
        print ""+url
        SUPERSTAR(url)
        
elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
