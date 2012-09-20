import os
imghandlers = []

def besthandler(filename):
	bestrat = 0
	bestyet = None
	for handler in imghandlers:
		if(handler.priority(filename) > bestrat):
			bestrat = handler.priority(filename)
			bestyet= handler
	return bestyet
def registerhandler(h):
	imghandlers.append(h)



class imghandler:#base class for image functions
	def priority(self, filename):#return 0-10 (0=can't handle, 10=native)
		return 0
	def genthumb(self, filename, thumbfile):#return none
		pass
	def canopenwith(self, filename):#return a list of programs it can be opened with
		return []
	def open(self, filename, index=0):#open with that program (returns immediately?) return none
		pass
	def takentime(self, filename):#time the photo was taken in unix time
		return 0


class jpgpnghandler(imghandler):
	def priority(self, filename):
		if ".jpg" in filename or ".JPG" in filename or ".png" in filename or ".PNG" in filename:
			return 10
		return 0
	def genthumb(self, filename, thumbfile):
		os.system("convert \""+filename+"\" -resize 256x256 \""+thumbfile+"\"")
		#pass #XXX:not implemented yet
	def open(self, filename, index=0):
		os.system("feh \""+filename+"\"&")
registerhandler(jpgpnghandler())


class rawhandler(imghandler):
	def priority(self, filename):
		if ".dng" in filename or ".DNG" in filename or ".cr2" in filename or ".CR2" in filename:
			return 10
		return 0
	def genthumb(self, filename, thumbfile):
		os.system("ufraw-batch --embedded-image --size=256x256 --out-type=jpeg --output=\""+thumbfile+"\" \""+filename+"\"")
	def open(self, filename, index=0):#open with that program (returns immediately?) return none
		os.system("ufraw \""+filename+"\"&")
	def takentime(self, filename):
		return int(os.path.getctime(filename))#FIXME:this is the file creation/modification time, not the taken date
registerhandler(rawhandler())

