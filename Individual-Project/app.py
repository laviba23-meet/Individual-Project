from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyBRnS2hUZGCeKlGjoiK1tJX1MaKEt8FVT8",
  "authDomain": "cs-project-y2.firebaseapp.com",
  "databaseURL": "https://cs-project-y2-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "cs-project-y2",
  "storageBucket": "cs-project-y2.appspot.com",
  "messagingSenderId": "880720805455",
  "appId": "1:880720805455:web:ccacac35f69726644bb43a",
  "measurementId": "G-SGVBKHRZGH"
};
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Code goes below here


@app.route('/', methods=['GET', 'POST'])
def login():

    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            if email == 'LaviBanner@gmail.com' and password == 'Lavi080906':
                users = db.child("Users").get().val()
                return render_template('admin.html', users=users)

            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("login.html")

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
         email = request.form['email']
         password = request.form['password']
         fullname = request.form['fullname']
         try:
             login_session['user'] = auth.create_user_with_email_and_password(email, password)
             user = {"fullname": fullname, "email": email,"password":password}
             db.child("Users").child(login_session['user']
             ['localId']).set(user)
             return redirect(url_for('home'))
         except:
            error = "Authentication failed"
    return render_template("signup.html")
     

@app.route('/home',methods = ['GET', 'POST'] )
def home():
    return render_template("home.html")


@app.route('/signout', methods = ['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('login'))



@app.route('/remove', methods = ['GET', 'POST'])
def remove():
    uid = login_session['user']['localId'] 
    db.child("Users").child(uid).remove()
    auth.delete_user_account(login_session['user']['idToken'])
    return redirect(url_for('login'))

@app.route('/users', methods = ['GET', 'POST'])
def users():
    users = db.child("Users").get().val()
    return render_template("users.html", users=users)

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)