from flask_app import app
import re
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.court import Court
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("reg_log.html")

@app.route('/register', methods=["POST"])
def register():
    is_valid = User.validate_user(request.form)

    if not is_valid:
        return redirect("/")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save(new_user)
    if not id:
        flash("Email already taken.","register")
        return redirect('/')
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=["POST"])
def login():
    data = {
        "email": request.form['email']
    }
    user = User.get_info_email(data)
    print("**********************************")
    if not user:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id']
    }
    
    return render_template("/dashboard.html",user = User.get_one_with_courts(data))

@app.route('/edit_profile/<int:user_id>')
def edit_page(user_id):
    data = {
        'user_id' : user_id
    }
    user = User.get_one_user(data)
    session['email'] = user.email
    
    return render_template("/edit_profile.html", user = user)

@app.route('/edit_user', methods=["POST"])
def edit_user():
    is_valid = User.validate_edit(request.form, session['email'])
    if not is_valid:
        return redirect(f"/edit_profile/{request.form['user_id']}")
    # New insert
    user_edits = {
        "user_id" : request.form["user_id"],
        "first_name": request.form["new_first_name"],
        "last_name": request.form["new_last_name"],
        "email": request.form["new_email"],
        "password": bcrypt.generate_password_hash(request.form["new_password"]),
    }
    User.edit_one_user(user_edits)
    user_id = request.form['user_id']
    return redirect('/dashboard')

@app.route('/upload_profile_pic', methods=["POST"])
def upload_pic():
    data = {
        'user_id' : request.form['user_id'],
        'new_picture' : request.form['new_picture']
    }
    user = User.update_profile_pic(data)
    return redirect(f"/edit_profile/{request.form['user_id']}")

@app.route('/add_to_fav', methods=["POST"])
def plus_favs():
    data = {
        "court_id" : request.form['court_id'],
        "user_id" : request.form['user_id']
    }
    user = User.get_one_with_courts(data)
    is_valid = User.validate_fav(user, data)
    if not is_valid:
        return redirect(f"/court/{request.form['court_id']}")
    user = User.add_fav_court(data)
    return redirect(f"/court/{request.form['court_id']}")




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')