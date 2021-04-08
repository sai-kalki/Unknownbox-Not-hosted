from flask import * 
import pymongo
from pymongo import MongoClient
from random import randint
from datetime import timedelta
from datetime import datetime

cluster = MongoClient("mongodb+srv://<username>:<password>@cluster0.unsh3.mongodb.net/PandoraBox?retryWrites=true&w=majority")
db = cluster["PandoraBox"]
msg_col = db["Messages"]
user_col = db["Users"]
app = Flask(__name__)
app.secret_key =  "b'_5#y2LF4Q8z\n\xec]/'"
app.permanent_session_lifetime = timedelta(days=2)




@app.route('/login',methods=["POST","GET"])
@app.route('/',methods=["POST","GET"])
def login():
	if request.method=="POST":
		if request.form["username"]=="":
			return render_template("login.html",Invalid_Credentials="Fill the username column")
		else:
			username=request.form["username"]
			password=request.form["password"]
			validate = user_col.find_one({"username":username})
			dbpassword = validate["password"]
			if password==dbpassword[0:-3]:
				session.permanent = True
				id = validate["_id"]
				session["id"] = id
				session["username"]=username
				return redirect(url_for('home'))
			else:
				return render_template("login.html",Invalid_Credentials="Invalid Username or password")
		
	else:
		if "id" in session:
			return redirect(url_for('home'))
		return render_template("login.html")
		
@app.route('/register',methods=["POST","GET"])
def register():
	if request.method=="POST":
		if request.form["username"]=="":
			return render_template("register.html",flash="Fill the username column")
		elif request.form.getlist('checkbox'):
			username=request.form["username"]
			password=request.form["password"]+"123"
			validate = user_col.find_one({"username":username})
		
			if validate!=None:
				return render_template("register.html",flash="Username already exists")
			else:
				session.permanent = True
				id = randint(0,99999999999999)+ randint(0,99999999)
				user = {"_id":id,"username":username,"password":password}
				user_col.insert_one(user)
				session["id"]=id
				session["username"]=username
				return redirect(url_for('home'))
		else:
			return render_template("register.html",flash="Cannot register without accepting the terms and conditions")
			
	else:
		if "id" in session:
			return redirect(url_for('home'))
		return render_template("Register.html")
		

@app.route('/home',methods=["POST","GET"])
def home():
	if "id" in session:
		idnum = session["id"]
		user = session["username"]
		return render_template("Home.html",idnum=idnum,user=user)
	else:
		return redirect(url_for('login'))	
		
	
@app.route('/messages',methods=["POST","GET"])
def messages():
	if "id" in session:
		id = str(session["id"])
		msgs = msg_col.find({"numid":id})
		msglist =  []
		timelist = []
		for msg in msgs:
			msglist.append(msg["message"])
			timelist.append(msg["time"])
		msglist.reverse()
		timelist.reverse()
		return render_template("Messages.html",msgs=msglist,times=timelist)
	else:
		return redirect(url_for('login'))
		
		

@app.route('/writemsgs/<id>',methods=["POST","GET"])
def writemsg(id):
	valid1 = int(id)
	if "id" in session:
		valid2 = int(session["id"])
	else:
		valid2=0
	if request.method=="POST":
		message=request.form["message"]
		number = id
		time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		msg = {"numid":number,"message":message,"time":time}
		msg_col.insert_one(msg)
		return redirect(url_for('successful'))
	elif valid1==valid2:
		return redirect(url_for('messages'))
	else:
		return render_template("WriteMsg.html",valid1=valid1,valid2=valid2)
	
	
	
@app.route('/successful',methods=["POST","GET"])
def successful():
	return render_template("Successful.html")		

@app.route('/terms')
def terms():
	return render_template("terms.html")	
	
	
@app.route('/logout')
def logout():
	if "id" in session:
		session.pop("id",None)
		session.pop("username",None)
		return render_template("logout.html")
	else:
		return redirect(url_for('login'))

	
if __name__=="__main__":
	app.run(debug=True)
