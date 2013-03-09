# -*- coding: utf-8 -*-
# *
# *thanks to
# * http://code.google.com/p/xbmc-doplnky/
#
# Modify: 2013-03-06, Ivo Brhel
#

import os,re,sys,urllib2,urllib,traceback,time,socket
import xbmcgui,xbmcplugin,xbmc


def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("Download","Stahování souboru",os.path.basename(dest))
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED" # need to get this part working
        dp.close()


def download(addon,filename,url,notifyFinishDialog=True):
	icon = os.path.join(addon.getAddonInfo('path'),'icon.png')
	notify = addon.getSetting('download-notify') == 'true'
	notifyEvery = addon.getSetting('download-notify-every')
	notifyPercent = 1
	if int(notifyEvery) == 0:
		notifyPercent = 10
	if int(notifyEvery) == 1:
		notifyPercent = 5
		
	def callback(percent,speed,est,filename):
                if percent == 0 and speed == 0:
			xbmc.executebuiltin('XBMC.Notification(%s,%s,3000,%s)' % (xbmc.getLocalizedString(13413).encode('utf-8'),filename,icon))
			#xbmc.executebuiltin('XBMC.Notification(%s,%s,3000,%s)' % ('Otevírám...',filename,icon))
                        return
                if notify:
                        if percent > 0 and percent % notifyPercent == 0:
                                esTime = '%ss' % est
                                if est>60:
                                        esTime = '%sm' % int(est/60)
                                message = xbmc.getLocalizedString(24042) % percent + ' - %s KB/s %s' % (speed,esTime)
                                xbmc.executebuiltin('XBMC.Notification(%s,%s,3000,%s)'%(message.encode('utf-8'),filename,icon))	  

        downloader = Downloader(callback)
        result = downloader.download(url,filename)
        try:
                if result == True:
                        if xbmc.Player().isPlaying():
                                xbmc.executebuiltin('XBMC.Notification(%s,%s,8000,%s)' % (xbmc.getLocalizedString(20177),filename.encode('utf-8'),icon))
                        else:
                                if notifyFinishDialog:
                                        xbmcgui.Dialog().ok(xbmc.getLocalizedString(20177),filename.encode('utf-8'))
                                else:
                                        xbmc.executebuiltin('XBMC.Notification(%s,%s,3000,%s)' % (xbmc.getLocalizedString(20177),filename.encode('utf-8'),icon))
                else:
                        xbmc.executebuiltin('XBMC.Notification(%s,%s,5000,%s)' % ('Chyba',filename,icon))
                        xbmcgui.Dialog().ok(filename,xbmc.getLocalizedString(257) +' : '+result)
        except:
                traceback.print_exc()

class Downloader(object):
        def __init__(self,callback = None):
                self.init_time = time.time()
                self.callback = callback
                self.gran = 50
                self.percent = -1


        def download(self,remote,filename):
                class MyURLopener(urllib.FancyURLopener):
                        def http_error_default(self, url, fp, errcode, errmsg, headers):
                                self.error_msg = 'Download failed, error : '+str(errcode)


                #if not filename:
                #        filename = os.path.basename(local)
                self.filename = filename
                if self.callback:
                        #self.callback(0,0,0,os.path.basename(filename))
                        self.callback(0,0,0,filename)
                socket.setdefaulttimeout(60)
                opener = MyURLopener()
                try:
			print filename
			print remote
                        opener.retrieve(remote,filename,reporthook=self.dlProgress)
                        if hasattr(opener,'error_msg'):
                                return opener.error_msg
                        return True
                except socket.error:
                        errno, errstr = sys.exc_info()[:2]
                        if errno == socket.timeout:
                                return 'Download failed, connection timeout'
                except:
                        traceback.print_exc()
                        errno, errstr = sys.exc_info()[:2]
                        return str(errstr)


        def dlProgress(self,count, blockSize, totalSize):
                if count % self.gran == 0 and not count == 0:
                        percent = int(count*blockSize*100/totalSize)
                        newTime = time.time()
                        diff = newTime - self.init_time
                        self.init_time = newTime
                        if diff <=0:
                                diff = 1
                        speed = int(((1/diff) * blockSize * self.gran )/1024)
                        est = int((totalSize - int(count*blockSize))/1024/speed)
                        if self.callback and not self.percent == percent:
                                #self.callback(percent,speed,est,os.path.basename(self.filename))
                                self.callback(percent,speed,est,self.filename)
                        self.percent=percent

                        
                        
