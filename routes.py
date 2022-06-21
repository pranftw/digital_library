from flask import url_for, render_template, redirect, request, flash
from flask import session as flask_session
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from __main__ import db, app
import secrets


session = db.session


from models import *
from helper import send_reset_email, hash_password, get_token, validate_token, get_due_date, send_notify_email, validate_form_data, send_verification_email


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


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))


@app.context_processor
def context_processor():
    return dict(current_user=current_user, enumerate=enumerate, request=request)


@app.errorhandler(404)
def error404(e):
    return render_template('404.html')


@app.errorhandler(500)
def error500(e):
    return render_template('500.html')


def get_user(user_id):
    return session.query(User).filter_by(id=user_id).first()

def get_book(book_id):
    return session.query(Book).filter_by(id=book_id).first()


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
            due_date,due_diff = get_due_date(iss.date)
            if(due_diff>0):
                total_due_days+=due_diff
            due_dates.append(due_date)
        fine = total_due_days*5

        notify = session.query(Notify).filter_by(user_id=current_user.id).all()
        book_requests = session.query(Requests).all()
        approval_requests = session.query(ToBeApproved).filter_by(user_id=current_user.id).all()
        approval_issue_requests = session.query(ToBeApproved).filter_by(type_approval='issue').all()
        approval_return_requests = session.query(ToBeApproved).filter_by(type_approval='return').all()
        watchlist_books = []
        for noti in notify:
            watchlist_books.append(session.query(Book).filter_by(id=noti.book_id).first())
        to_be_approved_books = []
        for appr in approval_requests:
            to_be_approved_books.append((session.query(Book).filter_by(id=appr.book_id).first(),appr.type_approval))
        return render_template('home.html', books=books, due_dates=due_dates, fine=fine, watchlist_books=watchlist_books, to_be_approved_books=to_be_approved_books,book_requests=book_requests, approval_issue_requests=approval_issue_requests, approval_return_requests=approval_return_requests, get_user=get_user, get_book=get_book)
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
        errors = validate_form_data(form_data)
        if len(errors)!=0:
            flash('<br>'.join(errors))
            return redirect(request.referrer)
        user = session.query(User).filter_by(email=form_data['email']).first()
        if user is None:
            flash("You aren't registered yet! Register now!")
            return redirect(url_for('register'))
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
        errors = validate_form_data(form_data)
        existing_user = session.query(User).filter_by(email=form_data['email']).first()
        if existing_user:
            errors.append("User already present with that email!")
        if len(errors)!=0:
            flash('<br>'.join(errors))
            return redirect(request.referrer)
        flask_session['registration_data'] = form_data
        return redirect(url_for('send_verification_token'),307)
    return render_template('register.html')


@app.post("/send_verification_token")
def send_verification_token():
    """
        Sends verification token for new users who are registering
    """
    registration_data = flask_session.get('registration_data')
    if not(registration_data):
        flash("You haven't started the registration process yet!")
        return redirect(url_for('register'))
    verification_token = secrets.token_hex(4)
    send_verification_email(flask_session['registration_data']['email'],verification_token)
    verification_token_hash = hash_password(verification_token)
    flask_session['verification_token_hash'] = verification_token_hash
    flash("Verification token sent! Check your email!")
    return redirect(url_for('verify_token'))


@app.route("/verify_token",methods=['GET','POST'])
def verify_token():
    """
        Verifies the verification token sent to the email
    """
    registration_data = flask_session.get('registration_data')
    if request.method=='POST':
        form_data = request.form.to_dict()
        session_verification_token_hash = flask_session.get('verification_token_hash')
        if hash_password(form_data['token'])!=session_verification_token_hash:
            flash("Invalid verification code!")
            return redirect(request.referrer)
        hashed_pw = hash_password(registration_data['password'])
        user = User(first_name=registration_data['first_name'],last_name=registration_data['last_name'],email=registration_data['email'],password=hashed_pw)
        session.add(user)
        session.commit()
        flash("Successfully registered! You can now login!")
        flask_session.pop('registration_data')
        flask_session.pop('verification_token_hash')
        return redirect(url_for('home'))
    if not(registration_data):
        flash("You haven't started the registration process yet!")
        return redirect(url_for('register'))
    return render_template('verify_token.html')


@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    """
        Sends a request to reset the password
    """
    if(request.method=='POST'):
        form_data = request.form.to_dict()
        errors = validate_form_data(form_data)
        if len(errors)!=0:
            flash('<br>'.join(errors))
            return redirect(request.referrer)
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
    """
        Allows the user to reset the password after validating the reset_request token
    """
    payload = validate_token(token)
    print(payload)
    if(payload):
        if(request.method=='POST'):
            form_data = request.form.to_dict()
            errors = validate_form_data(form_data)
            if len(errors)!=0:
                flash('<br>'.join(errors))
                return redirect(request.referrer)
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


@app.get("/explore")
@login_required
def explore_links():
    """
        Contains all the links to different senesters' explore pages
    """
    return render_template('explore_links.html')


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
    return render_template('explore.html', books=books, issue_status=issue_status, num_issued=len(issued), sem=sem)


@app.post("/transact/<book_id>")
@login_required
def transact(book_id):
    """
        Book can be issued or returned
        If issued, it returns, else it issues it appropriate links are set up
    """
    if current_user.is_admin==True:
        flash("Admin can't issue books!")
        return redirect(request.referrer)
    issued_book = session.query(Issued).filter_by(book_id=book_id).first()
    book_obj = session.query(Book).filter_by(id=book_id).first()
    if book_obj is None:
        flash("Invalid book id!")
        return redirect(request.referrer)
    if issued_book: # RETURN IT
        # orig_stocks = book_obj.stocks
        # book_obj.stocks+=1
        # if book_obj.stocks!=0 and orig_stocks==0:
        #     notify_objs = session.query(Notify).filter_by(book_id=book_id).all()
        #     emails = []
        #     for notify_obj in notify_objs:
        #         emails.append(session.query(User.email).filter_by(id=notify_obj.user_id).first()[0])
        #         session.delete(notify_obj)
        #     send_notify_email(emails,book_obj,url_for('search',search=book_obj.title,book_id=book_obj.id,_external=True))
        # session.delete(issued_book)
        existing_request = session.query(ToBeApproved).filter_by(book_id=book_id, user_id=current_user.id, type_approval='return').first()
        if existing_request is None:
            approval = ToBeApproved(book_id=book_id, user_id=current_user.id, type_approval='return')
            session.add(approval)
            session.commit()
            flash("Book successfully returned! Waiting for approval!")
        else:
            flash("Book already submitted for return approval!")
    else: # ISSUE IT
        existing_request = session.query(ToBeApproved).filter_by(book_id=book_id, user_id=current_user.id, type_approval='issue').first()
        if existing_request is None:
            already_issued = session.query(Issued).filter_by(user_id=current_user.id).all()
            waiting_for_approval = session.query(ToBeApproved).filter_by(user_id=current_user.id).all()
            if(len(already_issued)+len(waiting_for_approval)!=5):
                approval = ToBeApproved(book_id=book_id, user_id=current_user.id, type_approval='issue')
                session.add(approval)
                # issue = Issued(book_id=book_id, user_id=current_user.id)
                # book_obj.stocks-=1
                # session.add(issue)
                session.commit()
                flash("Book successfully issued! Waiting for approval!")
            else:
                flash("You have reached your limit!")
        else:
            flash("Book already submitted for issue approval!")
    return redirect(request.referrer)


@app.post("/approve/<book_id>/<user_id>/<type_approval>")
@login_required
def approve(book_id, user_id, type_approval):
    if current_user.is_admin:
        book_obj = session.query(Book).filter_by(id=book_id).first()
        if book_obj is None:
            flash("Invalid book id!")
            return redirect(request.referrer)
        approval = session.query(ToBeApproved).filter_by(user_id=user_id,book_id=book_id,type_approval=type_approval).first()
        if approval:
            session.delete(approval)
            session.commit()
            if type_approval=='issue':
                issue = Issued(book_id=book_id, user_id=user_id)
                book_obj.stocks-=1
                session.add(issue)
                session.commit()
                flash("Approved issue!")
            else:
                issued_book = session.query(Issued).filter_by(book_id=book_id).first()
                orig_stocks = book_obj.stocks
                book_obj.stocks+=1
                if book_obj.stocks!=0 and orig_stocks==0:
                    notify_objs = session.query(Notify).filter_by(book_id=book_id).all()
                    emails = []
                    for notify_obj in notify_objs:
                        emails.append(session.query(User.email).filter_by(id=notify_obj.user_id).first()[0])
                        session.delete(notify_obj)
                    send_notify_email(emails,book_obj,url_for('search',search=book_obj.title,book_id=book_obj.id,_external=True))
                session.delete(issued_book)
                session.commit()
                flash("Approved return!")
    else:
        flash("Only admins can approve!")
    return redirect(request.referrer)


@app.post("/remove_approval_request/<book_id>")
@login_required
def remove_approval_request(book_id):
    user_id = current_user.id
    approval = session.query(ToBeApproved).filter_by(user_id=user_id,book_id=book_id).first()
    if approval:
        session.delete(approval)
        session.commit()
        flash("Removed approval request!")
    return redirect(request.referrer)


@app.post("/notify/<book_id>")
@login_required
def notify(book_id):
    """
        Opt in for notifications of a book which is not in stock
    """
    form_data = request.form.to_dict()
    errors = validate_form_data(form_data)
    if len(errors)!=0:
        flash('<br>'.join(errors))
        return redirect(request.referrer)
    notify_obj = session.query(Notify).filter_by(user_id=current_user.id,book_id=book_id).first()
    if notify_obj:
        flash("You have already opted to get notified for this book!")
    else:
        notify_obj = Notify(book_id=book_id,user_id=current_user.id)
        session.add(notify_obj)
        session.commit()
        flash("You'll be notified when this book is in stock!")
    return redirect(request.referrer)


@app.post("/denotify/<book_id>")
@login_required
def denotify(book_id):
    """
        Opt out of notifications for a book
    """
    form_data = request.form.to_dict()
    errors = validate_form_data(form_data)
    if len(errors)!=0:
        flash('<br>'.join(errors))
        return redirect(request.referrer)
    notify_obj = session.query(Notify).filter_by(user_id=current_user.id,book_id=book_id).first()
    if notify_obj:
        session.delete(notify_obj)
        session.commit()
        flash("Successfully opted out of getting notified for this book!")
    else:
        flash("You haven't opted to get notifications for this book!")
    return redirect(request.referrer)


@app.route("/search", methods=['GET','POST'])
@login_required
def search():
    """
        Search for a book
    """
    if request.method=='POST' or request.args.get('search'):
        if request.method=='POST':
            form_data = request.form.to_dict()
        else:
            form_data = request.args.to_dict()
        errors = validate_form_data(form_data)
        if len(errors)!=0:
            flash('<br>'.join(errors))
            return redirect(request.referrer)
        issued = session.query(Issued).filter_by(user_id=current_user.id).all()
        issue_status = []
        books = session.query(Book).filter(Book.title.like("%" + form_data['search'] + "%"))
        if form_data.get('book_id'):
            books = books.filter_by(id=form_data.get('book_id'))
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
        errors = validate_form_data(form_data)
        if len(errors)!=0:
            flash('<br>'.join(errors))
            return redirect(request.referrer)
        if int(form_data['stocks'])<0:
            flash("Stocks can't be negative!")
            return redirect(request.referrer)
        new_book = Book(title=form_data['title'], author=form_data['author'], sem=form_data['sem'], subject=form_data['subject'], stocks=form_data['stocks'], img_url=form_data['img_url'])
        session.add(new_book)
        session.commit()
        flash("Successfully added a new book!")
    else:
        flash("Only admins have access to add a book!")
    return redirect(url_for('home'))


@app.post("/modify/<book_id>")
def modify_stocks(book_id):
    """
        Allows the admin to modify the stocks of a book
    """
    form_data = request.form.to_dict()
    errors = validate_form_data(form_data)
    if len(errors)!=0:
        flash('<br>'.join(errors))
        return redirect(request.referrer)
    book = session.query(Book).filter_by(id=book_id).first()
    if book is None:
        flash("There is no book with that book id!")
        return redirect(request.referrer)
    if current_user.is_admin==False:
        flash("Only admins have permission to modify stocks!")
        return redirect(request.referrer)
    form_data_stocks = int(form_data['stocks'])
    if(book.stocks+form_data_stocks<0):
        flash("Book stocks can't be negative!")
    else:
        orig_stocks = book.stocks
        book.stocks+=form_data_stocks
        session.commit()
        if book.stocks!=0 and orig_stocks==0:
            notify_objs = session.query(Notify).filter_by(book_id=book_id).all()
            emails = []
            for notify_obj in notify_objs:
                emails.append(session.query(User.email).filter_by(id=notify_obj.user_id).first()[0])
                session.delete(notify_obj)
            send_notify_email(emails,book,url_for('search',search=book.title,book_id=book.id,_external=True))
            session.commit()
        flash("Stock updated!")
    return redirect(request.referrer)
        

@app.post("/request_book")
def request_book():
    """
        Request a book
    """
    form_data = request.form.to_dict()
    errors = validate_form_data(form_data)
    if len(errors)!=0:
        flash('<br>'.join(errors))
        return redirect(request.referrer)
    request_obj = Requests(title=form_data['title'],author=form_data['author'])
    session.add(request_obj)
    session.commit()
    flash("Successfully requested for the book!")
    return redirect(request.referrer)


@app.post("/delete_request/<request_id>")
def delete_request(request_id):
    """
        Delete a book request upon adding of a new book or if the book isn't available
    """
    request_obj = session.query(Requests).filter_by(id=request_id).first()
    if request_obj:
        session.delete(request_obj)
        session.commit()
        flash("Request successfully deleted!")
    else:
        flash("Request with the corresponding request id not available!")
    return redirect(url_for('home'))
