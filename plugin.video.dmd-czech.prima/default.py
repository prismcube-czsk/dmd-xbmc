# -*- coding: utf-8 -*-

###############################################################################
REMOTE_DBG = False
# append pydev remote debugger
# http://wiki.xbmc.org/index.php?title=HOW-TO:Debug_Python_Scripts_with_Eclipse 
if REMOTE_DBG:
    try:
        import pysrc.pydevd as pydevd
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)
###############################################################################
        
import urllib2,urllib,re,os,random,decimal
#from parseutilsbs4 import *
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://play.iprima.cz'
__nejnovejsiurl__ = 'http://play.iprima.cz/primaplay/channel_ajax_more/'
__cdn_url__  = 'http://cdn-dispatcher.stream.cz/?id='
__dmdbase__ = 'http://iamm.netuje.cz/xbmc/prima/'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.prima')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.prima')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
prima = xbmc.translatePath( os.path.join( home, 'family.png' ) )
love = xbmc.translatePath( os.path.join( home, 'love.png' ) )
cool = xbmc.translatePath( os.path.join( home, 'cool.png' ) )
zoom = xbmc.translatePath( os.path.join( home, 'zoom.png' ) )
vyvoleni = xbmc.translatePath( os.path.join( home, 'vyvoleni.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
file = __settings__.getSetting('xml_file')
kvalita =__settings__.getSetting('kvalita')
konvert_nazev = __settings__.getSetting('prevod_nazev')
if kvalita == '':
    xbmc.executebuiltin("XBMC.Notification('Doplněk Prima PLAY','Vyberte preferovanou kvalitu!',30000,"+icon+")")
    __settings__.openSettings() 

def replace_words(text, word_dic):
    rc = re.compile('|'.join(map(re.escape, word_dic)))
    def translate(match):
        return word_dic[match.group(0)]
    return rc.sub(translate, text)

word_dic = {
'\u00e1': 'á',
'\u00e9': 'é',
'\u00ed': 'í',
'\u00fd': 'ý',
'\u00f3': 'ó',
'\u00fa': 'ú',
'\u016f': 'ů',
'\u011b': 'ě',
'\u0161': 'š',
'\u0165': 'ť',
'\u010d': 'č',
'\u0159': 'ř',
'\u017e': 'ž',
'\u010f': 'ď',
'\u0148': 'ň',
'\u00C0': 'Á',
'\u00c9': 'É',
'\u00cd': 'Í',
'\u00d3': 'Ó',
'\u00da': 'Ú',
'\u016e': 'Ů',
'\u0115': 'Ě',
'\u0160': 'Š',
'\u010c': 'Č',
'\u0158': 'Ř',
'\u0164': 'Ť',
'\u017d': 'Ž',
'\u010e': 'Ď',
'\u0147': 'Ň',
'\\xc3\\xa1': 'á',
'\\xc4\\x97': 'é',
'\\xc3\\xad': 'í',
'\\xc3\\xbd': 'ý',
'\\xc5\\xaf': 'ů',
'\\xc4\\x9b': 'ě',
'\\xc5\\xa1': 'š',
'\\xc5\\xa4': 'ť',
'\\xc4\\x8d': 'č',
'\\xc5\\x99': 'ř',
'\\xc5\\xbe': 'ž',
'\\xc4\\x8f': 'ď',
'\\xc5\\x88': 'ň',
'\\xc5\\xae': 'Ů',
'\\xc4\\x94': 'Ě',
'\\xc5\\xa0': 'Š',
'\\xc4\\x8c': 'Č',
'\\xc5\\x98': 'Ř',
'\\xc5\\xa4': 'Ť',
'\\xc5\\xbd': 'Ž',
'\\xc4\\x8e': 'Ď',
'\\xc5\\x87': 'Ň',
}

		
def getURL(url):
    request = urllib2.Request(url)
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()
    return data

def substr(data,start,end):
	i1 = data.find(start)
	i2 = data.find(end,i1)
	return data[i1:i2]


def OBSAH():
    addDir('[B][COLOR blue]Nejnovější videa:[/COLOR][/B]','','','','','')
    addDir('Prima Family',__nejnovejsiurl__,6,prima,0,'prima')
    addDir('Prima Cool',__nejnovejsiurl__,6,cool,0,'cool')    
    addDir('Prima Love',__nejnovejsiurl__,6,love,0,'love')
    addDir('Prima Zoom',__nejnovejsiurl__,6,zoom,0,'zoom')

    addDir('[B][COLOR blue]Pořady dle Abecedy:[/COLOR][/B]','','','','','')
    addDir('Prima Family','http://play.iprima.cz/az/vse/vse/prima',4,prima,0,'prima')
    addDir('Prima Cool','http://play.iprima.cz/az/vse/vse/cool',4,cool,0,'cool')    
    addDir('Prima Love','http://play.iprima.cz/az/vse/vse/love',4,love,0,'love')
    addDir('Prima Zoom','http://play.iprima.cz/az/vse/vse/zoom',4,zoom,0,'zoom')

    addDir('[B][COLOR blue]Žánry:[/COLOR][/B]','','','','','')	
    addDir('Akční','http://play.iprima.cz/zanry/akcni',4,icon,0, 'akcni')
    addDir('Cestování','http://play.iprima.cz/zanry/cestovani',4,icon,0, 'cestovani')
    addDir('Dobrodružství','http://play.iprima.cz/zanry/dobrodruzstvi',4,icon,0, 'dobrodruzstvi')
    addDir('Dokumenty','http://play.iprima.cz/zanry/dokumenty',4,icon,0, 'dokumenty')
    addDir('Drama','http://play.iprima.cz/zanry/drama',4,icon,0, 'drama')
    addDir('Fantasy','http://play.iprima.cz/zanry/fantasy',4,icon,0, 'fantasy')
    addDir('Filmy','http://play.iprima.cz/zanry/filmy',4,icon,0, 'filmy')
    addDir('Historie','http://play.iprima.cz/zanry/historie',4,icon,0, 'historie')
    addDir('Hry','http://play.iprima.cz/zanry/hry',4,icon,0, 'hry')
    addDir('Hudba','http://play.iprima.cz/zanry/hudba',4,icon,0, 'hudba')
    addDir('Komedie','http://play.iprima.cz/zanry/komedie',4,icon,0, 'komedie')
    addDir('Krimi','http://play.iprima.cz/zanry/krimi',4,icon,0, 'krimi')
    addDir('Lifestyle','http://play.iprima.cz/zanry/lifestyle',4,icon,0, 'lifestyle')
    addDir('Příroda','http://play.iprima.cz/zanry/priroda',4,icon,0, 'priroda')
    addDir('Publicistika','http://play.iprima.cz/zanry/publicistika',4,icon,0, 'publicistika')
    addDir('Reality','http://play.iprima.cz/zanry/reality',4,icon,0, 'reality')
    addDir('Romantika','http://play.iprima.cz/zanry/romantika',4,icon,0, 'romantika')
    addDir('Seriály','http://play.iprima.cz/zanry/serialy',4,icon,0, 'serialy')
    addDir('Soutěže','http://play.iprima.cz/zanry/souteze',4,icon,0, 'souteze')
    addDir('Sport','http://play.iprima.cz/zanry/sport',4,icon,0, 'sport')
    addDir('Talkshow','http://play.iprima.cz/zanry/talkshow',4,icon,0, 'talkshow')
    addDir('Telenovely','http://play.iprima.cz/zanry/telenovely',4,icon,0, 'telenovely')
    addDir('Vaření','http://play.iprima.cz/zanry/vareni',4,icon,0, 'vareni')
    addDir('Věda a technika','http://play.iprima.cz/zanry/veda-technika',4,icon,0, 'veda-technika')
    addDir('Zábava','http://play.iprima.cz/zanry/zabava',4,icon,0, 'zabava')
    addDir('Zpravodajství','http://play.iprima.cz/zanry/zpravodajstvi',4,icon,0, 'zpravodajstvi')

    url = 'http://play.iprima.cz/az'
    request = urllib2.Request(url)
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()
    match = re.compile('callbackItem" data-id="(.+?)" data-alias="(.+?)"><a href="(.+?)">(.+?)</a></div>').findall(data)
    for porad_id,data_alias,url,jmeno in match:
        if re.search('vse', data_alias, re.U): 
                continue
        url = 'http://play.iprima.cz/primaplay/az_ajax?letter=vse&genres='+data_alias+'&channel=vse'
        #print porad_id,data_alias,url,jmeno
        addDir(replace_words(jmeno, word_dic),url,4,__dmdbase__+data_alias+'.jpg',0,jmeno)

def NEJNOVEJSI(url,page,kanal):
   
    newurl = str(url)+''+str(page)+'/'+str(kanal)
    print "newurl: %s"%newurl
    data = getURL(newurl)
    pattern = '<div class="field-image-.+?"><a href="(.+?)"><span class="container-image.+?"><img src="(.+?)" alt="(.+?)" title=""  class="image.+?class="cover">'
    pattern = '<div class="field-image-.+?"><a href="(.+?)"><span class="container-image.+?"><img src="(.+?)" alt=.+?class="field-title"><a href=".+?" title="(.+?)">.+?</a></div>'
    match = re.compile(pattern).findall(data)
    for linkurl, obrazek, nazev in match:
        print 'linkurl :'
        print linkurl
        addDir(nazev,__baseurl__+linkurl,10,obrazek,0,nazev)
    nextpage = page+1
    addDir('>> Další strana',url,6,nexticon,nextpage,kanal)
 
	
def KATEGORIE(url,page,kanal):
    if re.search('page', url, re.U):
            match = re.compile('page=([0-9]+)').findall(url)
            strquery = '?page='+match[0]
            request = urllib2.Request(url, strquery)
    else:
        request = urllib2.Request(url)
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()
    match = re.compile('<div class=".+?" data-video-id=".+?" data-thumbs-count=".+?"><div class="field-image-primary"><a href="(.+?)"><span class=".+?195x110"><img src="(.+?)" alt="(.+?) Foto: "').findall(data)
    for url,thumb,name in match:
        #print url,thumb,name
        addDir(replace_words(name, word_dic),__baseurl__+url,10,thumb,0,name)           
    try:
        match = re.compile('<li class="pager-next last"><a href="(.+?)"').findall(data)
        #print match[0] 
        addDir('>> Další strana',__baseurl__+match[0],5,nexticon,'','')
    except:
        print 'strankovani nenalezeno'

    
def INDEX(url,page,kanal):

    data = getURL(url)
    
    pattern = '<div class="field-image-primary">.+?<img src="(.+?)".+?href="(.+?)">(.+?)</a></div><div class="field-video-count">(.+?) vide'
    match = re.compile(pattern).findall(substr(data,'<div class="items">','<div id="rightContainer">'))
    for item in match:
	   #addDir(replace_words(name+' '+pocet, word_dic),__baseurl__+url,5,thumb,0,name) 
	if konvert_nazev:
		addDir(replace_words(item[2]+' - počet videí: '+item[3], word_dic),__baseurl__+item[1],5,item[0],0,item[2])  
	else:
		addDir(item[2]+' - počet videí: '+item[3],__baseurl__+item[1],5,item[0],0,item[2])  
    try:
        pattern = '<li class="pager-next last"><a href="(.+?)"'
        match = re.compile(pattern).findall(data)
        addDir('>> Další strana',__baseurl__+match[0],4,nexticon,'','')
    except:
        print 'strankovani nenalezeno'

def VYVOLENI(url,page,kanal):
    if kanal !=1:
        addDir('Exkluzivně','http://www.iprima.cz/vyvoleni/videa-z-vily/exkluzivne',2,vyvoleni,'','1')
        addDir('Videa z TV','http://www.iprima.cz/vyvoleni/videa-z-vily/videa-z-tv',2,vyvoleni,'','1')        
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    items = re.compile('<div class="views-field-prima-field-image-primary-nid">(.+?)<span class="cover"></span></span></a></div>',re.S).findall(str(httpdata))
    match = re.compile('<a href="(.+?)"><span class="container-image-195x110"><img src="(.+?)" alt="(.+?)"',re.S).findall(str(items))    

    for url,thumb,name in match:  
            name = replace_words(name, word_dic)
            thumb = re.sub('98x55','280x158',thumb)
            req = urllib2.Request('http://www.iprima.cz'+url)
            req.add_header('User-Agent', _UserAgent_)
            response = urllib2.urlopen(req)
            httpdata = response.read()
            response.close()
            url = re.compile('"nid":"(.+?)","tid":"(.+?)"').findall(httpdata)    
            for nid,tid in url:
                url = 'http://play.iprima.cz/all/'+nid+'/all'
            addDir(name,url,10,'http://www.iprima.cz/'+thumb,'','')
                
        
def VIDEOLINK(url,name):
    request = urllib2.Request(url)
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()
    stream_video = re.compile('cdnID=([0-9]+)').findall(data)
    if len(stream_video) > 0:
        print 'LQ '+__cdn_url__+name,stream_video[0],icon,''
        addLink('LQ '+name,__cdn_url__+stream_video[0],icon,'')        
    else:
        try:
            hd_stream = re.compile('"hd_id":"(.+?)"').findall(data)
            hd_stream = hd_stream[0]
        except:
            hd_stream = 'Null'        
        hq_stream = re.compile('"hq_id":"(.+?)"').findall(data)
        lq_stream = re.compile('"lq_id":"(.+?)"').findall(data)
        geo_zone = re.compile('"zoneGEO":(.+?),').findall(data)        
        try:
            thumb = re.compile("'thumbnail': '(.+?)'").findall(data)
            nahled = thumb[0]
        except:
            nahled = icon
        key = 'http://embed.livebox.cz/iprimaplay/player-embed-v2.js?__tok'+str(gen_random_decimal(1073741824))+'__='+str(gen_random_decimal(1073741824))
        req = urllib2.Request(key)
        req.add_header('User-Agent', _UserAgent_)
        req.add_header('Referer', url)
        response = urllib2.urlopen(req)
        keydata = response.read()
        response.close()
        keydata = re.compile("_any_(.*?)'").findall(keydata)
        #keydata = re.compile("auth='(.*?)'").findall(keydata)        
        print keydata
        if geo_zone[0] == "1":
            #hd_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token?auth=_any_'+keydata[1]+'/mp4:hq/'+hd_stream[0]
            hd_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token_'+geo_zone[0]+'?auth=_any_'+keydata[1]+' playpath=mp4:hq/'+hd_stream+ ' live=true'
            hq_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token_'+geo_zone[0]+'?auth=_any_'+keydata[1]+'/mp4:'+hq_stream[0]
            lq_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token_'+geo_zone[0]+'?auth=_any_'+keydata[1]+'/mp4:'+lq_stream[0]
            if __settings__.getSetting('proxy_use')  == "true":
                proxy_ip = __settings__.getSetting('proxy_ip')
                proxy_port = str(__settings__.getSetting('proxy_port'))
                hd_url = hd_url + ' socks=' + proxy_ip+':'+proxy_port
                hq_url = hq_url + ' socks=' + proxy_ip+':'+proxy_port
                lq_url = lq_url + ' socks=' + proxy_ip+':'+proxy_port
        else:
            if re.match('Prima', hq_stream[0], re.U): 
                #hd_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token?auth=_any_'+keydata[1]+'/mp4:hq/'+hd_stream[0]
                hd_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token?auth=_any_'+keydata[1]+' playpath=mp4:hq/'+hd_stream+ ' live=true'
                hq_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token?auth=_any_'+keydata[1]+'/mp4:'+hq_stream[0]
                lq_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token?auth=_any_'+keydata[1]+'/mp4:'+lq_stream[0]
            else:
                hd_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token?auth=_any_'+keydata[1]+'/'+hd_stream
                hq_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token?auth=_any_'+keydata[1]+'/'+hq_stream[0]
                lq_url = 'rtmp://bcastgw.livebox.cz:80/iprima_token?auth=_any_'+keydata[1]+'/'+lq_stream[0]               

        #print nahled, hq_url, lq_url
        if kvalita == "HD":
            print 'HD '+name,hq_url,nahled,name
            if hd_stream == 'Null':
                addLink('HD kvalita není pro toto video dostupná!','',icon,'HD kvalita není pro toto video dostupná!')
            else:
                addLink('HD '+name,hd_url,nahled,name)
            addLink('HQ '+name,hq_url,nahled,name)            
        elif kvalita == "HQ":
            print 'HQ '+name,lq_url,nahled,name
            addLink('HQ '+name,hq_url,nahled,name)
            addLink('LQ '+name,lq_url,nahled,name)
        else:            
            print 'LQ '+name,lq_url,nahled,name
            addLink('LQ '+name,lq_url,nahled,name)
        try:
             epizody = re.compile('<a href="(.+?)" class="videocategory-link">Celé epizody').findall(data)
             print 'epizody'
             print epizody[0]
             addDir('[B][COLOR blue]Další nabídka: [/COLOR][/B]','','','','','')
             addDir('Další epizody pořadu',__baseurl__+epizody[0],5,'',0,'Další epizody pořadu')
        except:
             print 'Další epizody nenalezeny'


def gen_random_decimal(d):
        return decimal.Decimal('%d' % (random.randint(0,d)))

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

def addDir(name,url,mode,iconimage,page,kanal):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)+"&kanal="+str(kanal)
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
page=None
kanal=None
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
try:
        page=int(params["page"])
except:
        pass
try:
        kanal=str(params["kanal"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Page: "+str(page)
print "Kanal: "+str(kanal)

if mode==None or url==None or len(url)<1:
        OBSAH()
       
elif mode==1:
        print ""+str(url)
        print ""+str(kanal)
        print ""+str(page)
        KATEGORIE(url,page,kanal)

elif mode==2:
        print ""+str(url)
        print ""+str(kanal)
        print ""+str(page)
        VYVOLENI(url,page,kanal)
        
elif mode==4:
        print ""+str(url)
        print ""+str(kanal)
        print ""+str(page)
        INDEX(url,page,kanal)

elif mode==5:
        print ""+str(url)
        print ""+str(kanal)
        print ""+str(page)
        KATEGORIE(url,page,kanal)
        

elif mode==6:
        print ""+str(url)
        print ""+str(kanal)
        print ""+str(page)
        NEJNOVEJSI(url,page,kanal)
        
elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
