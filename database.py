import sqlite3

class pdb:
	def __init__(self, filename):
		self.__filename = filename
		self.__db = sqlite3.connect(filename)
		self.__cur = self.__db.cursor()
		self.__lastsearch = ""
		self.__howmany = 0
		self.search("")#XXX:to count rows, doing it wrong
	def search(self, string, numskip=0, dontrecountflag=True):#dis gon b gud
		#print string
		self.__lastsearch = string
		splitstring = string.split()
		sqlpart = "SELECT * FROM photos WHERE "
		fitpart = []
		nextisor = False
		nextisnot = False
		for piece in splitstring:
			if piece == "OR":
				nextisor = True
				continue#OR keyword makes the next keyword an or
			if piece == "NOT":#NOTE:untested
				nextisnot = True
				continue
			#if nextisor:
			#	sqlpart += "comment LIKE ? OR "
			#else:
			if nextisor:
				sqlpart = sqlpart[:-4]
				sqlpart += " OR "
			if nextisnot:
				sqlpart += "( comment NOT LIKE ? AND "
			else:
				sqlpart += "( comment LIKE ? AND "
			fitpart.append("%"+piece+"%")
			nextisor = False
			nextisnot = False
		sqlpart = sqlpart[:-4]
		sqlpart += len(fitpart)*")"
		sqlpart += " ORDER BY taken DESC"# LIMIT -1 OFFSET "+str(numskip)#+", 10000000000"
		#print sqlpart
		#print(sqlpart)
		#self.__cur.execute("SELECT * FROM photos WHERE comment LIKE ?", ("%"+string+"%",))
		
		#count rows because db api doesn't support this (XXX:possible bottleneck)
		#self.__howmany = -1
		if dontrecountflag:
			self.__cur.execute(sqlpart, fitpart)
			self.__howmany = 0#FIXME:this innacurate if numskip > number of rows
			for row in self.__cur:
				self.__howmany +=1
		sqlpart += " LIMIT -1 OFFSET "+str(numskip)#+", 10000000000"
		self.__cur.execute(sqlpart, fitpart)#doing it wrong
	def add(self, filename, comment="", photodate = 0):
		#TODO: retreive date (maybe not this file?)
		#TODO: also make sure there aren't duplicate filenames (modify existing?)
		self.__cur.execute("INSERT INTO photos VALUES (?,?,?)", (filename, comment, photodate))
	def edit(self, old, new):
		othercur = self.__db.cursor()
		othercur.execute("UPDATE photos SET filenames=?, comment=?, taken=? WHERE filenames=? AND comment=? AND taken=?",(new[0],new[1],new[2],old[0],old[1],old[2]))
	def printall(self):
		arow = self.__cur.fetchone()
		while arow != None:
			print(arow)
			arow = self.__cur.fetchone()
	def howmany(self):
		#TODO:count only when needed
		#return self.__cur.rowcount
		return self.__howmany
	def fetchone(self):
		rv = self.__cur.fetchone()
		if rv != None and "#hidden" in rv[1] and "NOT #hidden" in self.__lastsearch:
			print("BAD: GOT HIDDEN WHEN DISABLED "+str(rv)+str(self.__lastsearch))
			return self.fetchone()
		return rv
		#return self.__cur.fetchone()#TODO:this is final version (previous is debug)
	def rewind(self, numtoskip=0):
		self.search(self.__lastsearch, numtoskip, dontrecountflag=False)
	def save(self):
		self.__db.commit()


def makenew(filename):
	try:
		newdb = sqlite3.connect(filename)#FIXME:check if file exists first
		newdb.execute("CREATE TABLE photos (filenames TEXT, comment TEXT, taken INTEGER)")
		newdb.close()
	except:
		print("FAILED TO CONNECT OR CREATE TABLE the file may already be a database")
	#database is created

__databases = []
def add(dbfilename):#UNTESTED add a database should take an array?
	global __databases
	ndb = pdb(dbfilename)
	__databases.append(ndb)
def search(string):#search all the  databases
	pass
def howmany():#sum
	sum = 0
	for i in __databases:
		sum += i.howmany()
	return sum
def fetch(howmany):#fetch a number of results
	#TODO
	rval = []
	#
	for i in range(0,howmany):
		pass
def skip(howmany):#discard results
	pass#TODO


if __name__ == "__main__":
	makenew("test.pdb")
	x = pdb("test.pdb")
	x.add("derp.png", "apples and cheese")
	x.add("derp2.png", "apples and bread")
	x.add("derp3.png", "pineapples and cheese")
	x.add("derp4.png", "apples and pears")
	x.search("pine apple")
	x.printall()
	print("test or")
	x.search("pine OR apple")
	x.printall()
