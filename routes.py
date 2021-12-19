# TODO: Forms have to be validated!

from flask import url_for, render_template, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from __main__ import db, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

session = db.session

from models import *
from helper import send_reset_email, hash_password, get_token, validate_token, get_due_date, send_notify_email

def objs_to_dict(objs):
    objs_list = []
    for obj in objs:
        obj_dict = {}
        for (var,val) in vars(obj).items():
            if(not(var.startswith("_"))):
                obj_dict[var] = val
        objs_list.append(obj_dict)
    return objs_list

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user

@app.context_processor
def context_processor():
    return dict(current_user=current_user, enumerate=enumerate, request=request)


@app.get("/")
@app.get("/home")
def home():
    """
        Lists all the features and provides links to login and register pages
        If logged in, it displays all the issued books and recommendations for Users
    """
    total_due_days = 0
    if current_user.is_authenticated:
        issued = session.query(Issued).filter_by(user_id=current_user.id).all()
        books = []
        for iss in issued:
            books.append(session.query(Book).filter_by(id=iss.book_id).first())
        due_dates = []
        for iss in issued:
            due_date,due_diff = get_due_date(iss.issued_date)
            if(due_diff>0):
                total_due_days+=due_diff
            due_dates.append(due_date)
        fine = total_due_days*5

        notify = session.query(Notify).filter_by(user_id=current_user.id).all()
        watchlist_books = []
        for noti in notify:
            watchlist_books.append(session.query(Book).filter_by(id=noti.book_id).first())
        return render_template('home.html', books=books, due_dates=due_dates, fine=fine, watchlist_books=watchlist_books)
    else:
        return render_template('home.html')


@app.route("/login",methods=['GET','POST'])
def login():
    """
        Users(faculties and students) have the same login and functionalities
        A checkbox if he's an admin and check the Admin table
    """
    if(request.method=='POST'):
        form_data = request.form.to_dict()
        user = session.query(User).filter_by(email=form_data['email']).first()
        hashed_form_pw = hash_password(form_data['password'])
        if(hashed_form_pw==user.password):
            flash("Successful login!")
            login_user(user, remember=form_data.get('remember', False))
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password!")
            return redirect(url_for('login'))
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
    if(request.method=='POST'):
        form_data = request.form.to_dict()
        hashed_pw = hash_password(form_data['password'])
        user = User(first_name=form_data['first_name'],last_name=form_data['last_name'],email=form_data['email'],password=hashed_pw)
        session.add(user)
        session.commit()
        flash("Successfully registered!")
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if(request.method=='POST'):
        form_data = request.form.to_dict()
        user = session.query(User).filter_by(email=form_data['email']).first()
        if user:
            token = get_token(user)
            send_reset_email(user.email,url_for('reset_password',token=token,_external=True))
            flash("Link to reset password has been sent to your email!")
            return redirect(url_for('login'))
        else:
            flash("You are not registered with us!")
    return render_template('reset_request.html')


@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_password(token):
    payload = validate_token(token)
    print(payload)
    if(payload):
        if(request.method=='POST'):
            form_data = request.form.to_dict()
            user = session.query(User).filter_by(email=payload).first()
            hashed_pw = hash_password(form_data['password'])
            user.password = hashed_pw
            session.commit()
            flash("Password successfully reset!")
            return redirect(url_for('login'))
    else:
        flash("Token invalid or exceeded time limit!")
        return redirect(url_for('reset_request'))
    return render_template('reset_password.html')


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
    if int(sem) in range(3,9):
        issued = session.query(Issued).filter_by(user_id=current_user.id).all()
        issue_status = []
        books = session.query(Book).filter_by(sem=sem).all()
        for i in range(len(books)):
            status = False
            for j in range(len(issued)):
                if books[i].id==issued[j].book_id:
                    status = True
                    break
            issue_status.append(status)
    else:
        flash("Invalid semester!")
        return redirect(url_for('home'))
    return render_template('explore.html', books=books, issue_status=issue_status, num_issued=len(issued))


@app.post("/transact/<book_id>")
@login_required
def transact(book_id):
    """
        Book can be issued or returned
        If issued, it returns, else it issues it appropriate links are set up
    """
    issued_book = session.query(Issued).filter_by(book_id=book_id).first()
    book_obj = session.query(Book).filter_by(id=book_id).first()
    if book_obj is None:
        flash("Invalid book id!")
        return redirect(request.referrer)
    if issued_book: # RETURN IT
        book_obj.stocks+=1
        session.delete(issued_book)
        session.commit()
        flash("Book successfully returned!")
    else: # ISSUE IT
        already_issued = session.query(Issued).filter_by(user_id=current_user.id).all()
        if(len(already_issued)!=5):
            issue = Issued(book_id=book_id, user_id=current_user.id)
            book_obj.stocks-=1
            session.add(issue)
            session.commit()
            flash("Book successfully issued!")
        else:
            flash("You have reached your limit!")
    return redirect(request.referrer)


@app.post("/notify/<book_id>")
@login_required
def notify(book_id):
    form_data = request.form.to_dict()
    notify_obj = session.query(Notify).filter_by(book_id=book_id).first()
    if notify_obj:
        flash("You have already opted to get notified for this book!")
    else:
        notify_obj = Notify(book_id=book_id,user_id=current_user.id)
        session.add(notify_obj)
        session.commit()
        flash("You'll be notified when this book is in stock!")
    return redirect(request.referrer)


@app.route("/search", methods=['GET','POST'])
@login_required
def search():
    """
        Search for a book
    """
    if request.method=='POST':
        form_data = request.form.to_dict()
        issued = session.query(Issued).filter_by(user_id=current_user.id).all()
        issue_status = []
        books = session.query(Book).filter(Book.title.like("%" + form_data['search'] + "%"))
        books = books.order_by(Book.title).all()
        for i in range(len(books)):
            status = False
            for j in range(len(issued)):
                if books[i].id==issued[j].book_id:
                    status = True
                    break
            issue_status.append(status)
        return render_template('search.html',books=books,issue_status=issue_status)
    return render_template('search.html')


@app.post("/add/book")
def add_book():
    """
        Add a new book to the database. Only admin has access to do this
    """
    if current_user.is_admin:
        form_data = request.form.to_dict()
        new_book = Book(title=form_data['title'], author=form_data['author'], sem=form_data['sem'], subject=form_data['subject'], stocks=form_data['stocks'])
        session.add(new_book)
        session.commit()
        flash("Successfully added a new book!")
    else:
        flash("Only admins have access to add a book!")
    return redirect(url_for('home'))


@app.post("/modify/<book_id>")
def modify_stocks(book_id):
    form_data = request.form.to_dict()
    book = session.query(Book).filter_by(id=book_id).first()
    if book is None:
        flash("There is no book with that book id!")
        return redirect(request.referrer)
    if current_user.is_admin==False:
        flash("Only admins have permission to modify stocks!")
        return redirect(request.referrer)
    if(book.stocks+int(form_data['stocks'])<0):
        flash("Book stocks can't be negative!")
    else:
        orig_stocks = book.stocks
        book.stocks+=int(form_data['stocks'])
        session.commit()
        if book.stocks!=0 and orig_stocks==0:
            notify_objs = session.query(Notify).filter_by(book_id=book_id).all()
            emails = []
            for notify_obj in notify_objs:
                emails.append(session.query(User.email).filter_by(id=notify_obj.user_id).first()[0])
                session.delete(notify_obj)
            send_notify_email(emails,book,url_for('explore',sem=book.sem, _external=True))
            session.commit()
        flash("Stock updated!")
    return redirect(request.referrer)
        
