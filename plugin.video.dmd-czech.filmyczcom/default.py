# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
import vk,novamov,videobb
import videonet,ytube,videomail
import servertools
try:
	import download
except:
	pass

__baseurl__ = 'http://filmycz.com'
#_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
_UserAgent_ =  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.filmyczcom')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.filmyczcom')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )


#==========================================================================
def OBSAH():
    addDir('Hledat ...',__baseurl__,4,icon)
    addDir('Podle kategorie',__baseurl__,1,icon)
    addDir('Serialy',__baseurl__+'/serialy/1-online',5,icon)
    addDir('Filmy',__baseurl__+'/',2,icon)
#==========================================================================



#==========================================================================
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
#==========================================================================


#==========================================================================
searchurl = __baseurl__+'/component/search/'
def SEARCH():
	keyb = xbmc.Keyboard('', 'Hledani FilmyCZ')
        keyb.doModal()
        if (keyb.isConfirmed()):
        	search = keyb.getText()
	        encode=urllib.quote(search)
		values = {'searchword': encode,'Submit': 'Search','searchphrase': 'all', 'limit': '15', 'ordering': 'newest'}
	        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	        headers = { 'User-Agent' : user_agent }
	        data = urllib.urlencode(values)
	        req = urllib2.Request(searchurl,data,headers)
	        req.add_header('User-Agent', _UserAgent_)
	        response = urllib2.urlopen(req)
	        data=response.read()
	        response.close()
		match = re.compile("<dt class=\"result-title\">[\s|\S]*?<a href=\"(.+?)\">[\s]*?(.+?)</a>[\s]+</dt").findall(data) 
		for item in match:
			name=item[1].replace('\t','')
            		addDir(name,__baseurl__+item[0],3,icon)
            		
#==========================================================================


#==========================================================================
def getUrlData(url):
	req = urllib2.Request(url)
    	req.add_header('User-Agent',_UserAgent_)
    	response = urllib2.urlopen(req)
    	data=response.read()
    	response.close()
	return data
#==========================================================================


#==========================================================================
def INDEX(url):
    doc = read_page(url)  
    items = doc.findAll('div','pos-media')
    for item in items:
            try:
		rating = item.find('div','vote-message').getText(" ").encode('utf-8')
		r = re.search('(?P<rating>.+?)rating',rating)
		if r:
			ra = r.group('rating').split('/')
			rating = float(ra[0])*2
            	item2 = item.findNextSibling()
	        popis = item2.getText(" ").encode('utf-8')
	        s  = re.search('Originální název: (?P<origname>.+?)Český název: (?P<jmeno>.+?)Datum vydání: (?P<rok>.+?)Žánry: (?P<zanry>.+?)Hrají: (?P<herci>.+?)Obsah: (?P<obsah>.+?)$',popis)
	        if s:
			origname = s.group('origname')
			name     = s.group('jmeno')
			rok      = s.group('rok')
			zanry    = s.group('zanry')
			herci    = s.group('herci').replace(' a ',',').split(',')
			obsah    = s.group('obsah')
			
	        infoLabels =  {'Title': name, 'Genre': zanry, 'Year': int(rok), 'Cast': herci, 'Rating': rating, 'OriginalTitle': origname, 'Plot': obsah}
	    
	    except:
	        infoLabels={}
      	    item = item.find('a')
            name = item['title'].encode('utf-8')
            link = item['href']
	    item = item.find('img')
            icon = item['src']
            addDir(name,__baseurl__+link,3,icon,infoLabels)
    try:
        pager = doc.find('div','pagination-bg')
        act_page_a = pager.find('span')
        act_page = act_page_a.getText(" ").encode('utf-8')
        next_page = int(act_page) + 1
	items = pager.findAll('a')
        for item in items:
		odkaz = item.getText(" ").encode('utf-8')
		if odkaz == '>':
			next_page_a = item['href']
		elif odkaz == '>>':
        		index = item['href'].rfind('/')
			max_page = item['href'][index+1:]
		else:
			continue
	if (int(next_page) > int(max_page)):
	        next_page=max_page
	next_label = 'Přejít na stranu '+ str(next_page)+' z '+ str(max_page) 
	addDir(next_label,__baseurl__+next_page_a,2,nexticon)
    except:
        print 'stop'
#==========================================================================


#==========================================================================
def SERIALY(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', _UserAgent_)
	response = urllib2.urlopen(req)
	data = response.read()
	response.close()
	match = re.compile('<div class=\"contentheading\"><h1>Seriály online</h1></div>[\s|\S]+<dl class=\"social-links\">'). findall(data)
	match = re.compile('<p><a href=\"(.+?)\">(.+?)</a></p>').findall(match[0])

	for item in match:
		addDir(item[1],__baseurl__+item[0],6,'',infoLabels={})
#==========================================================================


#==========================================================================
def SERIALY_DET(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', _UserAgent_)
	response = urllib2.urlopen(req)
	data = response.read()
	response.close()
	match = re.compile('<div class=\"contentheading\"><h1>[\s|\S]+<dl class=\"social-links\">'). findall(data)
	match = re.compile('href=\"(.+?)\">(.+?)</a>').findall(match[0])
	for item in match:
		r = re.search('mce_href=\"(?P<mce>.+?)$',item[0])
		if r:
			url = r.group('mce')
		else:
			url = item[0]
		name=item[1].replace('&nbsp;',' ')
		name=name.replace('<b></b>','')
		name=name.replace('<strong></strong>','')
		addDir(name,__baseurl__+url,3,'',infoLabels={})
#==========================================================================



#==========================================================================
def VIDEOBB_LINK(url,name):
	try:
		videourl=videobb.getURL(url)
    		addLink(name+" - videobb.com",videourl,'','')
	except:
		print "VIDEOBB URL: "+url
#==========================================================================


#==========================================================================
def NOVAMOV_LINK(url,name):
	try:
		videourl=novamov.getURL(url)
    		addLink(name+" - novamov.com",videourl,'','')
	except:
       		print "NOVAMOV.COM URL: "+url
#==========================================================================


#==========================================================================
def VKCOM_LINK(url,name):
	try:
		videourl=vk.getURL(url)
    		addLink(name+" - vk.com",videourl,'','')
	except:
       		print "VK.COM URL: "+url
#==========================================================================

#==========================================================================
def VIDEONET_LINK(url,name):
	try:
		videourl=videonet.getURL(url)
    		addLink(name+" - 24video.net",videourl,'','')
	except:
       		print "24VIDEO.NET URL: "+url
#==========================================================================

#==========================================================================
def YOUTUBE_LINK(url,name):
	try:
		videourl=ytube.getURL(url)
		addLink(name+" - youtube.com",videourl,'','')
	except:
       		print "YOUTUBE.COM URL: "+url
#==========================================================================


#==========================================================================
def VIDEOMAIL_LINK(url,name):
	try:
		videourl=videomail.getURL(url)
		addLink(name+" - videomail.ru",videourl,'','')
	except:
       		print "VIDEOMAIL.RU URL: "+url
#==========================================================================



#==========================================================================
def IFRAME_LINK(url,name):
	try:
		data  = getUrlData(__baseurl__+url)
		match = re.compile('<a href="(.+?)"').findall(data)
		data  = getUrlData(match[0])
		match = re.compile('location\.replace\("(.+?)"\)').findall(data)
		data  = getUrlData(match[0])
		items = servertools.findvideo(data)
		for server,adresa in items:
			adresa = adresa.replace('&amp;','&')
			server = server.lower()
			if server == "youtube":
				YOUTUBE_LINK(adresa,name)
	except:
       		print "IFRAME URL: "+url
#==========================================================================


#==========================================================================
def VIDEOLINK(url,name):
    print "URL: "+url
    data=getUrlData(url) 
    match=re.compile('<p>(.+?)</p>\s*.*<p style=.*><.*mce_(src|href)=\"(.+?)\".*').findall(data)
    if (len(match) < 1) or (match[0][0].find('<br /></p><p><br />') != -1) :
	items = servertools.findvideo(data)
	for server,adresa in items:
		adresa = adresa.replace('&amp;','&')
		server = server.lower()
	
		if server == "youtube":
			YOUTUBE_LINK(adresa,name+' - UKAZKA')

		if server == "24video":
			VIDEONET_LINK(adresa,name)
		if server == "videobb":
			VIDEOBB_LINK(adresa,name)
		if server == "novamov":
			NOVAMOV_LINK(adresa,name)
		if server == "vk":
			VKCOM_LINK(adresa,name)
		if server == "videomail":
			VIDEOMAIL_LINK(adresa,name)
		if server == "iframe":
			IFRAME_LINK(adresa,name)
		#else:
		#	print "VIDEOLINK URL: "+url
    else:
	for item in match:
		url = item[len(item)-1].replace('&amp;','&')
		try:
			n=item[2]
			name=item[0]
		except:
			pass 	    
		if url.find('youtube.com') != -1:
			YOUTUBE_LINK(url,name)
		elif url.find('24video.net') != -1:
			match=re.search('flash[v|V]ars.*\"id=(?P<id>.+?)&amp;idHtml=(?P<html>.+?)&amp;.*rootUrl=(?P<url>.+?)&amp;', data, re.IGNORECASE | re.DOTALL)
			VIDEONET_LINK(('%s%s%s?mode=play'% (match.group('url') , match.group('html'),match.group('id'))),name)
		elif url.find('videobb.com') != -1:
			VIDEOBB_LINK(url,name)
		elif url.find('novamov.com') != -1:
			NOVAMOV_LINK(url,name)
		elif url.find('vk.com') != -1 or url.find('vkontakte.ru') != -1:
			VKCOM_LINK(url,name)
		else:
			print "VIDEOLINK URL: "+url
#==========================================================================
	

#==========================================================================
def DOWNLOAD(url,name):
	if len(url) > 0:
		downloads = addon.getSetting('downloads')
		if '' == downloads:
			xbmcgui.Dialog().ok('FilmyCZ','Nastavte složku pro stahování')
			return
		localfile = '%s%s' % (downloads,name)
		localfile = localfile.replace(':','')
		download.download(addon,localfile,url)
		#download.DownloaderClass(videourl,localfile)
#==========================================================================
	
	
#==========================================================================
def PLAY(video_url,title):
	if video_url:
		print 'Sending %s to player' % video_url
		listitem = xbmcgui.ListItem(title)
		listitem.setInfo('video', {'Title': title})
		return xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play(video_url, listitem)
#==========================================================================
	
	
	
	
	
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




def addItem(name,url,mode,iconimage,infoLabels={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if not 'Title' in infoLabels:
		infoLabels["Title"] = name
        liz.setInfo( type="Video", infoLabels=infoLabels )
        liz.setProperty( "Fanart_Image", fanart )
        # -----
        liz.addContextMenuItems([ ( 'Stáhnout ...', "RunPlugin(%s?url=%s&mode=15&name=%s)" % ( sys.argv[0],  urllib.quote_plus(url), urllib.quote_plus(name) ) )] )
        #------
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

        
def addLink(name,url,iconimage,popis):
	addItem(name,url,7,iconimage,infoLabels={ "Title": name, "Plot": popis} )
	return True
	'''
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": popis} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
        '''
        
        
def addDir(name,url,mode,iconimage,infoLabels={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if not 'Title' in infoLabels:
		infoLabels["Title"] = name
        liz.setInfo( type="Video", infoLabels=infoLabels )
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

elif mode==4:
        print ""+url
        SEARCH()

elif mode==5:
        print ""+url
        SERIALY(url)

elif mode==6:
        print ""+url
        SERIALY_DET(url)

elif mode==7:
        print ""+url
        PLAY(url,name)
        
        
elif mode==15:
        print ""+url
        DOWNLOAD(url,name)
        

xbmcplugin.endOfDirectory(int(sys.argv[1]))


