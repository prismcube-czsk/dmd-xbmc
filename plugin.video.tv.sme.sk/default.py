# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://tv.sme.sk'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
import HTMLParser
from stats import *
from datetime import datetime,timedelta

__addon__ = xbmcaddon.Addon('plugin.video.tv.sme.sk')
__profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.tv.sme.sk')
__cwd__ = __settings__.getAddonInfo('path')
__scriptname__ = __addon__.getAddonInfo('name')
icon = xbmc.translatePath( os.path.join( __cwd__, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( __cwd__, 'nextpage.png' ) )


def log(msg, level=xbmc.LOGDEBUG):
	if type(msg).__name__=='unicode':
		msg = msg.encode('utf-8')
	xbmc.log("[%s] %s"%(__scriptname__,msg.__str__()), level)

def logDbg(msg):
	log(msg,level=xbmc.LOGDEBUG)

def logErr(msg):
	log(msg,level=xbmc.LOGERROR)

def addLink(name,url,iconimage,desc):
	logDbg("addLink(): '"+name+"' url='"+url+ "' img='"+iconimage+"' desc='"+desc+"'")
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": desc} )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,desc):
	logDbg("addDir(): '"+name+"' url='"+url+"' img='"+iconimage+"' desc='"+desc+"'")
	u=sys.argv[0]+"?url="+urllib.quote_plus(url.encode('utf-8'))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))+"&desc="+urllib.quote_plus(desc.encode('utf-8'))
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": desc} )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def listCategories():
	logDbg("listCategories()")
	addDir(u'[B]Všetky videá[/B]',__baseurl__+'/hs/',3,icon,'')
	addDir(u'[B]Spravodajské[/B]',__baseurl__+'/vr/118/spravodajske/',3,icon,'')
	addDir(u'[B]Publicistické[/B]',__baseurl__+'/vr/117/publicisticke/',3,icon,'')
	addDir(u'[B]Zábavné[/B]',__baseurl__+'/vr/119/zabavne/',3,icon,'')
	addDir(u'[B]Zoznam relácií (aktívne)[/B]',__baseurl__+'/relacie/',1,icon,'')
	addDir(u'[B]Zoznam relácií (archív)[/B]',__baseurl__+'/relacie/',2,icon,'')

def listActiveShows(url):
	logDbg("listActiveShows()")
	req = urllib2.Request(__baseurl__+'/relacie/')
	req.add_header('User-Agent', _UserAgent_)
	response = urllib2.urlopen(req)
	httpdata = response.read().decode("windows-1250")
	response.close()
	match = re.compile(u'<h2 class="light">Aktívne</h2>(.+?)<h2 class="light">Archív</h2>', re.S).findall(httpdata)
	if match:
		items = re.compile('img src="(.*?)" alt=.+?<h2><a href="(.+?)">(.+?)</a></h2>', re.S).findall(match[0])
		for img,link,name in items:
			link = __baseurl__+link
			addDir(name,link,3,img,'') #!!! doplnit desc
	else:
		logErr("List of TV shows not found!")

def listArchiveShows(url):
	logDbg("listArchiveShows()")
	req = urllib2.Request(__baseurl__+'/relacie/')
	req.add_header('User-Agent', _UserAgent_)
	response = urllib2.urlopen(req)
	httpdata = response.read().decode("windows-1250")
	response.close()
	match = re.compile(u'<h2 class="light">Archív</h2>(.+?)<div class="cb"></div></div>', re.S).findall(httpdata)
	if match:
		items = re.compile('img src="(.*?)" alt=.+?<h2><a href="(.+?)">(.+?)</a></h2>', re.S).findall(match[0])
		for img,link,name in items:
			link = __baseurl__+link
			addDir(name,link,3,img,'')
	else:
		logErr("List of TV shows not found!")

def listEpisodes(url):
	logDbg("listEpisodes()")
	req = urllib2.Request(url)
	req.add_header('User-Agent', _UserAgent_)
	response = urllib2.urlopen(req)
	httpdata = response.read().decode("windows-1250")
	response.close()
	match = re.compile('<div class="list">(.+?)<div id="otherartw" class="pages"', re.S).findall(httpdata)
	if match:
		items = re.compile('src="(.*?)" alt=.+?<h2>.*?<a href="(.+?)">(.+?)</a>.+?<div class="time">(.+?)</div>(.*?)</div>', re.S).findall(match[0])
		for img,link,name,date,desc in items:
			link = __baseurl__+link
			# remove new lines
			desc=desc.replace("\n", "")
			if len(desc):
				match = re.compile('<p>(.+?)</p>', re.S).findall(desc)
				if match:
					desc = match[0]
					# remove optional <span>...</span> tag
					if "<span" in desc:
						logDbg("span found")
						match = re.compile('<span.*</span>(.*)', re.S).findall(desc)
						if match:
							desc = match[0]
							logDbg("new desc: "+desc)
			addDir('('+date+') '+name,link,4,img,desc)
		items = re.compile('<div class="otherart r"><h5><a href="(.+?)">(.+?)</a>', re.S).findall(httpdata)
		if items:
			link, name = items[0]
			link = __baseurl__+link
			h = HTMLParser.HTMLParser()
			addDir('[B]'+h.unescape(name)+'[/B]',link,3,nexticon,'')
	else:
		logErr("List of episodes not found!")

def getVideoLink(url,prefix,name,desc):
	logDbg("getVideoLink()")
	req = urllib2.Request(url)
	req.add_header('User-Agent', _UserAgent_)
	response = urllib2.urlopen(req)
	httpdata = response.read().decode("windows-1250")
	response.close()
	match = re.compile('_fn\(t\)(.+?)</script>', re.S).findall(httpdata)
	if match:
		items = re.compile('var rev=(.+?);.+?"file", escape\("(.+?)"\+ rev \+"(.+?)"\)\);', re.S).findall(match[0])
		if items:
			rev,link1,link2 = items[0]
			link = link1+str(rev)+link2
			req = urllib2.Request(link)
			req.add_header('User-Agent', _UserAgent_)
			response = urllib2.urlopen(req)
			httpdata = response.read().decode("utf-8")
			response.close()
			item = re.compile('<title>(.+?)</title>.+?<location>(.+?)</location>.+?<image>(.+?)</image>', re.S).findall(httpdata)
			if item:
				title, link, img = item[0]
				addLink(prefix+name,link,img,desc)
			else:
				logErr("Video location not found!")
		else:
			logErr("Video informations not found!")
	else:
		logErr("Player script not found!")

def listVideoLink(url1,name,desc):
	logDbg("listVideoLink()")
	url1_is_hd = False
	url2 = ''
	req = urllib2.Request(url)
	req.add_header('User-Agent', _UserAgent_)
	response = urllib2.urlopen(req)
	httpdata = response.read().decode("windows-1250")
	response.close()
	match = re.compile('<div class="v-podcast-box">(.+?)<div class="v-clanok">', re.S).findall(httpdata)
	if match:
		items = re.compile('</label><a href="(.+?)" class="hd-btn(.+?)"></a>', re.S).findall(match[0])
		if items:
			url2, hd_btn_off = items[0]
			url2 = __baseurl__ + url2
			if len(hd_btn_off) == 0:
				url1_is_hd = True
		else:
			logDbg("Alternative video quality not found.")
	else:
		logErr("podcast-box not found!")
	if len(url2):
		if url1_is_hd:
			getVideoLink(url1,'[HD] ',name,desc)
			getVideoLink(url2,'[SD] ',name,desc)
		else:
			getVideoLink(url2,'[HD] ',name,desc)
			getVideoLink(url1,'[SD] ',name,desc)
	else:
		getVideoLink(url1,'',name,desc)

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

params=get_params()
url=None
name=None
desc=None
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
try:
	desc=urllib.unquote_plus(params["desc"])
except:
	pass

logDbg("Mode: "+str(mode))
logDbg("URL: "+str(url))
logDbg("Name: "+str(name))
logDbg("Desc: "+str(desc))

if mode==None or url==None or len(url)<1:
	STATS("listCategories", "Function")
	listCategories()
	
elif mode==1:
	STATS("listActiveShows", "Function")
	listActiveShows(url)

elif mode==2:
	STATS("listArchiveShows", "Function")
	listArchiveShows(url)

elif mode==3:
	listEpisodes(url)

elif mode==4:
	STATS(name, "Item")
	listVideoLink(url,name.decode('utf-8'),desc.decode('utf-8'))

xbmcplugin.endOfDirectory(int(sys.argv[1]))
