import sqlite3

class pdb:
	def __init__(self, filename):
		self.__filename = filename
		self.__db = sqlite3.connect(filename)
		self.__cur = self.__db.cursor()
	def search(self, string):#dis gon b gud
		self.__lastsearch = string
		splitstring = string.split()
		sqlpart = "SELECT * FROM photos WHERE "
		fitpart = []
		nextisor = False
		for piece in splitstring:
			if piece == "OR":
				nextisor = True
				continue#OR keyword makes the next keyword an or
			#if nextisor:
			#	sqlpart += "comment LIKE ? OR "
			#else:
			if nextisor:
				sqlpart = sqlpart[:-4]
				sqlpart += " OR "
			sqlpart += "comment LIKE ? AND "
			fitpart.append("%"+piece+"%")
			nextisor = False
		sqlpart = sqlpart[:-4]
		sqlpart += " ORDER BY taken"
		#print(sqlpart)
		self.__cur.execute(sqlpart, fitpart)
		#self.__cur.execute("SELECT * FROM photos WHERE comment LIKE ?", ("%"+string+"%",))
		pass
	def add(self, filename, comment="", photodate = 0):
		#TODO: retreive date (maybe not this file?)
		#TODO: also make sure there aren't duplicate filenames (modify existing?)
		self.__cur.execute("INSERT INTO photos VALUES (?,?,?)", (filename, comment, photodate))
		self.__db.commit()
	def printall(self):
		arow = self.__cur.fetchone()
		while arow != None:
			print(arow)
			arow = self.__cur.fetchone()
	def howmany(self):
		return self.__cur.rowcount
	


def makenew(filename):
	try:
		newdb = sqlite3.connect(filename)#FIXME:check if file exists first
		newdb.execute("CREATE TABLE photos (filenames TEXT, comment TEXT, taken INTEGER)")
		newdb.close()
	except:
		print("FAILED TO CONNECT OR CREATE TABLE the file may already be a database")
	#database is created



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
