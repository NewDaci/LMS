import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app import app, db
from models.model import Book, User, Enrollments, Rating, Sections, Status, Book_req, Feedback, Messages
from flask import session
from flask import render_template
from flask import request, flash
from flask import redirect, url_for
from datetime import date


######## Admin panel ##########

admin_routes = ["dashboard", "category", "all_books",
                "add_section", "delete_section", "update_section", "view_section",
                "view", "all_books", "new_book", "admin_delete", "admin_update",
                "users", "user_details", "user_delete",
                "requests", "requests_status", "enrolls", "auto_revoke", "revoke"]

user_routes = ["my_book", "feedback", "download",
               "issue_this_book", "profile", "update_profile", "delete_profile", "message"]

@app.before_request
def before_req():

    if "admin" not in session and request.endpoint in admin_routes:
        return redirect("/admin_login")
    
    elif "user_id" not in session and request.endpoint in user_routes:
        return redirect("/user_login")
    

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        if 'admin' in session.keys():
                return redirect(url_for("dashboard"))
        return render_template("admin/admin_login.html")

    elif request.method == "POST":
        admin_id = request.form["admin-id"]
        passw = request.form["admin-pass"]

        if admin_id == "admin":
            if passw == "123":
                session["admin"] = "123"
                return redirect("dashboard")

        flash("Invalid credentials! Try again")
        return redirect("admin_login")


@app.route("/dashboard")
def dashboard():

    books = Book.query.all()
    users = User.query.all()
    enrollments = Enrollments.query.all()
    returned_books = Status.query.all()
    sections = Sections.query.all()
    ratings = Rating.query.all()
    
    # section vs books
    sec_name = []
    sec_val = []
    for i in sections:
        sec_name.append(i.name)
        sec_val.append(len(Book.query.filter_by(section=i.id).all()))

    # books vs enrollments
    book_name = []
    enrolls = []
    for i in books:
        book_name.append(i.name)
        enrolls.append(len(Enrollments.query.filter_by(book_id=i.id).all()))

    # book vs ratings
    book_name_rate = []
    rate = []
    for i in books:
        if i.rating != None:
            book_name_rate.append(i.name)
            rate.append(i.rating)


    num_books = len(books)
    num_users = len(users)
    num_enrollments = len(enrollments)

    # book vs enrollments
    plt.figure(figsize=(18.9, 8))
    bars = plt.bar(book_name, enrolls, color=['gray', 'green', 'orange', 'yellow', 'pink', 'blue'], width=0.3)
    plt.xlabel('Books')
    plt.ylabel('Enrollments')
    plt.title('Books vs Enrollments')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() 
    for bar, value in zip(bars, enrolls):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), value, ha='center', va='bottom')
    plt.savefig('static/dashboard_chart.png') 
    plt.close()

    # book vs section
    plt.figure(figsize=(9.3,6))
    bars = plt.bar(sec_name, sec_val, color=['gray', 'green', 'orange', 'yellow', 'red', 'blue'])
    plt.xlabel("Section")
    plt.ylabel("No. of Books")
    plt.title("Section vs Books")
    for bar, value in zip(bars, sec_val):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), value, ha='center', va='bottom')
    plt.savefig('static/section.png')
    plt.close

    # book vs rating
    plt.figure(figsize=(9.3,6))
    bars = plt.bar(book_name_rate, rate, color=['gray', 'green', 'orange', 'yellow', 'red', 'blue'])
    plt.xlabel("Books")
    plt.ylabel("Rating")
    plt.title("Rating vs Books")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    for bar, value in zip(bars, rate):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), value, ha='center', va='bottom')
    plt.savefig('static/rating.png')
    plt.close

    return render_template("admin/dashboard.html", books=num_books, users=num_users, enrolls=num_enrollments, returned_books=len(returned_books))
    

############# CRUD OPERATIONS on BOOK ############

# View
@app.route("/view/<int:id>", methods=["GET", "POST"])
def view(id):

    if request.method == "GET":

        book = Book.query.filter_by(id=id).first()
        enrollments = book.enrollments

        users = []
        for i in enrollments:
            user = User.query.filter_by(id=i.user_id).first()
            users.append(user)

        return render_template("admin/view.html", book=book, users=users, i=len(users))
    elif request.method == "POST":
        return redirect(url_for("users"))


# Read
@app.route("/all-books", methods=["GET", "POST"])
def all_books():

    if request.method == "GET":
        books = Book.query.all()
        return render_template("admin/all_books.html", books=books)

    elif request.method == "POST":
        if "new_book" in request.form:
            return redirect(url_for("new_book"))


# Create
@app.route("/new-book", methods=["GET", "POST"])
def new_book():

    if request.method == "GET":
        
        sec = Sections.query.all()
        return render_template("admin/new_book.html", sec=sec)

    elif request.method == "POST":
        isbn = request.form.get("isbn")
        name = request.form.get("name")
        author = request.form.get("author")
        section = request.form.get("section")
        language = request.form.get("language")
        
        alr_ex_book = Book.query.filter_by(isbn=isbn).first()
        if alr_ex_book:
            flash("ISBN no already exists! Please provide unique ISBN no.")
            return redirect("all-books")

        try:
            form_date = request.form.get("date")
            a = form_date.split("-")
            b = date(int(a[0]), int(a[1]), int(a[2]))
        except:
            flash("Invalid Date!")
            return redirect("all-books")
        content = request.form.get("content")

        new_book = Book(
            isbn=isbn,
            name=name,
            author_name=author,
            language=language,
            date_added=b,
            content=content,
            section=section,
        )
        db.session.add(new_book)
        db.session.commit()

        flash("Book has been Added Successfully!")
        return redirect("all-books")


# Delete
@app.route("/delete/<int:id>")
def admin_delete(id):

    l=[]
    book = Book.query.filter_by(id=id).first()

    l.append(book.enrollments)
    l.append(book.ratings)
    l.append(Book_req.query.filter_by(book_id=id).all())
    l.append(Feedback.query.filter_by(book_id=id).all())
    l.append(Messages.query.filter_by(book_id=id).all())
    l.append(Status.query.filter_by(book_id=id).all())

    for i in l:
        for j in i:
            db.session.delete(j)

    db.session.commit() 
    db.session.delete(book)
    db.session.commit()
    flash("Book has been Deleted Successfully!")
    return redirect("/all-books")


# Update
@app.route("/update/<int:id>", methods=["GET", "POST"])
def admin_update(id):

    if request.method == "GET":

        book = Book.query.filter_by(id=id).first()
        sec = Sections.query.all()
        return render_template("admin/update.html", book=book, sec=sec)

    elif request.method == "POST":

        book = Book.query.filter_by(id=id).first()

        isbn = request.form.get("isbn")
        name = request.form.get("name")
        author = request.form.get("author")
        section = request.form.get("section")
        language = request.form.get("language")

        form_date = request.form.get("date")
        a = form_date.split("-")
        b = date(int(a[0]), int(a[1]), int(a[2]))

        content = request.form.get("content")

        book.isbn = isbn
        book.name = name
        book.author_name = author
        book.section = section
        book.language = language
        book.date_added = b
        book.content = content

        db.session.commit()
        flash("Book has been Updated Successfully!")
        return redirect("/all-books")


################## CRUD on USERS #####################

@app.route("/users")
def users():

    users = User.query.all()
    return render_template("admin/users.html", users=users)


@app.route("/user_details/<int:id>")
def user_details(id):

    if request.method == "GET":
        user = User.query.filter_by(id=id).first()

        enrollments = Enrollments.query.filter_by(user_id=user.id).all()

        books = []
        for i in enrollments:
            book = Book.query.filter_by(id=i.book_id).first()
            if book not in books:
                books.append(book)

        return render_template("admin/user_details.html", books=books, user=user, i=len(books))

    elif request.method == "POST":
        return redirect(url_for("users"))
    

@app.route("/user_delete/<int:id>")
def user_delete(id):

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

    for i in l:
        for j in i:
            db.session.delete(j)

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("users"))

    


