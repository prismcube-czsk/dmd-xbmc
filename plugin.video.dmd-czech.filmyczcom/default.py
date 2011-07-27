# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon

__baseurl__ = 'http://filmycz.com'
#_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
_UserAgent_ =  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'
txheaders =  {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'}
_VALID_URL = r'^((?:http://)?(?:\w+\.)?videobb\.com/(?:(?:(?:e/)|(?:video/))|(?:f/))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.filmyczcom')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.filmyczcom')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
page_pole_url = []
page_pole_no = []
novamov_url="http://www.novamov.com/api/player.api.php"


def OBSAH():
    addDir('Podle kategorie',__baseurl__,1,icon)
    addDir('Filmy Online',__baseurl__+'/',2,icon)



def KATEGORIE():
    addDir('Akční',__baseurl__+'/film/category/akcni/',2,icon)
    addDir('Animovaný',__baseurl__+'/film/category/animovany/',2,icon)
    addDir('Dobrodružný',__baseurl__+'/film/category/dobrodruzny/',2,icon)
    addDir('Dokumentární',__baseurl__+'/film/category/dokumentarni/',2,icon)
    addDir('Drama',__baseurl__+'/film/category/drama/',2,icon)
    addDir('Erotický',__baseurl__+'/film/category/eroticky/',2,icon)
    addDir('Fantasy',__baseurl__+'/film/category/fantasy/',2,icon)
    addDir('Historický',__baseurl__+'/film/category/historicky/',2,icon)
    addDir('Horory',__baseurl__+'/film/category/horory/',2,icon)
    addDir('Komedie',__baseurl__+'/film/category/komedie/',2,icon)
    addDir('Krimi',__baseurl__+'/film/category/krimi/',2,icon)
    addDir('Mysteriózní',__baseurl__+'/film/category/mysteriozni/',2,icon)
    addDir('Psychologický',__baseurl__+'/film/category/psychologicky/',2,icon)
    addDir('Rodinné',__baseurl__+'/film/category/rodinne/',2,icon)
    addDir('Romantické',__baseurl__+'/film/category/romanticke/',2,icon)
    addDir('Sci-fi',__baseurl__+'/film/category/sci-fi/',2,icon)
    addDir('Sportovní',__baseurl__+'/film/category/sportovni/',2,icon)
    addDir('Thrillery',__baseurl__+'/film/category/thrillery/',2,icon)
    addDir('Válečný',__baseurl__+'/film/category/valecny/',2,icon)




def INDEX(url):
    doc = read_page(url)  
    items = doc.findAll('div','pos-media')
    for item in items:
      	    item = item.find('a')
            name = item['title'].encode('utf-8')
            link = item['href']
	    item = item.find('img')
            icon = item['src']
            addDir(name,__baseurl__+link,3,icon)
	    #VIDEOLINK(__baseurl__+link,name)
    try:
        pager = doc.find('div', 'pagination-bg')
        act_page_a = pager.find('span')
        act_page = act_page_a.getText(" ").encode('utf-8')
        next_page = int(act_page) + 1
        url_page = int(act_page)-1
        #print act_page, url_page
        for item in pager.findAll('a'):
            page_url = item['href'].encode('utf-8')
            page_no = item.getText(" ").encode('utf-8')
            #print page_url,page_no
	    if ((page_no.isdigit()) or (page_no.isdigit())):
            	page_pole_url.append(page_url)
            	page_pole_no.append(page_no)
        max_page_count = len(page_pole_no)-1
        max_page = page_pole_url[max_page_count]
    	pole=max_page.split("/")
	max_page=pole[len(pole)-1]
	if (url_page > max_page):
		url_page=max_page
        next_url = page_pole_url[url_page]
        next_label = 'Přejít na stranu '+str(next_page)+' z '+max_page
        addDir(next_label,__baseurl__+next_url,2,nexticon)
    except:
        print 'stop'


#=========================================================================================
# Original code from 
# http://code.google.com/p/xbmc-tvalacarta/
# http://code.google.com/p/xbmc-tvalacarta/source/browse/trunk/pelisalacarta/servers/videobb.py
#=========================================================================================
def geturl_VIDEOBB(url):
    code = Extract_id(url)
    #controluri = "http://videobb.com/player_control/settings.php?v=%s&fv=v1.1.58"  %code
    controluri = "http://videobb.com/player_control/settings.php?v=%s&em=TRUE&fv=v1.1.67" %code
    #
    #datajson = scrapertools.cachePage(controluri)
    #
    req = urllib2.Request(controluri)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    datajson=response.read()
    response.close()
    #print datajson
    datajson = datajson.replace("false","False").replace("true","True")
    datajson = datajson.replace("null","None")
    datadict = eval("("+datajson+")")
    formatos = datadict["settings"]["res"]
    longitud = len(formatos)
    uri = formatos[longitud-1]["u"]
    import base64
    
    devuelve = base64.decodestring(uri)
    return devuelve

def Extract_id(url):
	# Extract video id from URL
	mobj = re.match(_VALID_URL, url)
	if mobj is None:
		print 'ERROR: URL invalida: %s' % url
		return ""
	id = mobj.group(2)
	return id
#============================================================================================

def VIDEOBB_LINK(url,name):
	try:
		videourl=geturl_VIDEOBB(url)
    		addLink(name+" - videobb.com",videourl,'','')
	except:
		print "VIDEOBB URL: "+url


def NOVAMOV_LINK(url,name):
	req = urllib2.Request(url)
    	req.add_header('User-Agent',_UserAgent_)
    	response = urllib2.urlopen(req)
    	link=response.read()
	try:
		match=re.compile('flashvars.advURL=\"(.+?)\".*').findall(link)
    		urlhq= match[0]
    		#
		req = urllib2.Request(urlhq)
   		req.add_header('User-Agent',_UserAgent_)
    		response = urllib2.urlopen(req)
    		link=response.read()
		#
    		match=re.compile('flashvars.file=\"(.+?)\".*').findall(link)
		file=match[0]
    		match=re.compile('flashvars.filekey=\"(.+?)\".*').findall(link)
		filekey=match[0]
		#
		urlhq=novamov_url+"?key="+filekey+"&pass=undefined&file="+file+"&user=undefined"
		req = urllib2.Request(urlhq)
   		req.add_header('User-Agent',_UserAgent_)
    		response = urllib2.urlopen(req)
    		link=response.read()
    		response.close()
    		#	
    		match=re.compile('url=(.+?)&title=.*').findall(link)
		urlhq=match[0]
    		addLink(name+" - novamov.com",urlhq,'','')
	except:
       		print "NOVAMOV URL: "+url




#=========================================================================================
# Original code from 
# http://code.google.com/p/xbmc-tvalacarta/
# http://code.google.com/p/xbmc-tvalacarta/source/browse/trunk/pelisalacarta/servers/vk.py
#=========================================================================================
def geturl_VK(urlvideo):
    #print "-------------------------------------------------------"
    #url=urlvideo.replace("amp;","")
    #print urlvideo
    #print "-------------------------------------------------------"
    theurl = urlvideo
    # an example url that sets a cookie,
    # try different urls here and see the cookie collection you can make !

    txdata = None
    # if we were making a POST type request,
    # we could encode a dictionary of values here,
    # using urllib.urlencode(somedict)

    #txheaders =  {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'}
    # fake a user agent, some websites (like google) don't like automated exploration

    req = urllib2.Request(theurl, txdata, txheaders)
    handle = urllib2.urlopen(req)
    #cj.save(ficherocookies)                     # save the cookies again    

    data=handle.read()
    handle.close()
    #print data
    
    # Extrae la URL

    #print data
    videourl = ""
    #quality = config.get_setting("quality_flv")
    quality="1"
       
    regexp =re.compile(r'vkid=([^\&]+)\&')
    match = regexp.search(data)
    vkid = ""
    #print 'match %s'%str(match)
    #print match
    if match is not None:
        vkid = match.group(1)
    else:
        print "no vkid"

    patron  = "var video_host = '([^']+)'.*?"
    patron += "var video_uid = '([^']+)'.*?"
    patron += "var video_vtag = '([^']+)'.*?"
    patron += "var video_no_flv = ([^;]+);.*?"
    patron += "var video_max_hd = '([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    #print matches
    if len(matches)>0:    
        for match in matches:
            if match[3].strip() == "0" and match[1] != "0":
                tipo = "flv"
                if "http://" in match[0]:
                    videourl = "%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                else:
                    videourl = "http://%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                
            elif match[1]== "0" and vkid != "":     #http://447.gt3.vkadre.ru/assets/videos/2638f17ddd39-75081019.vk.flv 
                tipo = "flv"
                if "http://" in match[0]:
                    videourl = "%s/assets/videos/%s%s.vk.%s" % (match[0],match[2],vkid,tipo)
                else:
                    videourl = "http://%s/assets/videos/%s%s.vk.%s" % (match[0],match[2],vkid,tipo)
                
            else:                                   #http://cs12385.vkontakte.ru/u88260894/video/d09802a95b.360.mp4
                #Si la calidad elegida en el setting es HD se reproducira a 480 o 720, caso contrario solo 360, este control es por la xbox
                if   match[4]=="0":
                    tipo = "240.mp4"
                elif match[4]=="1":
                    tipo = "360.mp4"
                elif match[4]== "2" and quality == "1":
                    tipo = "480.mp4"
                elif match[4]=="3" and quality == "1":
                    tipo = "720.mp4"
                else:
                    tipo = "360.mp4"
                if match[0].endswith("/"):
                    videourl = "%su%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                else:
                    videourl = "%s/u%s/video/%s.%s" % (match[0],match[1],match[2],tipo)
                
    return videourl
#=========================================================================================

def VKCOM_LINK(url,name):
	try:
		videourl=geturl_VK(url)
    		addLink(name+" - vk.com",videourl,'','')
	except:
       		print "VK.COM URL: "+url

def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    link = response.read()
    match=re.compile(' .*mce_src=\"(.+?)\" .*').findall(link)
    print match
    for item in match:
    	item = item.replace('&amp;','&')
	if item.find('youtube.com') != -1:
		continue
	elif item.find('videobb.com') != -1:
		VIDEOBB_LINK(item,name)
	elif item.find('novamov.com') != -1:
		NOVAMOV_LINK(item,name)
	elif item.find('vk.com') != -1 or item.find('vkontakte.ru') != -1:
		VKCOM_LINK(item,name)
	else:
		print "VIDEOLINK URL: "+item

	

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
        KATEGORIE()

elif mode==2:
        print ""+url
        INDEX(url)
        
elif mode==3:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


