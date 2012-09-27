import os
import threading
import subprocess
import sys
import time
imghandlers = []


def readexifdate(filename):
	return int(os.path.getctime(filename))

try:
	sys.path.append("pyexiftool")
	import exiftool
	tool = exiftool.ExifTool()
	tool.start()
	def rxd(filename):
		try:
			t = tool.get_tag("CreateDate", filename)
			t = int(time.mktime(time.strptime(t, "%Y:%m:%d %H:%M:%S")))
			#print tool.execute_json("-d","%s","-CreateDate", filename)[0]
			#t = int(tool.execute_json("-d","%s","-CreateDate", filename)[0]["EXIF:CreateDate"])
			print("exiftool says "+str(t))
			return t#int(tool.get_tag("CreationDate", filename))
		except:#herp
			print("reading exif failed, using file creation time")
			return int(os.path.getctime(filename))
	readexifdate = rxd
except ImportError:
	print("WARNING:exiftool module is not available (may not be able to read creation dates)")

THUMBGENSIZE=256

def besthandler(filename):
	bestrat = 0
	bestyet = None
	for handler in imghandlers:
		if(handler.priority(filename) > bestrat):
			bestrat = handler.priority(filename)
			bestyet= handler
	return bestyet
#TODO:restructure so handlers represent single editors with a global open and canopenwith, possibly separate systems for takentime and genthumb

def open(filename, index=0, callback=None):#this will get rewritten
	threading.Thread(target=besthandler(filename).open, args=(filename, index, callback)).start()




def registerhandler(h):
	imghandlers.append(h)



class imghandler:#base class for image functions
	def priority(self, filename):#return 0-10 (0=can't handle, 10=native)
		return 0
	def genthumb(self, filename, thumbfile):#return none
		pass
	def canopenwith(self, filename):#return a list of programs it can be opened with
		return []
	def open(self, filename, index=0, callback=None):#open with that program (returns immediately?) return none callback gets called if we make a new version
		pass
	#def takentime(self, filename):#time the photo was taken in unix time
	#	return 0
	def takentime(self, filename):
		return readexifdate(filename)#return int(os.path.getctime(filename))#FIXME:this is the file creation/modification time, not the taken date


class jpgpnghandler(imghandler):
	def priority(self, filename):
		if ".jpg" in filename or ".JPG" in filename or ".png" in filename or ".PNG" in filename:
			return 10
		return 0
	def genthumb(self, filename, thumbfile):
		os.system("convert \""+filename+"\" -resize "+str(THUMBGENSIZE)+"x"+str(THUMBGENSIZE)+" \""+thumbfile+"\"")
		#pass #XXX:not implemented yet
	def open(self, filename, index=0, callback=None):
		if index == 3:
			os.system('xterm -e "exiftool \\"'+filename+'\\"|less"&')
		else:
			os.system("feh \""+filename+"\"&")

registerhandler(jpgpnghandler())


class rawhandler(imghandler):
	def priority(self, filename):
		if ".dng" in filename or ".DNG" in filename or ".cr2" in filename or ".CR2" in filename or ".ufraw" in filename or "NEF" in filename or "RAF" in filename:
			return 10
		return 0
	def genthumb(self, filename, thumbfile):
		if ".ufraw" in filename:
			os.system("ufraw-batch --size="+str(THUMBGENSIZE)+"x"+str(THUMBGENSIZE)+" --out-type=jpeg --output=\""+thumbfile+"\" \""+filename+"\"")
			return
		os.system("ufraw-batch --embedded-image --size="+str(THUMBGENSIZE)+"x"+str(THUMBGENSIZE)+" --out-type=jpeg --output=\""+thumbfile+"\" \""+filename+"\"")
	def open(self, filename, index=0, callback=None):#open with that program (returns immediately?) return none
		if index ==1:
			if ".ufraw" in filename:
				os.system("ufraw-batch --size=550x550 --create-id=no --out-type=jpg --output=- \""+filename+"\"| display&")
			else:
				os.system("ufraw-batch --embedded-image --size=550x550 --out-type=jpg --output=- \""+filename+"\"| display&")
		elif index ==2:
			os.system("ufraw-batch --embedded-image --out-type=jpg --output=- \""+filename+"\"| display&")
		elif index ==3:
			os.system('xterm -e "exiftool \\"'+filename+'\\"|less"&')
		else:
			#if callback == None:
			ff = list(os.path.split(filename))
			if ".ufraw" in ff[1]:#edits of edits get chained edits, and that's OK
				ff[1] = ff[1][:-5]
			else:
				ff[1] = ff[1][:-4]
			editnum = 0
			while os.path.exists(os.path.join(ff[0], ff[1]+"edit"+str(editnum)+".ufraw")):
				editnum += 1
			newpath = os.path.join(ff[0], ff[1]+"edit"+str(editnum)+".ufraw")
			#os.system("ufraw --create-id=also --output=\""+ff[1]+"edit"+str(editnum)+"\" --out-path=\""+ff[0]+"\" \""+filename+"\"")
			os.system("ufraw --create-id=only --output=\""+newpath[:-6]+".jpg"+"\" \""+filename+"\"")
			if os.path.exists(newpath) and callback != None:
				print("saved new version "+newpath)
				callback(newpath)
			else:
				print("didn't saved new version "+newpath)
			'''
			else:
				#TODO:run in a separate thread
				#pipe = os.popen("ufraw \""+filename+"\"")
				pipe = subprocess.Popen(("ufraw", filename), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				pipe.wait()
				output = pipe.communicate()
				print("got "+str(output))
			'''


	def takentime(self, filename):
		return readexifdate(filename)#return int(os.path.getctime(filename))#FIXME:this is the file creation/modification time, not the taken date
registerhandler(rawhandler())

