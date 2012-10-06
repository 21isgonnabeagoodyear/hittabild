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
		#self.testdb.search("NOT #hidden")
		self.thumbsacross = 5
		self.scrollrows = 0
		self.plist = []
		self.selected = {}
		self.activeselected = self.testdb.fetchone()
		self.testdb.rewind()
		

		self.scalethumbsize = images.THUMBGENSIZE#256#0 to never scale
		#self.scalethumbsize = 0#0 to never scale
		


		self.__idlecb = "derp"


		self.cbsearch(self.builder.get_object("entry2"))
		self.scrollbar.get_adjustment().upper = self.testdb.howmany()/self.thumbsacross +1
		self.scrollbar.get_adjustment().step_increment = 1
		#self.scrollbar.get_adjustment().page_increment= 1
		self.scrollbar.get_adjustment().page_size= 1
	def updateplist(self):
		#TODO:see if this is a bottleneck, cache stuff if so
		self.testdb.rewind(self.thumbsacross*self.scrollrows)
		#self.testdb.rewind()
		#for i in range(0,self.thumbsacross*self.scrollrows):
		#	self.testdb.fetchone()
		self.plist = []
		for i in range(0,self.thumbsacross*20):#limit visible pictures to 200
			ne = self.testdb.fetchone()
			if ne == None:
				break
			self.plist.append(ne)
	def redrawwhenyougetaroundtoit(self):
		def cb():
			self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))
		if self.__idlecb != "derp":
			#gtk.idle_remove(self.__idlecb)#NOTE:gtk_idle_add and remove are deprecated, but who gives a fuck
			gobject.source_remove(self.__idlecb)
			self.__idlecb = "derp"
		#self.__idlecb = gtk.idle_add(cb)#, priority=500)
		self.__idlecb = gobject.idle_add(cb, priority=gobject.PRIORITY_HIGH_IDLE)

	def cbfancykeys(self, widget, event=None, data=None):
		if event.keyval == 47:#/
			self.builder.get_object("entry2").grab_focus()
		elif event.keyval == 58:#:
			self.builder.get_object("entry1").grab_focus()
		else:
			return False
		return True
	def cbquit(self, widget, data=None):
		gtk.main_quit()
	def cbredraw(self, widget, data=None):
		self.updateplist()#XXX:doesn't go here
		ctx = widget.window.cairo_create()
		ctx.set_antialias(cairo.ANTIALIAS_NONE)
		#ctx.set_filter(cairo.FILTER_FAST)
		#ctx.scale(0.5,0.5)
		#print(widget.window.get_size())
		thumbsize = widget.window.get_size()[0]/self.thumbsacross
		ctx.set_line_width(2)
		linew = 2
		if thumbsize < self.scalethumbsize:
			ctx.scale(thumbsize/float(self.scalethumbsize), thumbsize/float(self.scalethumbsize))
			ctx.set_line_width(2/(thumbsize/float(self.scalethumbsize)))
			linew = 2/(thumbsize/float(self.scalethumbsize))
			thumbsize = self.scalethumbsize
		#print("draw "+str(int(widget.window.get_size()[1]/(widget.window.get_size()[0]/self.thumbsacross))+1))
		for i in range(0,int(widget.window.get_size()[1]/(widget.window.get_size()[0]/self.thumbsacross))+1):#TODO:whole thing needs to go in a separate thread
			for j in range(0,self.thumbsacross):
				if len(self.plist) > i*self.thumbsacross + j:
					ctx.set_source_pixbuf( thumbload.loadthumb(self.plist[i*self.thumbsacross+j][0].split(":")[0]),j*thumbsize,i*thumbsize)
					#print("drawing "+self.plist[i*self.thumbsacross+j][0])
					ctx.get_source().set_filter(cairo.FILTER_FAST)
				else:
					continue #ctx.set_source_rgb(0,0,0)
				ctx.rectangle(j*thumbsize,i*thumbsize,thumbsize, thumbsize)
				ctx.fill()
				ctx.set_source_rgb(0,0,0)
				if self.plist[i*self.thumbsacross+j] in self.selected:
					ctx.set_source_rgb(0,1,0)
				if self.plist[i*self.thumbsacross+j] == self.activeselected:
					ctx.set_source_rgb(0.8,1,0)
				'''	ctx.set_dash((1,0,0,0,0))
				else:
					ctx.set_dash((1,1,1,1,1,1,1,1))'''
				#ctx.set_line_width(2)
				ctx.rectangle(j*thumbsize,i*thumbsize,thumbsize-linew, thumbsize-linew)#should fix it so this doesn't cover up the edges of thumbnail
				ctx.stroke()
				#draw number of versions
				numversions = self.plist[i*self.thumbsacross+j][0].count(":")
				if numversions > 0:
					ctx.set_font_size(30)
					ctx.move_to(j*thumbsize + thumbsize-30, i*thumbsize + thumbsize -10)
					ctx.show_text(str(numversions+1))
					ctx.stroke()
				stars = -1
				for k in range(1,6):
					if "#"+str(k)+"stars" in self.plist[i*self.thumbsacross+j][1]:
						stars = k
						break
				ctx.set_font_size(60)
				ctx.move_to(j*thumbsize +10, i*thumbsize + thumbsize -10)
				ctx.show_text(str("*"*stars))
				ctx.stroke()

				ctx.set_font_size(20)
				ctx.move_to(j*thumbsize +thumbsize-80, i*thumbsize + thumbsize -40)
				ctx.show_text(images.describe(self.plist[i*self.thumbsacross+j][0].split(":")[0]))
				ctx.stroke()



		#	gtk.main_iteration_do()#give back control for a little bit (this actually slows everything down massively)
				
	def cbscroll(self, widget, event=None, data=None):
		#print(event.state)
		if(event.state & gtk.gdk.CONTROL_MASK):
			#print("zoom")
			partdown = (self.scrollbar.get_adjustment().value +1)/self.scrollbar.get_adjustment().upper
			if event.direction == gtk.gdk.SCROLL_DOWN:
				#print("down")
				self.thumbsacross +=1
			if event.direction == gtk.gdk.SCROLL_UP:
				#print("up")
				self.thumbsacross -=1
			self.thumbsacross = max(min(self.thumbsacross, 10), 1)
			self.scrollbar.get_adjustment().upper = self.testdb.howmany()/self.thumbsacross +1#+1 for page?  should use ceiling?
			#self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))#don't need to do this, it's done in cbscrolledbar
			self.scrollbar.get_adjustment().value = self.scrollbar.get_adjustment().upper * partdown -1
			#self.redrawwhenyougetaroundtoit()
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
		self.redrawwhenyougetaroundtoit()
		'''def cb():
			self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))
		if self.__idlecb != "derp":
			#gtk.idle_remove(self.__idlecb)#NOTE:gtk_idle_add and remove are deprecated, but who gives a fuck
			gobject.source_remove(self.__idlecb)
			self.__idlecb = "derp"
		#self.__idlecb = gtk.idle_add(cb)#, priority=500)
		#self.__idlecb = gtk.idle_add_priority(200, cb)
		self.__idlecb = gobject.idle_add(cb, priority=gobject.PRIORITY_HIGH_IDLE)
		#print("scrolled bar")'''
	def cbsearch(self, widget, event=None, data=None):
		print("SEARCHING")
		stext = unicode(widget.get_text())
		if not self.builder.get_object("hiddenview").get_active():
			stext += " NOT #hidden "
		if self.builder.get_object("5starview").get_active():
			stext += " #5stars "
		if self.builder.get_object("unratedview").get_active():
			stext += " NOT #5stars NOT #4stars NOT #3stars NOT #2stars NOT #1stars "
		if self.builder.get_object("trashview").get_active():
			stext += " #trash "
		else:
			stext += " NOT #trash "
			

		self.testdb.search(stext)
		print("found "+str(self.testdb.howmany()))
		#self.testdb.printall()
		#update scrollbar
		adj = self.scrollbar.get_adjustment()
		adj.upper = self.testdb.howmany()/self.thumbsacross
		#adj.upper = 100
		#adj.lower = 0
		#adj.pagesize = 1
		#self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))
		self.redrawwhenyougetaroundtoit()
	def cbchangedfilter(self, widget, event=None,data=None):
		self.cbsearch(self.builder.get_object("entry2"))
		self.scrollbar.get_adjustment().upper = self.testdb.howmany()/self.thumbsacross +1
	def cbclickedthumb(self, widget, event, data=None):
		widget.grab_focus()
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
				self.selected[one] = 1#NOTE:shift clicking the active thumb can select all which may use loads of memory
				print one
				one = self.testdb.fetchone()
			self.selected[one] = 1

		self.activeselected = self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)]
		#TODO:take input focus
		#print event.state
			
		#self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))
		self.redrawwhenyougetaroundtoit()
	def cbclickedthumba(self, widget, event, data=None):#need button down event to detect double clicks
		thumbsize = widget.window.get_size()[0]/self.thumbsacross
		if event.type == gtk.gdk._2BUTTON_PRESS:
			imagetoopen = self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)]
			def addcallbackactual(newfilenames):#FIXME:this doesn't work if we edit the image while it is open
				nu = list(imagetoopen)
				for i in range(0,len(newfilenames)):
					nu[0] = newfilenames[i] + ":" + nu[0]
				if not "#versioned" in nu[1]:
					nu[1] += " #versioned"
				self.testdb.edit(imagetoopen, nu)
				self.testdb.save()
				self.redrawwhenyougetaroundtoit()
			def addcallback(newfilenames):#call only once
				gobject.idle_add(addcallbackactual, newfilenames, priority=gobject.PRIORITY_HIGH_IDLE)

			if event.button == 3:
				#images.besthandler(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0]).open(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0], 1)
				images.open(imagetoopen[0].split(":")[0],1, callback=addcallback)
			elif event.button == 2:
				#images.besthandler(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0]).open(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0], 2)
				images.open(imagetoopen[0].split(":")[0],2, callback=addcallback)
			elif event.button == 1:
				#images.besthandler(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0]).open(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0], callback=1)
				images.open(imagetoopen[0].split(":")[0], callback=addcallback)
			elif event.button == 10:
				#images.besthandler(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0]).open(self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0].split(":")[0], 3)
				images.open(imagetoopen[0].split(":")[0],3, callback=addcallback)
			else:
				print("unrecognized mouse button" + str(event.button))
			#print("open "+self.plist[self.thumbsacross*int((event.y/thumbsize)) + int(event.x/thumbsize)][0])
		#print event.type
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
			#self.builder.get_object("drawingarea1").draw(gtk.gdk.Rectangle(0,0,10000,10000))
			self.redrawwhenyougetaroundtoit()
		elif event.keyval == 65366:#FIXME:don't use literal here (page up)
			self.scrollrows = max(min(self.scrollrows+1, self.testdb.howmany()/self.thumbsacross), 0)
			self.scrollbar.get_adjustment().value = self.scrollrows
		elif event.keyval == 65365:#FIXME:don't use literal here (page down)
			self.scrollrows = max(min(self.scrollrows-1, self.testdb.howmany()/self.thumbsacross), 0)
			self.scrollbar.get_adjustment().value = self.scrollrows
		elif event.keyval ==33:
			#regenerate thumbnail
			for f in self.selected:
				thumbload.forcereload(f[0].split(":")[0])
				#reload creation date
				oldestdate = 10000000000
				for g in f[0].split(":"):
					newdate = images.besthandler(g).takentime(g)
					if newdate < oldestdate:
						oldestdate = newdate
				newitem = (f[0],f[1],oldestdate)
				self.testdb.edit(f, newitem)

			self.redrawwhenyougetaroundtoit()
		elif event.keyval >= 48  and event.keyval <= 53:
			for sel in self.selected.keys():
				nu = list(sel)
				nu[1] = " ".join(filter(lambda x:x not in ["#0stars","#1stars", "#2stars", "#3stars", "#4stars", "#5stars"] ,nu[1].split(" ")))
				nu[1] += " #"+str(event.keyval-48)+"stars"
				self.testdb.edit(sel, nu)
				del self.selected[sel]
				self.selected[tuple(nu)] = 1
			self.testdb.save()
			self.updateplist()
			self.redrawwhenyougetaroundtoit()
		elif event.keyval == 106:#j
			#self.testdb.rewind((self.scrollrows-1)*self.thumbsacross)
			self.testdb.rewind()
			derp = self.testdb.fetchone()
			while derp != self.activeselected and derp != None:
				derp = self.testdb.fetchone()
			for i in range(0,self.thumbsacross -1):
				self.testdb.fetchone()
			self.activeselected = self.testdb.fetchone()
			self.scrollrows += 1
			self.scrollbar.get_adjustment().value = self.scrollrows
			#self.redrawwhenyougetaroundtoit()
		elif event.keyval == 107:#k
			self.testdb.rewind()
			prev = []
			for i in range(0,self.thumbsacross):
				prev.append(self.testdb.fetchone())
			tmp = self.testdb.fetchone()
			while tmp != self.activeselected and tmp != None:
				prev.append(tmp)
				prev.pop(0)
				tmp = self.testdb.fetchone()
			self.activeselected = prev[0]
			self.scrollrows -= 1
			self.scrollbar.get_adjustment().value = self.scrollrows
		elif event.keyval == 108:#l
			self.testdb.rewind()
			numpassed = 1
			while self.testdb.fetchone() != self.activeselected:
				numpassed +=1
			self.activeselected = self.testdb.fetchone()
			if numpassed % self.thumbsacross ==0:
				self.scrollrows += 1
				self.scrollbar.get_adjustment().value = self.scrollrows
			else:
				self.redrawwhenyougetaroundtoit()
		elif event.keyval == 32:#space
			if self.activeselected in self.selected:
				del self.selected[self.activeselected] 
			else:
				self.selected[self.activeselected] = 1
		elif event.keyval == 104:#h
			print "dis is hard"
			self.testdb.rewind()
			prev = self.testdb.fetchone()
			tmp = self.testdb.fetchone()
			numpassed = 1
			while tmp != self.activeselected and tmp != None:
				prev = tmp
				tmp = self.testdb.fetchone()
				numpassed +=1
			self.activeselected = prev
			if numpassed % self.thumbsacross ==0:
				self.scrollrows -= 1
				self.scrollbar.get_adjustment().value = self.scrollrows
			else:
				self.redrawwhenyougetaroundtoit()
		elif event.keyval == 99 and event.state & gtk.gdk.CONTROL_MASK:
			buf = ""
			for img in self.selected.keys():
				buf += '"'+img[0].split(":")[0]+'" '
			gtk.Clipboard().set_text(buf)
			
		elif event.keyval == 65535:#delete
			for sel in self.selected.keys():
				nu = list(sel)
				if "#trash" not in sel[1]:
					nu[1] += " #trash"
				self.testdb.edit(sel, nu)
				del self.selected[sel]
				self.selected[tuple(nu)] = 1
			self.testdb.save()
			self.updateplist()
			self.redrawwhenyougetaroundtoit()
		else:
			print(event.keyval)

def main():
	if len(sys.argv) > 2 and sys.argv[1] == "add":
		db = database.pdb("test.pdb")
		for i in range(2,len(sys.argv)):
			db.add(sys.argv[i], photodate=images.besthandler(sys.argv[i]).takentime(sys.argv[i]))
			#print sys.argv[i]
		db.save()
	elif len(sys.argv) > 1 and sys.argv[1] == "reloaddates":
		db = database.pdb("test.pdb")
		item = db.fetchone()
		while item != None:
			oldestdate = 10000000000
			for f in item[0].split(":"):
				newdate = images.besthandler(f).takentime(f)
				if newdate < oldestdate:
					oldestdate = newdate
			newitem = (item[0],item[1],oldestdate)
			db.edit(item, newitem)
			item = db.fetchone()
		db.save()
	elif len(sys.argv) > 1 and sys.argv[1] == "newdb":
		database.makenew("test.pdb")
	elif len(sys.argv) > 1 and sys.argv[1] == "makethumbs":
		db = database.pdb("test.pdb")
		item = db.fetchone()
		while item != None:
			thumbload.loadthumb(item[0].split(":")[0])
			item = db.fetchone()
	elif len(sys.argv) > 1 and sys.argv[1] == "info":
		db = database.pdb("test.pdb")
		print("number of images: "+str(db.howmany()))
	else:
		mw = mainwin()
		gtk.main()


if __name__ == "__main__":
	#cProfile.run("main()")
	main()
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
