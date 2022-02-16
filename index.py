from flask import Flask, render_template, request, redirect, jsonify
from models import registration, urls
from hashlib import sha256
from json import loads, dumps

app = Flask(__name__)

@app.route("/")
def index(): return render_template("register.html")

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html", jobs=[])

@app.route("/loadDashboard")
def loadDashboard():
	jobs = loads(getJobs(request.args.get("UUID"))).get("jobs")
	return render_template("dashboard.html", jobs=jobs)
	
@app.route("/about")
def about(): return render_template("about.html")

@app.route("/register")
def register():
	try:
		getData = request.args.get
		MODE = getData("mode")
		hashedPassword = sha256(getData("password").encode()).hexdigest()
		if MODE == "signup" :
			if not getData("email") in registration().getAll("email"):
				registration().newUser(
					name     = getData("name"),
					email    = getData("email"),
					password = hashedPassword,
					age      = int(getData("age")),
					skills   = getData("skills"),
					UUID     = registration().makeUUID()
				)
				return "حساب کاربری شما باموفقیت ساخته شد"
			else :
				return "این ایمیل قبلا استفاده شده است"
		else :
			# if MODE is not signup, so that's login.
			if getData("email") in registration().getAll("email") and hashedPassword in registration().getAll("password"):
				thisUser = registration().getUser(getData("email"))
				if thisUser.get("password") == hashedPassword:
					response = jsonify(thisUser)
					response.headers.add('Access-Control-Allow-Origin', '*')
					return response

				else : return "رمزعبور نادرست است"
			else :
				return "حسابی با این اطلاعات وجود ندارد"
	except AttributeError:
		return redirect("/")

@app.route("/settings")
def settings(): return render_template("settings.html", sites=list(urls.keys()))

@app.route("/editSite")
def editSite():
	try:
		getData = request.args.get

		user = registration().getUserByUUID(getData("UUID"))
		lastNonAllowedSites = [i for i in user.get("nonAllowedSites").replace("'","").replace("[","").replace("]","").split(",") if i != ""]
		nonAllowedSite = getData("site")

		if nonAllowedSite in lastNonAllowedSites :
			lastNonAllowedSites.remove(nonAllowedSite)
		else :
			lastNonAllowedSites.append(nonAllowedSite)

		registration().editUser(getData("UUID"), {"nonAllowedSites": ",".join(lastNonAllowedSites)})
		response = jsonify(registration().getUserByUUID(getData("UUID")))
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

	except Exception as e:
		print(e)
		return "Error"

@app.route("/api/getUser")
def getUserAPI():
	try:
		response = jsonify({"status": "ok", "response":registration().getUserByUUID(request.args.get("UUID"))})
	except Exception as e:
		response = {"status":"error", "error":str(e)}, 400

	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route("/api/getJobs")
def getJobsView():
	response = jsonify(getJobs(request.args.get("UUID")))
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.errorhandler(404)
def notFound(error): return render_template("404.html"), 404

def getJobs(UUID):
	user = registration().getUserByUUID(UUID)
	jobs = []
	for site in urls.keys() :
		if not site in user["nonAllowedSites"] :
			searchedJobs = urls[site](" ".join(user["skills"].split(",")))
			for job in searchedJobs :
				jobs.append(job)

	return dumps({"jobs":jobs})

#app.run(debug=True, port=5000)
