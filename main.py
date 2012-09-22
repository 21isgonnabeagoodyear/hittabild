import sys
import gtk
import gobject
import cairo
import database
import images
import thumbload
import cProfile

class mainwin:
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file("mainwin.builder")
		self.builder.connect_signals(self)
		self.builder.get_object("drawingarea1").connect("expose_event", self.cbredraw)#NOTE: this should be done in glade but it doesn't have the handler
		self.scrollbar = self.builder.get_object("scrollbar1")
		self.testdb = database.pdb("test.pdb")
		self.testdb.search("NOT #hidden")
		self.thumbsacross = 5
		self.scrollrows = 0
		self.plist = []
		self.selected = {}
		self.activeselected = self.testdb.fetchone()
		self.testdb.rewind()
		

		self.scalethumbsize = 256#0 to never scale
		#self.scalethumbsize = 0#0 to never scale
		
		self.scrollbar.get_adjustment().upper = self.testdb.howmany()/self.thumbsacross +1
		self.scrollbar.get_adjustment().step_increment = 1
		#self.scrollbar.get_adjustment().page_increment= 1
		self.scrollbar.get_adjustment().page_size= 1


		self.__idlecb = "derp"
	def updateplist(self):
		#TODO:see if this is a bottleneck, cache stuff if so
		self.testdb.rewind()
		for i in range(0,self.thumbsacross*self.scrollrows):
			self.testdb.fetchone()
		self.plist = []
		for i in range(0,self.thumbsacross*20):#limit visible pictures to 200
			ne = self.testdb.fetchone()
			if ne == None:
				break
			self.plist.append(ne)


	def cbquit(self, widget, data=None):
		gtk.main_quit()
	def cbredraw(self, widget, data=None):
		self.updateplist()#XXX:doesn't go here
		ctx = widget.window.cairo_create()
		#ctx.scale(0.5,0.5)
		#print(widget.window.get_size())
		thumbsize = widget.window.get_size()[0]/self.thumbsacross
		ctx.set_line_width(2)
		if thumbsize < self.scalethumbsize:
			ctx.scale(thumbsize/float(self.scalethumbsize), thumbsize/float(self.scalethumbsize))
			ctx.set_line_width(2/(thumbsize/float(self.scalethumbsize)))
			thumbsize = self.scalethumbsize
		#print("draw "+str(int(widget.window.get_size()[1]/(widget.window.get_size()[0]/self.thumbsacross))+1))
		for i in range(0,int(widget.window.get_size()[1]/(widget.window.get_size()[0]/self.thumbsacross))+1):#TODO:whole thing needs to go in a separate thread
			for j in range(0,self.thumbsacross):
				if len(self.plist) > i*self.thumbsacross + j:
					ctx.set_source_pixbuf( thumbload.loadthumb(self.plist[i*self.thumbsacross+j][0].split(":")[0]),j*thumbsize,i*thumbsize)
					#print("drawing "+self.plist[i*self.thumbsacross+j][0])
				else:
					continue #ctx.set_source_rgb(0,0,0)
				ctx.rectangle(j*thumbsize,i*thumbsize,thumbsize, thumbsize)
				ctx.fill()
				ctx.set_source_rgb(0,0,0)
				if self.plist[i*self.thumbsacross+j] in self.selected:
					ctx.set_source_rgb(0,1,0)
				#ctx.set_line_width(2)
				ctx.rectangle(j*thumbsize,i*thumbsize,thumbsize-2, thumbsize-2)#should fix it so this doesn't cover up the edges of thumbnail
				ctx.stroke()



		#	gtk.main_iteration_do()#give back control for a little bit (this actually slows everything down massively)
				
	def cbscroll(self, widget, event=None, data=None):
		#print(event.state)
		if(event.state & gtk.gdk.CONTROL_MASK):
			#print("zoom")
			if event.direction == gtk.gdk.SCROLL_DOWN:
				#print("down")
				self.thumbsacross +=1
			if event.direction == gtk.gdk.SCROLL_UP:
				#print("up")
				self.thumbsacross -=1
			self.thumbsacross = max(min(self.thumbsacross, 10), 1)
			self.scrollbar.get_adjustment().upper = self.testdb.howmany()/self.thumbsacross +1#+1 for page?  should use ceiling?
			self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))#don't need to do this, it's done in cbscrolledbar
		else:
			if event.direction == gtk.gdk.SCROLL_DOWN:
				#print("down")
				self.scrollrows +=1
			if event.direction == gtk.gdk.SCROLL_UP:
				#print("up")
				self.scrollrows -=1
			if(self.scrollrows <0):
				self.scrollrows=0
			oldscrollrows = self.scrollrows#so we don't redraw when at the top or bottom (waste of code? bottleneck seems to be event system)
			self.scrollrows = max(min(self.scrollrows, self.testdb.howmany()/self.thumbsacross), 0)
			if(oldscrollrows == self.scrollrows):
				#self.scrollbar.get_adjustment().value = self.scrollrows  #DIS NIGGA SLOW
				#def cb():
				self.scrollbar.get_adjustment().value = self.scrollrows  #DIS NIGGA SLOW
				#gtk.idle_add(cb)
		#self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))#don't need to do this, it's done in cbscrolledbar
	def cbscrolledbar(self, widget, event=None, data=None):
		self.scrollrows = int(self.scrollbar.get_adjustment().value)
		def cb():
			self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))
		if self.__idlecb != "derp":
			#gtk.idle_remove(self.__idlecb)#NOTE:gtk_idle_add and remove are deprecated, but who gives a fuck
			gobject.source_remove(self.__idlecb)
			self.__idlecb = "derp"
		#self.__idlecb = gtk.idle_add(cb)#, priority=500)
		#self.__idlecb = gtk.idle_add_priority(200, cb)
		self.__idlecb = gobject.idle_add(cb, priority=gobject.PRIORITY_HIGH_IDLE)
		#print("scrolled bar")
	def cbsearch(self, widget, data=None):
		print("SEARCHING")
		if "#hidden" in unicode(widget.get_text()):
			self.testdb.search(unicode(widget.get_text()))
		else:
			self.testdb.search(unicode(widget.get_text())+" NOT #hidden ")
		print("found "+str(self.testdb.howmany()))
		#self.testdb.printall()
		#update scrollbar
		adj = self.scrollbar.get_adjustment()
		adj.upper = self.testdb.howmany()/self.thumbsacross
		#adj.upper = 100
		#adj.lower = 0
		#adj.pagesize = 1
		self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))
	def cbclickedthumb(self, widget, event, data=None):
		thumbsize = widget.window.get_size()[0]/self.thumbsacross
		print("clicked "+str(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)]))
		print((event.type))
		if event.state & gtk.gdk.CONTROL_MASK:
			if self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)] in self.selected:
				del self.selected[self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)]]
			else:
				self.selected[self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)]] = 1
		else:
			self.selected = {}
			self.selected[self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)]] = 1
			
			self.builder.get_object("entry1").set_text(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][1])
		print "evtstate:"+str(event.state & gtk.gdk.SHIFT_MASK)
		if event.state & gtk.gdk.SHIFT_MASK:#not ctrl shift?
			self.testdb.rewind()
			one = self.testdb.fetchone()
			while one != self.activeselected and one != self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)] and one != None:
				one = self.testdb.fetchone()
			self.selected[one] = 1
			one = self.testdb.fetchone()
			while one != self.activeselected and one != self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)] and one != None:
				self.selected[one] = 1
				print one
				one = self.testdb.fetchone()

		self.activeselected = self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)]
		#TODO:take input focus
		#print event.state
			
		self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))
	def cbclickedthumba(self, widget, event, data=None):#need button down event to detect double clicks
		thumbsize = widget.window.get_size()[0]/self.thumbsacross
		if event.type == gtk.gdk._2BUTTON_PRESS:
			if event.button == 3:
				images.besthandler(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0]).open(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0], 1)
			else:
				images.besthandler(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0]).open(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0])
			print("open "+self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0])
		print event.type
	def cbchangedcomment(self, widget, iconpos=0, data=None):
		print unicode(widget.get_text())
		for sel in self.selected:
			nu = list(sel)

			if self.builder.get_object("overwritebutton").get_active():
				nu[1] = unicode(widget.get_text())
			else:
				nu[1] += " "+unicode(widget.get_text())
			print("change "+str(sel)+" to "+str(nu))
			self.testdb.edit(sel, nu)
		self.testdb.save()
	def cbpressedkeycomment(self, widget, event=None, data=None):
		if event.keyval == 65293:#FIXME:don't use literal here (Return)
			print widget
			self.cbchangedcomment(widget)
	def cbpressedkeymain(self, widget, event, data=None):
		print event.keyval
		if event.keyval == 93:#FIXME:don't use literal here (])
			for sel in self.selected.keys():
				nu = list(sel)
				files = sel[0].split(":")
				nu[0] = files[-1]
				for f in files[:-1]:
					nu[0] += ":"+f
				print("change "+str(sel)+" to "+str(nu))
				self.testdb.edit(sel, nu)
				del self.selected[sel]
				self.selected[tuple(nu)] = 1
			self.testdb.save()
			self.updateplist()
			self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))

def main():
	if len(sys.argv) > 2 and sys.argv[1] == "add":
		db = database.pdb("test.pdb")
		for i in range(2,len(sys.argv)):#TODO:globbing
			db.add(sys.argv[i])
			#print sys.argv[i]
		db.save()
	elif len(sys.argv) > 1 and sys.argv[1] == "reloaddates":
		db = database.pdb("test.pdb")
		item = db.fetchone()
		while item != None:
			newdate = images.besthandler(item[0]).takentime(item[0])
			newitem = (item[0],item[1],newdate)
			db.edit(item, newitem)
			item = db.fetchone()
		db.save()
	elif len(sys.argv) > 1 and sys.argv[1] == "newdb":
		database.makenew("test.pdb")
	elif len(sys.argv) > 1 and sys.argv[1] == "makethumbs":
		db = database.pdb("test.pdb")
		item = db.fetchone()
		while item != None:
			thumbload.loadthumb(item[0])
			item = db.fetchone()
	else:
		mw = mainwin()
		gtk.main()


if __name__ == "__main__":
	cProfile.run("main()")
	'''
	if len(sys.argv) > 2 and sys.argv[1] == "add":
		db = database.pdb("test.pdb")
		for i in range(2,len(sys.argv)):#TODO:globbing
			db.add(sys.argv[i])
			#print sys.argv[i]
	else:
		mw = mainwin()
		gtk.main()
	'''
