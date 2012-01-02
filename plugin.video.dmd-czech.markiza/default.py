# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
import aes
__baseurl__ = 'http://video.markiza.sk'
__baseurl2__= 'http://voyo.markiza.sk'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
UA =  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'
key = 'EaDUutg4ppGYXwNMFdRJsadenFSnI6gJ'

addon = xbmcaddon.Addon('plugin.video.dmd-czech.markiza')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.markiza')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

def OBSAH():
    addDir('Seriály',__baseurl2__+'/zoznam/serialy/',2,icon)
    addDir('Relácie',__baseurl2__+'/stranka/relacie/',1,icon)
    addDir('Spravodajstvo',__baseurl2__+'/stranka/spravodajstvo/',1,icon)    
    addDir('FUN TV',__baseurl__+'/fun-tv',3,icon)    

    
def CAT_ALL(url):
    doc = read_page(url)
    for sekce in doc.findAll('div', 'archive-list-items'):
        for item in sekce.findAll('div', 'content'):
                item = item.find('div', 'image')
                link = item.a['href'].encode('utf-8')
                name = item.a['title'].encode('utf-8')
                thumb = item.a.img['src'].encode('utf-8')
                if re.search('voyo', link, re.U):
                    #print 'VOYO:'+link,thumb,name
                    addDir(name,link,5,thumb)
                else:
                    #print 'MARKIZA:'+link,thumb,name
                    addDir(name,link,4,thumb)


def CAT_VOYO(url):
    doc = read_page(url)
    zakazane = ['648-sultan', '/serialy/26482-5-dnu-do-pulnoci']
    items = doc.find('div', 'productsList')    
    for item in items.findAll('div', 'section_item'):
        porad = item.find('div', 'poster')
        info = item.find('div', 'item_info')
        info = info.find('a', 'watch_now only')
        if re.search('Prehrať', str(info), re.U):
            continue
        url = porad.a['href'].encode('utf-8')
        title = porad.a['title'].encode('utf-8')
        thumb = porad.a.img['src'].encode('utf-8')
        print title,url,thumb
        addDir(title,__baseurl2__+url,5,thumb)

def CAT_FUN(url):
    doc = read_page(url)
    items = doc.find('div', id='VagonFunContent')
    for item in items.findAll('div', 'item'):
        name_a = item.find('div','text')
        name_a = name_a.find('a')
        name_a = name_a.getText(" ").encode('utf-8')
        link = str(item.a['href']) 
        thumb = str(item.img['src'])  
        addDir(name_a,__baseurl__+link,4,thumb)


def LIST_MF(url):
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

def LIST_VOYO(url):
    doc = read_page(url)
    items = doc.find('div', 'productsList')
    for item in items.findAll('div', 'poster'):
        title = item.a['title'].encode('utf-8') 
        name_a = item.a['href']
        url = __baseurl2__+name_a
        thumb = str(item.img['src'])  
        addDir(title,url,11,thumb)
    try:
        pager = doc.find('div', 'pagination')
        next_item = pager.findAll('a')
       	for item in next_item:
	    if item.getText(" ").encode('utf-8') != '>':
		continue
	    else:
		next_url = item['href']
        addDir('Další strana >>',__baseurl2__+ next_url,5,nexticon)
    except:
        print 'STRANKOVANI NENALEZENO'

              
def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<media:player url="(.+?)"/>').findall(httpdata)
    thumb = re.compile('<media:thumbnail url="(.+?)"/>').findall(httpdata)
    title = re.compile('<title>(.+?)</title>').findall(httpdata)
    no = 0
    notit = 1
    for link in match:
        print '#'+str(notit) +' '+ title[0], link, thumb[no]
        addLink('#'+str(notit) +' '+ title[0],link,thumb[no],name)
        no +=1
        notit +=1

def VIDEOLINK_VOYO(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    param1 = re.compile('mainVideo = new mediaData\((.+?), (.+?), (.+?),').findall(httpdata)    
    for prod,unit,media in param1:
        site = re.compile('siteId: ([0-9]+)').findall(httpdata)
        section = re.compile('sectionId: ([0-9]+)').findall(httpdata)
        product_page = 'http://voyo.markiza.sk/bin/eshop/ws/plusPlayer.php?x=playerFlash&prod='+prod+'&unit='+unit+'&media='+media+'&site='+site[0]+'&section='+section[0]+'&subsite=produkt&embed=0&mute=0&realSite='+site[0]+'&width=704&height=441&hdEnabled=1&hash=&finish=finishedPlayer&dev=null'
    data=geturl(product_page)
    if re.search('VAROVANIE', str(data), re.U):
        xbmc.executebuiltin("XBMC.Notification('Doplněk Markíza.sk','Tento pořad nelze sledovat mimo území SR!',30000,"+icon+")")
    else:
        match = re.compile('var voyoPlusConfig.*[^"]+"(.+?)";').findall(data)
        aes_decrypt = aes.decrypt(match[0],key,128).encode('utf-8')
        aes_decrypt = aes_decrypt.replace('\/','/')
        #print aes_crypt
        server = re.compile('"host":"(.+?)"').findall(aes_decrypt)
        filename = re.compile('"filename":"(.+?)"').findall(aes_decrypt)
        bitrates = re.compile('"bitrates":(.+?)\}').findall(aes_decrypt)
        swfurl = 'http://voyo.markiza.sk/static/shared/app/flowplayer/play.swf'
        lqurl = server[0]+' playpath=mp4:'+filename[0]+'-1.mp4 pageUrl='+url+' swfUrl='+swfurl+'swfVfy=true'
        addLink(name,lqurl,icon,name)

        #if re.search('400', bitrates[0], re.U):
            #url      = 'rtmpe://vod.markiza.sk/voyosk playpath=mp4:2011/12/06/20111205_PARTICKA-1.mp4'
            #lqurl = server[0]+' playpath=mp4:'+filename[0]+'-1.mp4 pageUrl='+url+' swfUrl='+swfurl+'swfVfy=true'
            #addLink(name,lqurl,icon,name)
        #if re.search('700', bitrates[0], re.U):
            #hqurl = server[0]+' playpath=mp4:'+filename[0]+'700-1.mp4 pageUrl='+url+' swfUrl='+swfurl+'swfVfy=true'
            #addLink(name,hqurl,icon,name)

def _getfile(product_page):
	f = open(stranka, "r")
	result = f.read()
	f.close()
	return result


def geturl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link


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
        CAT_ALL(url)

elif mode==2:
        print ""+url
        CAT_VOYO(url)

elif mode==3:
        print ""+url
        CAT_FUN(url)

elif mode==4:
        print ""+url
        LIST_MF(url)


elif mode==5:
        print ""+url
        LIST_VOYO(url)

        
elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

elif mode==11:
        print ""+url
        VIDEOLINK_VOYO(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
