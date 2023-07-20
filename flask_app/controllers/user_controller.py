from flask import Flask, render_template, request, redirect, request, session, flash
from flask_app import app
from flask_app.models import user_model
from flask_app.models import show_model
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route('/register/user', methods=["POST"])
def register():
    raw_user_data = request.form
    if not user_model.User.new_email(raw_user_data):
        print("not new")
        flash("Already an email address. Please log in.")
        return redirect('/')
    if not user_model.User.validate(raw_user_data):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(raw_user_data['password'])
    print(pw_hash)
    valid_user_data = {
        "first_name": raw_user_data["first_name"],
        "last_name": raw_user_data["last_name"],
        "password": pw_hash,
        "email": raw_user_data["email"]
    }
    new_user_id=user_model.User.save(valid_user_data) #database has now returned the id of the new created user
    session['first_name'] = valid_user_data['first_name'] #session is a dictionary of whatever data is currently accessible
    session['last_name'] = valid_user_data['last_name']
    session['email'] = valid_user_data['email']
    session['user_id'] = new_user_id
    return redirect('/dashboard')

# @app.route("/reg_success")
# def reg_success():
#     return render_template("dashboard.html")

@app.route('/login/user', methods=["POST"])
def login_user():
    log_in_data = request.form
    print("THIS IS LOG_IN_DATA=", log_in_data)
    log_in_user = user_model.User.get_by_email(log_in_data["email"])
    if not log_in_user:
        flash('Please Register First', 'login')
        return redirect('/')
    if not user_model.User.validate_login(log_in_data["password"], log_in_user): 
        flash('Please Register First', 'login')
        return redirect('/')
    session['first_name'] = log_in_user.first_name #session is a dictionary of whatever data is currently accessible
    session['last_name'] = log_in_user.last_name
    session['email'] = log_in_user.email
    session['user_id'] = log_in_user.id
    return redirect('/dashboard')

# @app.route("/login_success")
# def login_success():
#     if 'user_id' in session:
#         return render_template("dashboard.html")
#     else:
#         redirect('/dashboard')

@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        current_user = user_model.User.get_by_id(session['user_id'])
    all_shows = show_model.Show.get_all()
    print("SHOWS TO DASHBOARD:", all_shows)
    return render_template("dashboard.html", all_shows=all_shows, user=current_user)

@app.route("/logout")
def logout():
    session.clear()
    print("session cleared")
    return render_template("login.html")




#examples:
# @app.route("/dashboard")
# def index():
#     users = User.get_all()
#     print(users)
#     return render_template("read_all.html", all_users=users)

# @app.route("/create_user")
# def create_user():
#     return render_template("create.html")

#@app.route('/create', methods=['POST'])
#def create_burger():
# if there are errors:
# We call the staticmethod on Burger model to validate
#    if not Burger.validate_burger(request.form):
# redirect to the route where the burger form is rendered.
#        return redirect('/')
# else no errors:
#    Burger.save(request.form)
#    return redirect("/burgers"


# from flask_app.models.user import User
# @app.route('/created', methods=["POST"])
# def created():
#     data = {
#         "first_name": request.form["first_name"],
#         "last_name": request.form["last_name"],
#         "email": request.form["email"]
#     }
#     new_user_id=User.save(data)
#	print("Got Post Info")
# Here we add two properties to session to store the name and email
#   session['username'] = request.form['name']
#   session['useremail'] = request.form['email']
#   return redirect('/show')
#
#     return redirect(f'/read_one/{new_user_id}')

#@app.route('/register/user', methods=['POST'])
#def register():
# validate the form here ...
# create the hash
#    pw_hash = bcrypt.generate_password_hash(request.form['password'])
#    print(pw_hash)
# put the pw_hash into the data dictionary
#    data = {
#        "username": request.form['username'],
#        "password" : pw_hash
#    }
# Call the save @classmethod on User
#    user_id = User.save(data)
# store user id into session
#    session['user_id'] = user_id
#    return redirect("/dashboard")


# from flask_app.models.user import User
# @app.route("/read_one/<int:id>")
# def read_one(id):
#     data = {
#         'id': id
#     }
#     return render_template("read_one.html", user = User.get_one(data))

#def show_user():
#    return render_template('show.html', name_on_template=session['username'], email_on_template=session['useremail'])


# @app.route('/edit/<int:id>')
# def edit(id):
#     data = {
#         'id': id,
#     }
#     # User.save(data)
#     return render_template("update.html", user = User.get_one(data))

# @app.route('/update', methods=['POST'])
# def update():
#     User.update(request.form)
#     new_user_id = request.form["id"]
#     return redirect(f'/read_one/{new_user_id}')

# @app.route('/delete/<int:id>')
# def delete(id):
#     data = {
#         'id': id
#     }
#     User.delete(data)
#     return redirect('/')
