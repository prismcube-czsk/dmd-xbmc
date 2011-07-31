# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
from urlparse import urlparse
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__='http://www.fashionstarstv.cz/cz/'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.fashion')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.fashion')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

def OBSAH():
    addDir('News',__baseurl__+'news.html',1,icon)
    addDir('Fashion',__baseurl__+'fashion.html',1,icon)
    addDir('Shopping',__baseurl__+'shopping.html',1,icon)
    addDir('Parties',__baseurl__+'parties.html',1,icon)
    addDir('Beauty',__baseurl__+'beauty.cz',1,icon)
    addDir('Backstage',__baseurl__+'backstage.cz',1,icon)
    addDir('Hollywood',__baseurl__+'hollywood.html',1,icon)
    addDir('Music (F.)Icon',__baseurl__+'music-f-icon.html',1,icon)
    addDir('Agentka Berslevička',__baseurl__+'agentka-berslevicka.html',1,icon)
            
def INDEX(url):
    doc = read_page(url)
    items = doc.find('div', id='page_left')
    for item in items.findAll('div','article'):
        link = str(item.a['href'])
        thumb = str(item.img['src'])
        name = item.find('a')
        name = name.getText(" ").encode('utf-8')
        addDir(name,'http://www.fashionstarstv.cz'+link,3,'http://www.fashionstarstv.cz'+thumb)    
    try:
        items = doc.find('p', 'listing')
        for item in items.findAll('a'):
            page_no = item.getText(" ").encode('utf-8')
            link = item['href']
            link = link[(link.find('javascript:ajax_request(') + len('javascript:ajax_request(') + 1):] 
            link = link[:(link.find(',') - 1)]
            link = re.sub('&amp;','&',link)
            #print page_no,link
            title = '= Strana '+page_no+' ='
            if re.match('>', page_no, re.U):
                continue
            elif re.match('<', page_no, re.U):
                continue
            addDir(title,'http://www.fashionstarstv.cz'+link,2,nexticon)
    except:
        print 'strankovani nenalezeno'        

def INDEX_AJAX(url):
    doc = read_page(url)
    for item in doc.findAll('div','article'):
        link = str(item.a['href'])
        thumb = str(item.img['src'])
        name = item.find('a')
        name = name.getText(" ").encode('utf-8')
        addDir(name,'http://www.fashionstarstv.cz'+link,3,'http://www.fashionstarstv.cz'+thumb)    
    try:
        items = doc.find('p', 'listing')
        for item in items.findAll('a'):
            page_no = item.getText(" ").encode('utf-8')
            link = item['href']
            link = link[(link.find('javascript:ajax_request(') + len('javascript:ajax_request(') + 1):] 
            link = link[:(link.find(',') - 1)]
            link = re.sub('&amp;','&',link)
            #print page_no,link
            title = '= Strana '+page_no+' ='
            if re.match('>', page_no, re.U):
                continue
            elif re.match('<', page_no, re.U):
                continue
            addDir(title,'http://www.fashionstarstv.cz'+link,2,nexticon)
    except:
        print 'strankovani nenalezeno'
        
def VIDEOLINK(url,name):
    doc = read_page(url)
    match = re.compile('config=/userfiles/video/config.txt&amp;flv=(.+?)&amp;startimage=(.+?)"').findall(str(doc))
    for link,thumb in match:
            #print name,link,thumb
            addLink(name,'http://www.fashionstarstv.cz'+link,'http://www.fashionstarstv.cz'+thumb,name)
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
        print ""
        INDEX(url)
elif mode==2:
        print ""
        INDEX_AJAX(url)

elif mode==3:
        print ""
        VIDEOLINK(url,name)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
