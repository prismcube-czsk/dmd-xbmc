# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
from urlparse import urlparse
import xbmcplugin,xbmcgui,xbmcaddon
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.huste')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.huste')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

def OBSAH():
    addDir('Hudba','http://hudba.huste.tv',1,icon)
    addDir('Šport','http://sport.huste.tv',4,icon)
    addDir('Relálie a seriály','http://zabava.huste.tv',2,icon)    
    addDir('Filmy','http://filmy.huste.tv',3,icon)
    addDir('Hlášky','http://hlasky.huste.tv',4,icon)    

def OBSAH_HUDBA(url):
    addDir('= Interpreti podle abecedy =','http://hudba.huste.tv',5,icon)
    PROUZEK(url)

def OBSAH_RELACE(url):
    addDir('= Podle názvu =','http://zabava.huste.tv',6,icon)
    PROUZEK(url)

def OBSAH_FILMY(url):
    addDir('= Filmy podle abecedy =','http://filmy.huste.tv',8,icon)
    PROUZEK(url)
    
def PROUZEK(url):
    doc = read_page(url)
    items = doc.find('div', id='s-secondary')
    for item in items.findAll('li'):
        name = item.a['title'].encode('utf-8')
        url = str(item.a['href']) 
        addDir(name,url,7,icon)

def ABC(url):
    doc = read_page(url)
    items = doc.find('div', 'b-wrap b-list-alphabet')
    match = re.compile('<a href="(.+?)" title="(.+?)">').findall(str(items))
    for link,name in match:
        addDir(name,link,7,icon)

def FILMY_ABC(url):
    doc = read_page(url)
    items = doc.find('div', 'b-wrap b-list-alphabet')
    match = re.compile('<a href="(.+?)" title="(.+?)">').findall(str(items))
    for link,name in match:
        addDir(name,link,9,icon)
        
def NAZEV(url):
    doc = read_page(url)
    items = doc.find('div', 'b-wrap b-list-simple')
    for item in items.findAll('li'):
        name = item.a['title'].encode('utf-8')
        url = str(item.a['href']) 
        addDir(name,url,7,icon)

    
def INDEX(url):
    doc = read_page(url)
    try:
        items = doc.find('ul', 'l c')
        for item in items.findAll('li','i'):
            title = item.a['title'].encode('utf-8')
            interpret = item.find('p')
            interpret = interpret.getText(" ").encode('utf-8')
            url = str(item.a['href']) 
            thumb = str(item.img['src'])   
            #print name+interpret,url,thumb
            name = title+' - '+interpret
            addDir(name,url,10,thumb)
    except:        
        items = doc.find('div', 'b-wrap b-video')
        items = items.find('ul', 'l c')
        for item in items.findAll('li','i'):
            name = item.a['title'].encode('utf-8')
            interpret = item.find('p')
            interpret = interpret.getText(" ").encode('utf-8')
            url = str(item.a['href']) 
            thumb = str(item.img['src'])   
            name = title+' - '+interpret
            #print name+interpret,url,thumb
            addDir(name,url,10,thumb)
    try:
        pager = doc.find('ul', 'j-center m-page')
        act_page_a = pager.find('li', 'active')
        act_page = act_page_a.getText(" ").encode('utf-8')
        for item in pager.findAll('a'):
            page_url = item['href'].encode('utf-8')
            page_no = item.getText(" ").encode('utf-8')
            #print page_url,page_no
            next_label = '= Strana '+act_page+' >> Další '+page_no+' ='
            if int(page_no) < int(act_page):
                continue
            addDir(next_label,page_url,7,nexticon)
            #print next_label,page_url
    except:
        print 'STRÁNKOVÁNÍ NENALEZENO'

def FILMY_INDEX(url):
    doc = read_page(url)
    items = doc.find('div', 'b-wrap b-video')
    items = items.find('ul', 'l c')
    for item in items.findAll('li','i'):
            name = item.a['title'].encode('utf-8')
            interpret = item.find('p')
            interpret = interpret.getText(" ").encode('utf-8')
            url = str(item.a['href']) 
            thumb = str(item.img['src'])   
            name = name+' - '+interpret
            #print name+interpret,url,thumb
            addDir(name,url,10,thumb)
    try:
        pager = doc.find('ul', 'j-center m-page')
        act_page_a = pager.find('li', 'active')
        act_page = act_page_a.getText(" ").encode('utf-8')
        for item in pager.findAll('a'):
            page_url = item['href'].encode('utf-8')
            page_no = item.getText(" ").encode('utf-8')
            #print page_url,page_no
            next_label = '= Strana '+act_page+' >> Další '+page_no+' ='
            if int(page_no) < int(act_page):
                continue
            addDir(next_label,page_url,7,nexticon)
            #print next_label,page_url
    except:
        print 'STRÁNKOVÁNÍ NENALEZENO'
                
def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    cast_url = urlparse(url)
    videoid = re.compile('videoId=(.+?)&').findall(httpdata)
    playlisturl = 'http://'+cast_url[1]+'/services/Video.php?clip='+videoid[0]
    print playlisturl
    doc = read_page(playlisturl)
    title = str(doc.event['title'].encode('utf-8'))    
    thumb = str(doc.event['image'])    
    items = doc.find('files')
    for item in items.findAll('file'):
        link = str(item['url'])    
        cesta = str(item['path'])
        kvalita = str(item['label'])             
        server = re.compile('rtmp://(.+?)/').findall(link)
        name = kvalita+ ' - ' + title
        tcurl = 'rtmp://'+server[0]
        swfurl = 'http://b.static.huste.tv/fileadmin/templates/swf/HusteMainPlayer.swf'
        rtmp_url = tcurl+' playpath='+cesta+' pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true'  
        print name,rtmp_url,thumb[0]
        addLink(name,rtmp_url,thumb[0],name)



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
        OBSAH_HUDBA(url)

elif mode==2:
        print ""+url
        OBSAH_RELACE(url)

elif mode==3:
        print ""+url
        OBSAH_FILMY(url)

elif mode==4:
        print ""+url
        PROUZEK(url)

elif mode==5:
        print ""+url
        ABC(url)

elif mode==6:
        print ""+url
        NAZEV(url)

elif mode==7:
        print ""+url
        INDEX(url)

elif mode==8:
        print ""+url
        FILMY_ABC(url)

elif mode==9:
        print ""+url
        FILMY_INDEX(url)
        
elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
