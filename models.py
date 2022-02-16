import sqlite3, bs4, requests, re

class searchJob:
	def __init__(self, skills):
		self.skills = skills

	def ponisha(self):
		soup = bs4.BeautifulSoup(requests.get(f"https://ponisha.ir/search/projects/keyword-{self.skills}").text, "html.parser")
		titles = [str(i)[4:-5] for i in soup.findAll("h4")[:-2]]
		descriptions = [re.findall(".+",str(i)) for i in soup.findAll("div", {"class":"desc"})[:-7]]
		Descriptions = []
		for d in descriptions:
			if not d in Descriptions and descriptions.index(d)%2 == 0: Descriptions.append("".join(d[1:-1]))
		links = [i.get("href") for i in soup.findAll("a", {"class": "no-link"})[1:-4]]
		Links = []
		for l in links:
			if not l in Links: Links.append(l)
	
		result = []
	
		for T,D,L in zip(titles, Descriptions, Links):
			result.append({
				"title": T,
				"description": D,
				"link": L
			})
		return result

	def hamiworks(self):
		soup = bs4.BeautifulSoup(requests.get(f"https://hamiworks.com/project/project/searchproject?keyword={self.skills}&phrase=any&id_location=1&status=COM_JBLANCE_OPEN&project_type%5Bfixed%5D=COM_JBLANCE_FIXED&project_type%5Bhourly%5D=COM_JBLANCE_HOURLY&budget=0%2C15000000&limit=0&option=com_jblance&view=project&layout=searchproject&task=").text, "html.parser")
		titles = [i.text for i in soup.findAll("a", {"rel": "nofollow"}) if not "viewprofile" in i.get("href")]
		descriptions = titles
		links = ["https://hamiworks.com"+i.get("href") for i in soup.findAll("a", {"rel": "nofollow"}) if not "viewprofile" in i.get("href")]
	
		result = []
	
		for T,D,L in zip(titles, descriptions, links):
			result.append({
				"title": T,
				"description": D,
				"link": L
			})
		return result

urls = {
	"ponisha.ir": lambda skills : searchJob(skills).ponisha(),
	"hamiworks.com": lambda skills : searchJob(skills).hamiworks(),
}

class registration:
	keys = ["name", "email", "password", "age", "skills", "nonAllowedSites", "UUID"]
	def __init__(self):
		self.db = DB("db/users.db")
		self.db.makeStorage("""[name] NVARCHAR(160)  NOT NULL,
			[email] NVARCHAR(160)  NOT NULL,
			[password] NVARCHAR(160)  NOT NULL,
			[age] INTEGER  NOT NULL,
			[skills] NVARCHAR(160)  NOT NULL,
			[nonAllowedSites] TEXT  NOT NULL,
			[UUID] NVARCHAR(32)  NOT NULL""")

	def newUser(self, name:str, email:str, password:str, age:int, skills:str, UUID:str):
		self.db.writeStorage((name, email, password, age, skills, "", UUID))

	def getUser(self, email:str, attr="*"):
		result = self.db.searchStorage(attr, "email", email)[0]
		dictResult = {}
		for key,value in zip(registration.keys, result): dictResult[key] = value
		return dictResult

	def getUserByUUID(self, UUID:str):
		result = self.db.searchStorage("*", "UUID", UUID)[0]
		dictResult = {}
		for key,value in zip(registration.keys, result): dictResult[key] = value
		return dictResult

	def editUser(self, UUID:str, changes:dict):
		changesStr = ""
		for key,value in zip(changes.keys(), changes.values()): changesStr += f',{key} = "{value}"'
		self.db.editStorage(
			changes = changesStr[1:],
			findBy  = f'UUID = "{UUID}"'
		)

	def getAll(self, attr="*"): return [i[0] for i in self.db.readStorage(attr)]

	def makeUUID(self):
		import random
		choices = [*"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"]
		selected = "".join([random.choice(choices) for i in range(32)])
		while selected in registration().getAll(attr="UUID") :
			# make a new UUID while this UUID is exist in table
			selected = "".join([random.choice(choices) for i in range(32)])
		return selected

class DB:
	def __init__(self, db):
		self.con = sqlite3.connect(db)
		self.cur = self.con.cursor()

	def makeStorage(self, cols):
		self.cur.execute(f"CREATE TABLE IF NOT EXISTS [storage]({cols});")
		self.con.commit()

	def writeStorage(self, queries):
		fields = str("?,"*len(queries))[:-1]
		self.cur.execute(f"INSERT INTO storage VALUES({fields});", queries)
		self.con.commit()

	def searchStorage(self, target, key, value):
		self.cur.execute(f"SELECT {target} FROM storage WHERE \"{key}\"=\"{value}\";")
		result = self.cur.fetchall()
		return result

	def readStorage(self, attr="*"):
		self.cur.execute(f"SELECT {attr} FROM storage;")
		result = self.cur.fetchall()
		return result

	def editStorage(self, changes:str, findBy:str):
		self.cur.execute(f"UPDATE storage SET {changes} WHERE {findBy};")
		self.con.commit()

	def closeStorage(self):
		self.con.close()