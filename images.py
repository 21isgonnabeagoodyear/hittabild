
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
	def priority(filename):#return 0-10 (0=can't handle, 10=native)
		return 0
	def genthumb(filename, thumbfile):#return none
		pass
	def canopenwith(filename):#return a list of programs it can be opened with
		return []
	def open(filename, index=0):#open with that program (returns immediately?) return none
		pass


class jpghandler(imghandler):
	def priority(filename):
		if ".jpg" in filename or ".JPG" in filename:
			return 10
		return 0
	def genthumb(filename, thumbfile):
		pass #XXX:not implemented yet
registerhandler(jpghandler())



