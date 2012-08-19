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
		for piece in splitstring:
			sqlpart += "comment LIKE %?% AND "
			fitpart.append(piece)
		sqlpart = sqlpart[:-4]
		print(sqlpart)
		self.__cur.execute(sqlpart, fitpart)
		#self.__cur.execute("SELECT * FROM photos WHERE comment LIKE ?", ("%"+string+"%",))
		pass
	def add(self, filename, comment=""):
		photodate = 0#TODO:
		self.__cur.execute("INSERT INTO photos VALUES (?,?,?)", (filename, comment, photodate))
		self.__db.commit()
	def printall(self):
		arow = self.__cur.fetchone()
		while arow != None:
			print(arow)
			arow = self.__cur.fetchone()
	







def makenew(filename):
	newdb = sqlite3.connect(filename)#FIXME:check if file exists first
	newdb.execute("CREATE TABLE photos (filenames TEXT, comment TEXT, taken INTEGER)")
	newdb.close()
	#database is created



if __name__ == "__main__":
	makenew("test.pdb")
	x = pdb("test.pdb")
	x.add("derp.png", "apples and cheese")
	x.add("derp2.png", "apples and bread")
	x.add("derp3.png", "pineapples and cheese")
	x.add("derp4.png", "apples and pears")
	x.search("pine pear")
	x.printall()
