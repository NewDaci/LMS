from app import app, db
from models.model import Enrollments, Book_req, Messages
from flask import session
from flask import render_template
from flask import request
from flask import redirect, url_for
from datetime import date



@app.route("/requests")
def requests():
    if request.method == "GET":
        book_reqs = Book_req.query.all()
        return render_template("admin/requests.html", book_reqs=book_reqs)


@app.route("/requests/<int:id>", methods=["GET", "POST"])
def requests_status(id):

    if request.method == "POST":
        book_req = Book_req.query.filter_by(id=id).first()

        if "accept" in request.form:
            check = Enrollments.query.filter_by(user_id=book_req.user_id, book_id=book_req.book_id).first()

            if check:
                db.session.delete(check)
                db.session.commit()

            enroll = Enrollments(user_id=book_req.user_id, book_id=book_req.book_id, issue_date=book_req.issue_date, return_date=book_req.return_date)
            db.session.add(enroll)

            #drop message to user for approval
            msg = Messages(user_id=book_req.user_id, book_id=book_req.book_id, message="Approved")
            db.session.add(msg)
        
            db.session.delete(book_req)
            db.session.commit()

        elif "reject" in request.form:
            reason = request.form.get("reason")
            msg = Messages(user_id=book_req.user_id, book_id=book_req.book_id, message=reason)

            db.session.add(msg)
            db.session.delete(book_req)
            db.session.commit()
        return redirect(url_for("requests"))


#BOOK ENROLLMENTS

@app.route("/enrolls")
def enrolls():

    enrolls  = Enrollments.query.all()
    return render_template("admin/enrolls.html", enrolls=enrolls)


@app.route("/revoke/<int:id>")
def revoke(id):

    enroll = Enrollments.query.filter_by(id=id).first()

    db.session.delete(enroll)
    db.session.commit()
    return redirect("/enrolls")


@app.route("/auto_revoke")
def auto_revoke():

    enrolls = Enrollments.query.all()

    for i in enrolls:
        if date.today() > i.return_date:
            db.session.delete(i)

    db.session.commit()
    return redirect("/enrolls")
