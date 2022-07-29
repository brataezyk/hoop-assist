from flask_app import app
import re
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.court import Court
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/add_court_page')
def add_court_page():
    return render_template("/add_court.html")


@app.route('/search_map_page')
def find_court():
    return render_template("/search_map.html")

@app.route('/add_court', methods=["POST"])
def add_court():
    is_valid = Court.validate_court(request.form)

    if not is_valid:
        return redirect("/add_court_page")
    new_court = {
        'state': request.form['state'],
        'city': request.form['city'],
        'num_hoops': request.form['num_hoops'],
        'num_courts': request.form['num_courts']
    }
    id = Court.save(new_court)
    return redirect(f"/court/{id}")

@app.route('/court/<int:court_id>')
def view_court(court_id):
    data = {
        'court_id' : court_id,
        'user_id': session['user_id']
    }
    return render_template("/court_info_page.html", court = Court.view_court_id(data), user = User.get_one_user(data))

@app.route('/view_all_courts')
def all_courts():
    data = {
        "user_id": session['user_id']
    }
    return render_template("all_courts.html", courts = Court.get_all(), user = User.get_one_with_courts(data))

@app.route('/edit_court/<int:court_id>')
def edit_court_page(court_id):
    data = {
        'court_id': court_id
    }

    return render_template("/edit_court.html", court = Court.view_court_id(data) )

@app.route('/edit_court_info', methods=["POST"])
def edit_court():
    is_valid = Court.validate_court(request.form)

    if not is_valid:
        return redirect(f"/edit_court/{request.form['court_id']}")
    court_edits = {
        'court_id': request.form['court_id'],
        'state': request.form['state'],
        'city': request.form['city'],
        'num_hoops': request.form['num_hoops'],
        'num_courts': request.form['num_courts']
    }
    Court.edit_one_court(court_edits)
    # Not sure if Court ID is accessed correectly in redirect below?
    return redirect(f"/court/{court_edits['court_id']}")

@app.route('/delete/<int:court_id>')
def remove_court(court_id):
    data = {
        'court_id': court_id
    }
    Court.delete_court(data)
    return redirect("/dashboard")
