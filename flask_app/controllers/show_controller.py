from flask import Flask, render_template, request, redirect, request, session, flash
from flask_app import app
from flask_app.models import show_model
from flask_app.controllers import user_controller
from flask_bcrypt import Bcrypt   
import pprint     
bcrypt = Bcrypt(app)

@app.route("/add_show")
def add_show():
    print('RENDERING add_show TEMPLATE')
    return render_template("add_show.html")

@app.route('/create', methods=['POST'])
def add_new_show():
    raw_show_data = request.form
    print("this is the raw_show_data:", raw_show_data)
    if not 'user_id' in session:
        flash('please log in', 'show')
        return redirect('/add_show')
    if not show_model.Show.validate_show(raw_show_data):
        return redirect('/add_show')
    print("Validating Show!!")
    # else no errors:
    valid_show_data = {
        "title": raw_show_data["title"],
        "network": raw_show_data["network"],
        "release_date": raw_show_data["release_date"],
        "description": raw_show_data["description"],
        "posted_by": raw_show_data["posted_by"]
    }
    print("This is the valid_show_data:", valid_show_data)
    new_show_id = show_model.Show.save(valid_show_data)
    print('This is the new show id=', new_show_id)
    return redirect("/dashboard")

@app.route('/view_show/<int:show_id>')
def show_details(show_id):
    show_data = {
        "show_id":show_id
    }
    show_to_view = show_model.Show.get_one(show_data)
    all_likes = show_model.Show.get_show_with_likes(show_data)
    count = show_model.Show.get_like_count(show_data)
    print("the show:")
    print(show_to_view)
    # liked_by = show_model.Show.get_driver_by_id(ride_data)
    return render_template("view_show.html", show=show_to_view, all_likes=all_likes, count=count)

@app.route('/edit_show/<int:show_id>')
def edit_show(show_id):
    show_data = {
        "id":show_id
    }
    show = show_model.Show.get_by_id(show_data)
    return render_template('edit_show.html', show=show)

@app.route('/edit_show/<int:show_id>', methods=['POST'])
def update_show(show_id):
    raw_show_data = request.form
    if not show_model.Show.validate_show_update(raw_show_data):
        flash('Not Valid Show Information')
        return redirect(f"/edit_show/{show_id}")
    valid_show_data = {
        'id': show_id,
        "title": raw_show_data["title"],
        "network": raw_show_data["network"],
        "release_date": raw_show_data["release_date"],
        "description": raw_show_data["description"],
        "posted_by": raw_show_data["posted_by"]
    }
    show_model.Show.update(valid_show_data)
    return redirect('/dashboard')

@app.route("/like_show/<int:show_id>", methods=["POST"])
def like_show(show_id):
    raw_show_data = request.form
    show_data = {
        "show_id":raw_show_data["show_id"],
        "liked_by": raw_show_data["liked_by"]
    }
    show_model.Show.assign_like(show_data)
    all_likes = show_model.Show.get_show_with_likes(show_data)
    print("this id liked this show:", show_data)
    return redirect("/dashboard")

@app.route('/unlike_show/<int:show_id>')
def cancel_like(show_id):
    show_data = {
        "show_id":["show_id"],
        "liked_by":["liked_by"]
    }
    show_model.Show.cancel_like(show_data)
    return redirect('/dashboard')

@app.route('/delete/<int:show_id>')
def delete(show_id):
    show_model.Show.delete(show_id)
    return redirect('/dashboard')

