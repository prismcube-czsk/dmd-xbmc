# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon

__baseurl__= 'http://voyo.markiza.sk'
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
    addDir('Seriály',__baseurl__+'/serialy/',1,icon)
    addDir('Relácie',__baseurl__+'/relacie/',1,icon)
    addDir('Šport',__baseurl__+'/sport/',1,icon)
    addDir('Spravodajstvo',__baseurl__+'/spravodajstvo/',1,icon)        


def CAT_VOYO(url):
    doc = read_page(url)
    zakazane = ['26482-5-dnu-do-pulnoci']
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
        print title, url, thumb
        addDir(title,__baseurl__+url,5,thumb)
    try:
        items = doc.find('div', 'pagination')
        for item in items.findAll('span', 'normal'):
            url = __baseurl__+str(item.a['href'])
            
            doc = read_page(url)
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
                print title, url, thumb
                addDir(title,__baseurl__+url,5,thumb)
    except:
        print 'Stránkování nenalezeno',url


def LIST_VOYO(url):
    doc = read_page(url)
    items = doc.find('div', 'productsList')
    for item in items.findAll('div', 'poster'):
        title = item.a['title'].encode('utf-8') 
        name_a = item.a['href']
        url = __baseurl__+name_a
        thumb = str(item.img['src'])  
        addDir(title,url,10,thumb)
    try:
        pager = doc.find('div', 'pagination')
        next_item = pager.findAll('a')
       	for item in next_item:
	    if item.getText(" ").encode('utf-8') != '>':
		continue
	    else:
		next_url = item['href']
        addDir('Další strana >>',__baseurl__+ next_url,5,nexticon)
    except:
        print 'STRANKOVANI NENALEZENO'

              
def VIDEOLINK_VOYO(url,name):
    URL2ALIAS = {'rodinna-kliatba':'rodkliatba',
                 'druhy-dych':'druhydych',
                 'mesto-tienov':'mestotienov',
                 'televizne-noviny':'tn',
                 'prve-televizne-noviny':'ptn',
                 'rychle-televizne-noviny-13-00':'rtn1300',
                 'rychle-televizne-noviny-14-00':'rtn1400',
                 'rychle-televizne-noviny-15-00':'rtn1500',
                 'rychle-televizne-noviny-16-00':'rtn1600',
                 'rychle-televizne-noviny-17-00':'rtn1700',
                 'rychle-televizne-noviny-18-00':'rtn1800',
                 'prve-pocasie':'ppocasie',
                 'sportove-noviny':'sport',
                 'zo-zakulisia-markizy':'zakulisie',
                 'na-telo':'natelo',
                 'modre-z-neba':'mzn',
                 'bez-servitky':'bezservitky',
                 'mafianske-popravy':'popravy'}
    if re.search('rychle-televizne-noviny', url, re.U):
        match = re.compile('\/[0-9]+-(.+?)-([0-9]+)-([0-9]+)-([0-9]+)-([0-9]+)-([0-9]+)-.+?').findall(url)
        for jmeno,hodina,minuta,mesic,den,rok in match:
            jmeno = jmeno+'-'+hodina+'-'+minuta
            if URL2ALIAS.has_key(jmeno):
                jmeno = URL2ALIAS[jmeno].swapcase()        
    else:            
        match = re.compile('\/[0-9]+-(.+?)-([0-9]+)-([0-9]+)-([0-9]+)-.+?').findall(url)
        for jmeno,mesic,den,rok in match:
            print jmeno,mesic,den,rok
            if URL2ALIAS.has_key(jmeno):
                jmeno = URL2ALIAS[jmeno]
            if re.search('-', jmeno, re.U):
                jmeno = re.compile('(.+?)-.+?').findall(jmeno)
                jmeno = jmeno[0]
        jmeno = jmeno.swapcase()
    cesta = 'mp4:'+rok+'/'+den+'/'+mesic+'/'+rok+'-'+den+'-'+mesic+'_'+jmeno+'-1.mp4'
    print jmeno,den,mesic,rok,cesta
    swfurl = 'http://voyo.markiza.sk/static/shared/app/flowplayer/13-flowplayer.cluster-3.2.1-01-004.swf'
    #lqurl = 'rtmpe://vod.markiza.sk/voyosk playpath='+cesta+' pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true'
    lqurl = 'rtmpe://vod.markiza.sk/voyosk playpath='+cesta+' conn=O:1 conn=NN:0:2274958.000000 conn=NS:1: conn=NN:2:1408.000000 conn=NS:3:null conn=O:0 pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true'    
    addLink(name,lqurl,icon,name)

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
        CAT_VOYO(url)

elif mode==5:
        print ""+url
        LIST_VOYO(url)

        
elif mode==10:
        print ""+url
        VIDEOLINK_VOYO(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
