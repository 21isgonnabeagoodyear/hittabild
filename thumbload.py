import gtk
import hashlib
import images
import random
import os

__cached = {}

def filetothumb(filename):
	return "thumbs/" +hashlib.md5(filename).hexdigest() + ".jpg"

def loadthumb(filename):
	thumb = None
	if filename in __cached:
		return __cached[filename]

	#print("loading from disk:"+filetothumb(filename))
	if len(__cached) > 100:
		del __cached[random.choice(__cached.keys())]
		#print "deleted one"
	try:
		thumb = gtk.gdk.pixbuf_new_from_file(filetothumb(filename))
		__cached[filename] = thumb
	except:
		#print("generating thumbnail:"+filetothumb(filename))
		images.besthandler(filename).genthumb(filename, filetothumb(filename))
		thumb = gtk.gdk.pixbuf_new_from_file(filetothumb(filename))
		__cached[filename] = thumb
	return thumb
def forcereload(filename):
	os.remove(filetothumb(filename))#XXX:DANGEROUS SHIT RIGHT HERE
	images.besthandler(filename).genthumb(filename, filetothumb(filename))
	del __cached[filename]
