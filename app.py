from flask import Flask,url_for
from flask import render_template , request, flash , redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from os import path
from flask_login import LoginManager ,login_user , login_required, logout_user,current_user

from datetime import date



# date string formate convertion  
def date_dmy(dates):
    d = dates[8:]
    m = dates[5:7]
    y = dates[:4]
    return d+"-"+m+"-"+y

def date_ymd(dates):
    d = dates[:2]
    m = dates[3:5]
    y = dates[6:]
    return y+"-"+m+"-"+d


# card status function *********************************
def card_status(id):
    cards = Card.query.get(id)
    if cards.complete == True :
        return "complete"
    else:
        deadline_date =  date_ymd(cards.deadline)
        today = str(date.today())

        if deadline_date < today:
            return "deadline passed"
        else:
            return "pending"




# bild configration of the app #################################################################

app = Flask(__name__)
db = SQLAlchemy()
app.config['SECRET_KEY'] = 'GUNANIDHI3VEDI'
# database connectivity 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

db.init_app(app)



# modles section  #################################################################

class User(db.Model,UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    card = db.relationship("Card")

class Card(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    titles = db.Column(db.String(100))
    content = db.Column(db.String(500))
    deadline = db.Column(db.String(10))
    last_updated = db.Column(db.String(10))
    completion_date = db.Column(db.String(10))
    complete = db.Column(db.Boolean(), nullable=False) 
    user_id = db.Column(db.Integer , db.ForeignKey("user.id"))




def create_database(app):
    with app.app_context():
        if not path.exists("database.sqlite3"):
            db.create_all()
            print('Created Database!')

create_database(app)




# login manager #################################################################
# login related setup code  ********************************
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/api/sign_up",methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        
        username = request.form.get("username")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username exist." , category="error")
        elif password1 != password2:
            flash("Password don\'t match.",category="error")
        else :
            user = User(username = username,password = password1,name = name)
            db.session.add(user)
            db.session.commit()
            login_user(user , remember= True)
            flash("Acount created! " , category="success")
            return redirect(url_for("home"))

    return render_template("sign_up.html",user = current_user)



@app.route("/api/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if password == user.password :
                login_user(user , remember= True)
                flash("logged in successfully." , category = "success")
                return redirect(url_for("home"))

            else :
                flash("Incorrect password , try again.", category="error")
        else:
            flash("username does not exist" , category="error")
        

    return render_template("login.html",user=current_user)



@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")




# home page #################################################################
@app.route("/" ,methods=["GET","POST"])
@login_required
def home():
    return render_template("home.html", user=current_user,card_status = card_status)


# card opration ################################################################
# add card
@app.route("/api/add_card",methods=["GET","POST"])
@login_required
def add_card():
    if request.method == "POST":
        titles = request.form.get("title")
        content = request.form.get("content")
        dates = date_dmy(request.form.get("date"))
        complete = request.form.get("complete")  # return none or on 
        if complete == "1":
            complete = True
            completion_date = date_dmy(str(date.today()))

        else:
            complete = False
            completion_date = None

        today = date_dmy(str(date.today()))
        user_id = current_user.id

        new_card = Card(titles=titles, content=content, deadline=dates,last_updated = today , complete=complete,user_id=user_id, completion_date=completion_date)
        db.session.add(new_card)
        db.session.commit()
        flash("card created! " , category="success")
        return redirect(url_for("home"))

    return render_template("add_card.html", user = current_user)


# update card
@app.route('/api/edit_card/<card_id>',methods=["GET","POST"])
@login_required
def edit_card(card_id):
    card = Card.query.get(card_id)
    if card:
        if request.method == "POST":
            if card.user_id == current_user.id :
                title = request.form.get("title")
                content = request.form.get("content")
                deadline = date_dmy(request.form.get("date"))
                complete = request.form.get("complete")  # return none or on 
                if complete == "1":
                    complete = True
                    completion_date = date_dmy(str(date.today()))
                else:
                    complete = False
                    completion_date = None

                card.titles = title
                card.content = content
                card.deadline = deadline
                card.complete = complete
                card.completion_date = completion_date
                card.last_updated = date_dmy(str(date.today()))
                db.session.commit()
                flash("card updated! " , category="success")
            return redirect(url_for("home"))
        return render_template("edit_card.html",card = card,user = current_user , date_ymd = date_ymd)


# delete card
@app.route('/api/delete_card/<card_id>',methods=["GET","POST"])
@login_required
def delete_card(card_id):
    card = Card.query.get(card_id)
    if card:
        if card.user_id == current_user.id :
            db.session.delete(card)
            db.session.commit()
            flash("card deleted! " , category="success")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)

