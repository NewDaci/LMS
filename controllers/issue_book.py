from app import app, db
from models.model import Book, Book_req, User, Status, Enrollments
from flask import render_template, session, redirect, url_for, flash, request
from datetime import timedelta, date


@app.route("/issue-book")
def issue_book():

    books = Book.query.all()
    current_date = date.today()
    return render_template("issue_book.html", books=books, current_date=current_date)


@app.route("/issue-this-book/<int:id>", methods=["GET", "POST"])
def issue_this_book(id):

    if request.method == "POST":

        req_days = request.form.get("req_days")
        curr_date = request.form.get("curr_date").split("-")
        issue_date = date(int(curr_date[0]), int(curr_date[1]), int(curr_date[2]))
        
        #get book details
        book = Book.query.filter_by(id=id).first()

        #get user details
        get_user_id = session.get("user_id")
        user = User.query.filter_by(id=get_user_id).first()
        
        try:
            return_date = issue_date + timedelta(days=int(req_days))
        except:
            flash("INVALID REQUESTED DAYS! PLEASE TRY AGAIN")
            return redirect("/issue-book")
        
        # check for user total no of enrollments + book_req not > 5
        book_req_len = Book_req.query.filter_by(user_id=session.get('user_id')).all()
        if len(book_req_len) >= 5:
            flash("Requested Books are more than 5. PLEASE WAIT FOR ADMIN TO APPROVE BOOK BEFORE REQUESTING MORE... ")
            return redirect("/issue-book")
        
        # check whether the user is alread enrolled with the book_id
        check_enroll = Enrollments.query.filter_by(user_id=get_user_id, book_id=book.id).first()
        if check_enroll and check_enroll.return_date > date.today():
            flash("Already ENROLLED in this Book!")
            return redirect(url_for("issue_book"))
        
        
        # check for whether the book is already completed by user or not
        check = Status.query.filter_by(book_id=id, user_id=session.get('user_id')).first()
        if not check:
            enroll = Book_req(user_id=user.id, user_name=user.name, book_id=book.id, book_name=book.name, req_days=req_days, issue_date = issue_date, return_date=return_date)
            try:    
                db.session.add(enroll)
                db.session.commit()
            except:
                flash("Already REQUESTED for this BOOK!")
                return redirect(url_for("issue_book"))
        else:
            flash("YOU HAVE ALREADY COMPLETED THIS BOOK. PLEASE CHECK UNDER MY-BOOKS!!")
            return redirect("/issue-book")
        
        flash("Requested for book : " + book.name + " with  Book ID  : " + str(book.id))
        return redirect(url_for("issue_book"))


