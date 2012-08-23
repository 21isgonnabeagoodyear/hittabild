import gtk
import cairo
import database
import images

class mainwin:
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file("mainwin.builder")
		self.builder.connect_signals(self)
		self.builder.get_object("drawingarea1").connect("expose_event", self.cbredraw)#NOTE: this should be done in glade but it doesn't have the handler
		self.testdb = database.pdb("test.pdb")
	def cbquit(self, widget, data=None):
		gtk.main_quit()
	def cbredraw(self, widget, data=None):
		ctx = widget.window.cairo_create()
		ctx.set_source_rgb(0.5,0.5,0.5)
		ctx.rectangle(10,10,20,20)
		ctx.fill()
	def cbsearch(self, widget, data=None):
		print("SEARCHING")
		self.testdb.search(widget.get_text())
		self.testdb.printall()
		
if __name__ == "__main__":
	mw = mainwin()
	gtk.main()

