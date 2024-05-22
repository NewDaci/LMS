from app import app, db, bcrypt
from models.model import User, Enrollments, Book, Sections, Messages, Book_req, Status
from flask import session
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import flash
from sqlalchemy import or_


@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        if 'user_id' in session.keys():
            return redirect(url_for("index"))
        return render_template("user_login.html")

    elif request.method == "POST":
        email = request.form["user-email"]
        passw = request.form["user-pass"]

        get_user = User.query.filter_by(email=email).first()
        if get_user:

            # if get_user.password == hash_pass:
            if bcrypt.check_password_hash(get_user.password, passw):
                #create a session to store user information
                session["user_id"] = get_user.id
                flash("Hello Reader! Welcome To Kalkaji Library. We have large collection of books to cater the reading needs of all kinds of readers. Happy Reading!!")
                return redirect(url_for("index"))
            
            flash("Wrong Password!")
            return redirect("/user_login")
        else:
            flash("User doesn't exists! Register First.")
            return redirect("/user_signup")


@app.route("/user_signup", methods=["GET", "POST"])
def user_signup():
    if request.method == "GET":
        return render_template("user_signup.html")

    elif request.method == "POST":
        username = request.form["user-name"]
        email = request.form["user-email"]
        passw = request.form["user-pass"]

        #check for already registered user
        alr_user = User.query.filter_by(email=email).first()

        if not alr_user:

            #hashing password
            pass_hash = bcrypt.generate_password_hash(passw).decode('utf-8')

            user = User(name=username, email=email, password=pass_hash)
            db.session.add(user)
            db.session.commit()

            get_user = User.query.filter_by(email=email).first()
            #create a session to store user information
            session["user_id"] = get_user.id
            flash("Hello Reader! Welcome To Kalkaji Library. We have large collection of books to cater the reading needs of all kinds of readers. Happy Reading!!")
            return redirect(url_for("index"))
        
        flash("Email Already Exists!")
        return redirect(url_for("user_signup"))


@app.route("/profile", methods=["GET", "POST"])
def profile():

    if request.method == "GET":
        # get id from session
        user_id = session.get("user_id")
        get_user = User.query.filter_by(id=user_id).first()

        # get issued books
        enrolls = Enrollments.query.filter_by(user_id=user_id).all()
        books = []
        for enroll in enrolls:
            l = Book.query.filter_by(id=enroll.book_id).first()
            books.append(l)
        return render_template("/profile/profile.html", user=get_user, books=books, i=len(books))

    elif request.method == "POST":
        if "update_details" in request.form:
            return redirect("/profile/update")


@app.route("/profile/update", methods=["GET", "POST"])
def update_profile():
    if request.method == "GET":
        return render_template("/profile/update.html")

    elif request.method == "POST":
        new_name = request.form.get("user-name")
        new_email = request.form.get("user-email")
        new_password = request.form.get("user-pass")

        # get user details from DB
        user_id = session.get("user_id")
        user = User.query.filter_by(id=user_id).first()
        if user:
            if new_name:
                user.name = new_name
            if new_email:
                user.email = new_email
            if new_password:
                pass_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user.password = pass_hash
            db.session.commit()
            flash("Profile updated successfully!")
            return redirect("/profile")
        flash("No User Found!")
        return redirect("/profile")



@app.route("/profile/delete/<int:id>")
def delete_profile(id):

    user = User.query.filter_by(id=id).first()

    l = []
    #remove book_req
    l.append(Book_req.query.filter_by(user_id=id).all())

    #remove enrollments
    l.append(Enrollments.query.filter_by(user_id=id).all())

    #remove messages
    l.append(Messages.query.filter_by(user_id=id).all())

    #remove status
    l.append(Status.query.filter_by(user_id=id).all())
    l.append([user])

    for i in l:
        for j in i:
            db.session.delete(j)
            
    db.session.commit()
    session.pop("user_id", None)
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    
    if request.method == 'POST':
        search_query = request.form['search']
        
        book_searched = Book.query.filter(Book.name.ilike(f'%{search_query}%')).all()
        section_searched = Sections.query.filter(or_(Sections.name.ilike(f'%{search_query}%'), Sections.description.ilike(f'%{search_query}%'))).all()
        author_searched = Book.query.filter(Book.author_name.ilike(f'%{search_query}%')).all()        
        # searched = db.session.query(Book, User).join(User, onclause=Book.id).filter(Book.name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', book_searched=book_searched, section_searched=section_searched, author_searched=author_searched, search_query=search_query)


@app.route("/message")
def message():
    messages = Messages.query.filter_by(user_id=session.get('user_id')).all()
    l = [ (msg, Book.query.filter_by(id=msg.book_id).first()) for msg in messages ]
    return render_template("message.html", messages=l)


@app.route("/message/read/<int:id>")
def msg_read(id):

    msg = Messages.query.filter_by(id=id).first()
    db.session.delete(msg)
    db.session.commit()
    return redirect("/message")


@app.route("/policy")
def policy():
    return render_template("policy.html")