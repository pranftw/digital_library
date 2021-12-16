from flask import url_for, render_template, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from __main__ import db, app

session = db.session

from models import *

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user

@app.context_processor
def context_processor():
    return dict(current_user=current_user)


@app.get("/")
@app.get("/home")
def home():
    """
        Lists all the features and provides links to login and register pages
        If logged in, it displays all the issued books and recommendations for Users
    """
    return render_template('home.html')


@app.route("/login",methods=['GET','POST'])
def login():
    """
        Users(faculties and students) have the same login and functionalities
        A checkbox if he's an admin and check the Admin table
    """
    # TODO: password matching
    if(request.method=='POST'):
        form_data = request.form.to_dict()
        user = session.query(User).filter_by(email=form_data['email']).first()
        login_user(user)
    return render_template('login.html')


@app.get("/logout")
@login_required
def logout():
    """
        Logs out the user
    """
    logout_user()
    return redirect(url_for('home'))


@app.route("/register",methods=['GET','POST'])
def register():
    """
        Users(faculties and students) have the same registration too
    """
    # TODO: Password hashing
    if(request.method=='POST'):
        form_data = request.form.to_dict()
        user = User(first_name=form_data['first_name'],last_name=form_data['last_name'],email=form_data['email'],password=form_data['password'])
        session.add(user)
        session.commit()
    return render_template('register.html')


@app.get("/profile")
@login_required
def profile():
    """
        Has functionalities to reset password, display all the information about the user
    """
    return render_template('profile.html')


@app.get("/explore/<sem>")
@login_required
def explore(sem):
    """
        Lists all the books for the user based on the sem
    """
    return render_template('explore.html')


@app.post("/transact/<book_id>")
@login_required
def transact(book_id):
    """
        Book can be issued or returned
        If issued, it returns, else it issues it appropriate links are set up
    """
    pass